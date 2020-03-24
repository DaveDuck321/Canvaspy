import ctypes
from OpenGL import GL as gl


def glGenFramebuffer(n):
    framebuffer = ctypes.c_int(0)
    gl.glGenFramebuffers(n, ctypes.byref(framebuffer))
    return framebuffer.value


class Antialias():
    def __init__(self, width, height):
        self.__width, self.__height = width, height
        # Create a texture for framebuffer, 2x size of window for antialising
        # TODO: find a performant way to do this
        #       Multisample does not work for the circle
        self.screen_tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.screen_tex)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0, gl.GL_RGB,
            2*self.__width, 2*self.__height,
            0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None
        )

        # Framebuffer to draw to texture
        self.framebuffer = glGenFramebuffer(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
        gl.glFramebufferTexture2D(
            gl.GL_FRAMEBUFFER,
            gl.GL_COLOR_ATTACHMENT0,
            gl.GL_TEXTURE_2D,
            self.screen_tex, 0
        )

        # Bind window back to framebuffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def start(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
        # Correct viewport size for drawing
        gl.glViewport(0, 0, 2*self.__width, 2*self.__height)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def finalize(self):
        # Push from multibuffer to buffer
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, 0)
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self.framebuffer)

        gl.glBlitFramebuffer(
            0, 0, 2*self.__width, 2*self.__height,
            0, 0, self.__width, self.__height,
            gl.GL_COLOR_BUFFER_BIT, gl.GL_LINEAR
        )
        # Set viewport back to screen dimensions for normal drawing
        gl.glViewport(0, 0, self.__width, self.__height)
