from OpenGL import GL as gl

from Canvas.GL_Shapes.rect import Rect_GL
from Canvas.GL_Shapes.circle import Circle_GL
from Canvas.GL_Shapes.line import Line_GL
from Canvas.style import Style, StrokeStyle, FillStyle, BLACK_STROKE

from Canvas.antialias import Antialias

from itertools import count


def separate_styles(styles):
    fill_style, stroke_style = None, None

    for style in styles:
        if isinstance(style, StrokeStyle):
            # Throw error if stroke style is already set
            if stroke_style is not None:
                raise ValueError("Multiple stroke styles received", styles)
            stroke_style = style
        else:  # Not a stroke style -- must be a fill style
            # Throw error if fill style is already set
            if fill_style is not None:
                raise ValueError("Multiple fill styles received", styles)
            if isinstance(style, FillStyle):
                # Everythings ok, record this fill style
                fill_style = style
            else:
                # Attempt to convert argument into a valid style
                fill_style = FillStyle(style)

    # If neither styles are set, choose a default style
    if fill_style is None and stroke_style is None:
        stroke_style = StrokeStyle((0, 0, 0))
    # Fill is not required, choose an empty style
    if fill_style is None:
        fill_style = FillStyle((0, 0, 0, 0))
    # Stroke is not required, choose an empty style
    if stroke_style is None:
        stroke_style = StrokeStyle((0, 0, 0, 0), 0)

    return fill_style, stroke_style


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
        self.aa.resize(*window_size)
        gl.glViewport(0, 0, self.__width, self.__height)

    def add_line(self, start, end, style=BLACK_STROKE):
        if isinstance(style, StrokeStyle):
            self.line.add(start, end, style.width, style.color)
        elif isinstance(style, Style):
            self.line.add(start, end, 1, style.color)
        else:
            style = StrokeStyle(style)
            self.line.add(start, end, style.width, style.color)

    def add_rect(self, pos, size, *styles):
        fill_style, stroke_style = separate_styles(styles)
        self.rect.add(
            pos, size, stroke_style.width,
            fill_style.color, stroke_style.color,
            0
        )

    def add_circle(self, pos, r, *styles):
        fill_style, stroke_style = separate_styles(styles)
        self.circle.add(
            pos, r, stroke_style.width,
            fill_style.color, stroke_style.color,
            0
        )

    def add_arc(self, pos, r, start_angle, end_angle, clockwise, *styles):
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
