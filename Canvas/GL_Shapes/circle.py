import ctypes

from OpenGL import GL as gl
from OpenGL.GL import shaders

from Canvas.buffer import Buffer


BOUNDING_VERTICES = (ctypes.c_float * 12)(
    -1, -1,
    -1, 1,
    1, -1,

    -1, 1,
    1, 1,
    1, -1
)


vertex_shader = """#version 330
in vec2 position;

in vec3 center;
in vec2 radii;  //x: radius, y: stroke width
in vec4 colorFill;
in vec4 colorStroke;

uniform vec2 window;

out vec2 fragRadii;
out vec4 fragColorF;
out vec4 fragColorS;
out vec2 toCenter;

void main() {
    gl_Position = vec4(
        2.0f * (position.x*radii.x+center.x)/window.x - 1.0f,
        1.0f - 2.0f * (position.y*radii.x+center.y)/window.y,
        -center.z, 1.0
    );
    toCenter = vec2(
        radii.x*position.x,
        radii.x*position.y
    );
    fragRadii = radii;
    fragColorF = colorFill;
    fragColorS = colorStroke;
}
"""

fragment_shader = """#version 330
in vec2 toCenter;

in vec2 fragRadii;
in vec4 fragColorF;
in vec4 fragColorS;

out vec4 color;
void main() {
    float r = length(toCenter);
    if(r <= fragRadii.x) {
        if(r >= fragRadii.x-fragRadii.y)
            color = fragColorS;
        else
            color = fragColorF;
    } else
        color = vec4(0, 0, 0, 0);
}
"""


class Circle_GL():
    def __init__(self):
        self.program = shaders.compileProgram(
            shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
        )
        gl.glUseProgram(self.program)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vertices = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertices)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(BOUNDING_VERTICES),
            BOUNDING_VERTICES,
            gl.GL_STATIC_DRAW
        )

        positionAttr = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(positionAttr)
        gl.glVertexAttribPointer(
            positionAttr, 2, gl.GL_FLOAT, gl.GL_FALSE,
            2*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0)
        )

        # Custom settings
        self.configBuffer = Buffer(ctypes.c_float, 13)
        self.glConfigBuffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.glConfigBuffer)

        centerAttr = gl.glGetAttribLocation(self.program, "center")
        radiiAttr = gl.glGetAttribLocation(self.program, "radii")
        colorFAttr = gl.glGetAttribLocation(self.program, "colorFill")
        colorSAttr = gl.glGetAttribLocation(self.program, "colorStroke")

        gl.glEnableVertexAttribArray(centerAttr)
        gl.glEnableVertexAttribArray(radiiAttr)
        gl.glEnableVertexAttribArray(colorFAttr)
        gl.glEnableVertexAttribArray(colorSAttr)

        gl.glVertexAttribDivisor(centerAttr, 1)
        gl.glVertexAttribDivisor(radiiAttr, 1)
        gl.glVertexAttribDivisor(colorFAttr, 1)
        gl.glVertexAttribDivisor(colorSAttr, 1)

        stride = (3+2+4+4) * ctypes.sizeof(ctypes.c_float)
        gl.glVertexAttribPointer(
            centerAttr, 3, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(0)
        )
        gl.glVertexAttribPointer(
            radiiAttr, 2, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float))
        )
        gl.glVertexAttribPointer(
            colorFAttr, 4, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(5*ctypes.sizeof(ctypes.c_float))
        )
        gl.glVertexAttribPointer(
            colorSAttr, 4, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(9*ctypes.sizeof(ctypes.c_float))
        )
        self.u_window = gl.glGetUniformLocation(self.program, "window")

        gl.glBindVertexArray(0)

    def add(self, pos, radius, stroke_width, fill_color, stroke_color, zindex):
        self.configBuffer.push_row((
            *pos, zindex,
            radius, stroke_width,
            *fill_color, *stroke_color
        ))

    def render(self, window_size):
        gl.glUseProgram(self.program)
        gl.glUniform2f(self.u_window, *window_size)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.glConfigBuffer)

        b_size, d_data = self.configBuffer.get_buffer()
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            b_size,
            d_data,
            gl.GL_DYNAMIC_DRAW
        )
        gl.glDrawArraysInstanced(
            gl.GL_TRIANGLES, 0, 6,
            self.configBuffer.row_count()
        )

        gl.glBindVertexArray(0)
        self.configBuffer.clear()
