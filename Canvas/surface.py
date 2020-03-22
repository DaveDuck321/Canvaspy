from OpenGL import GL as gl

from Canvas.GL_Shapes.rect import Rect_GL
from Canvas.GL_Shapes.circle import Circle_GL
from Canvas.GL_Shapes.line import Line_GL

from itertools import count


class Surface():
    def __init__(self, window_size):
        self.__width, self.__height = window_size

        self.counter = count(1)
        self.initgl()

        self.line = Line_GL()
        self.circle = Circle_GL()
        self.rect = Rect_GL()

    def initgl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glEnable(gl.GL_MULTISAMPLE)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
        gl.glClearColor(1.0, 1.0, 0.0, 1.0)

    def resize(self, window_size):
        self.__width, self.__height = window_size
        gl.glViewport(0, 0, self.__width, self.__height)

    def add_rect(self, pos, size, settings):
        pass

    def add_circle(self, pos, r, settings):
        raise NotImplementedError()

    def add_arc(self, pos, r, start_angle, end_angle, clockwise, settings):
        pass

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.line.render((self.__width, self.__height))
        self.circle.render((self.__width, self.__height))
        self.rect.render((self.__width, self.__height))

        self.counter = count(1)
