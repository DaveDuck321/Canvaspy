from ctypes import sizeof, c_float, c_void_p

from OpenGL import GL as gl
from OpenGL.GL import shaders

from Canvas.buffer import Buffer


class Shape_GL():
    def __init__(self, vertex_shader, fragment_shader, vertices):
        self.__config_attribs = []
        self.__config_size = 0

        self.__initgl(vertex_shader, fragment_shader, vertices)
        self.u_window = gl.glGetUniformLocation(self.program, "window")

    def __initgl(self, vertex_shader, fragment_shader, vertices):
        self.program = shaders.compileProgram(
            shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
        )
        gl.glUseProgram(self.program)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.glConfigBuffer = gl.glGenBuffers(1)
        verticesBuffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, verticesBuffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            sizeof(vertices),
            vertices,
            gl.GL_STATIC_DRAW
        )

        positionAttr = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(positionAttr)
        gl.glVertexAttribPointer(
            positionAttr, 2, gl.GL_FLOAT, gl.GL_FALSE,
            2*sizeof(c_float), c_void_p(0)
        )

    def _add_config_attrib(self, name, size):
        location = gl.glGetAttribLocation(self.program, name)
        gl.glEnableVertexAttribArray(location)
        gl.glVertexAttribDivisor(location, 1)

        self.__config_size += size
        self.__config_attribs.append((location, size))

    def _finalise_config_attribs(self):
        pointer = 0
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.glConfigBuffer)
        for location, size in self.__config_attribs:
            gl.glVertexAttribPointer(
                location, size, gl.GL_FLOAT, gl.GL_FALSE,
                self.__config_size, c_void_p(pointer*sizeof(c_float))
            )
            pointer += size

        self.configBuffer = Buffer(c_float, pointer)

    def add(self):
        raise NotImplementedError()

    def render(self, window_size):
        b_size, d_data = self.configBuffer.get_buffer()
        if b_size == 0:
            return

        gl.glUseProgram(self.program)
        gl.glUniform2f(self.u_window, *window_size)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.glConfigBuffer)

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
