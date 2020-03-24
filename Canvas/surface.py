from OpenGL import GL as gl

from Canvas.GL_Shapes.rect import Rect_GL
from Canvas.GL_Shapes.circle import Circle_GL
from Canvas.GL_Shapes.line import Line_GL

from Canvas.antialias import Antialias

from itertools import count


class Surface():
    def __init__(self, window_size):
        self.__width, self.__height = window_size

        self.counter = count(1)
        self.initgl()

        self.aa = Antialias(self.__width, self.__height)

        self.line = Line_GL()
        self.circle = Circle_GL()
        self.rect = Rect_GL()

    def initgl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glClearColor(1.0, 1.0, 0.0, 1.0)

    def resize(self, window_size):
        self.__width, self.__height = window_size
        gl.glViewport(0, 0, self.__width, self.__height)

    def add_line(self, start, end):
        self.line.add(start, end, 2, (0, 0, 0, 1))

    def add_rect(self, pos, size):
        self.rect.add(pos, size, 3, (1, 0, 0, 1), (0, 0, 0, 1), 0)

    def add_circle(self, pos, r):
        self.circle.add(pos, r, 3, (0, 1, 0, 1), (0, 0, 0, 1), 0)

    def add_arc(self, pos, r, start_angle, end_angle, clockwise):
        raise NotImplementedError()

    def render(self, antialias=True):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        if antialias:
            self.aa.start()

        self.line.render((self.__width, self.__height))
        self.circle.render((self.__width, self.__height))
        self.rect.render((self.__width, self.__height))

        if antialias:
            self.aa.finalize()
