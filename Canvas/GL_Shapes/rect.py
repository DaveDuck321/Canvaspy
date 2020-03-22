import ctypes

from OpenGL import GL as gl
from OpenGL.GL import shaders

from Canvas.buffer import Buffer


RECT_VERTICES = (ctypes.c_float * 12)(
    0, 0,
    0, 1,
    1, 0,

    0, 1,
    1, 1,
    1, 0,
)


rect_vertex_shader = """#version 330
in vec2 position;

in vec3 offset; //x: screen x, y screen y, z: z-index
in vec3 dimensions;  //x: width, y: height, z: border
in vec4 colorFill;
in vec4 colorStroke;

uniform vec2 window;

out float width;
out vec4 fromEdge;
out vec4 fragColorF;
out vec4 fragColorS;

void main() {
    gl_Position = vec4(
        2.0f * (position.x*dimensions.x+offset.x)/window.x - 1.0f,
        1.0f - 2.0f * (position.y*dimensions.y+offset.y)/window.y,
        -offset.z, 1.0
    );
    width = dimensions.z;
    fromEdge = vec4(
        position.x*dimensions.x,
        position.y*dimensions.y,
        (1.0f-position.x)*dimensions.x,
        (1.0f-position.y)*dimensions.y
    );
    fragColorF = colorFill;
    fragColorS = colorStroke;
}
"""

rect_fragment_shader = """#version 330
in vec4 fromEdge;

in float width;
in vec4 fragColorF;
in vec4 fragColorS;

out vec4 color;
void main() {
    if(fromEdge.x <= width
        || fromEdge.y <= width
        || fromEdge.z <= width
        || fromEdge.w <= width)
        color = fragColorS;
    else
        color = fragColorF;
}
"""


class Rect_GL():
    def __init__(self):
        self.rect_program = shaders.compileProgram(
            shaders.compileShader(rect_vertex_shader, gl.GL_VERTEX_SHADER),
            shaders.compileShader(rect_fragment_shader, gl.GL_FRAGMENT_SHADER)
        )
        gl.glUseProgram(self.rect_program)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vertices = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertices)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(RECT_VERTICES),
            RECT_VERTICES,
            gl.GL_STATIC_DRAW
        )

        positionAttr = gl.glGetAttribLocation(self.rect_program, "position")
        gl.glEnableVertexAttribArray(positionAttr)
        gl.glVertexAttribPointer(
            positionAttr, 2, gl.GL_FLOAT, gl.GL_FALSE,
            2*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0)
        )

        # Custom settings
        self.configBuffer = Buffer(ctypes.c_float, 14)
        self.glConfigBuffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.glConfigBuffer)

        offsetAttr = gl.glGetAttribLocation(self.rect_program, "offset")
        dimsAttr = gl.glGetAttribLocation(self.rect_program, "dimensions")
        colorFAttr = gl.glGetAttribLocation(self.rect_program, "colorFill")
        colorSAttr = gl.glGetAttribLocation(self.rect_program, "colorStroke")

        gl.glEnableVertexAttribArray(offsetAttr)
        gl.glEnableVertexAttribArray(dimsAttr)
        gl.glEnableVertexAttribArray(colorFAttr)
        gl.glEnableVertexAttribArray(colorSAttr)

        gl.glVertexAttribDivisor(offsetAttr, 1)
        gl.glVertexAttribDivisor(dimsAttr, 1)
        gl.glVertexAttribDivisor(colorFAttr, 1)
        gl.glVertexAttribDivisor(colorSAttr, 1)

        stride = (3+3+4+4) * ctypes.sizeof(ctypes.c_float)
        gl.glVertexAttribPointer(
            offsetAttr, 3, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(0)
        )
        gl.glVertexAttribPointer(
            dimsAttr, 3, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float))
        )
        gl.glVertexAttribPointer(
            colorFAttr, 4, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(6*ctypes.sizeof(ctypes.c_float))
        )
        gl.glVertexAttribPointer(
            colorSAttr, 4, gl.GL_FLOAT, gl.GL_FALSE,
            stride, ctypes.c_void_p(10*ctypes.sizeof(ctypes.c_float))
        )
        self.u_window = gl.glGetUniformLocation(self.rect_program, "window")

        gl.glBindVertexArray(0)

    def add(self, pos, size, stroke_width, fill_color, stroke_color, zindex):
        self.configBuffer.push_row((
            *pos, zindex,
            *size, stroke_width,
            *fill_color, *stroke_color
        ))

    def render(self, window_size):
        gl.glUseProgram(self.rect_program)
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
