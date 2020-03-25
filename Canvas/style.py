def convert_color(color):
    if isinstance(color, tuple) or isinstance(color, list):
        if min(color) < 0 or max(color) > 1:
            raise ValueError("Color must be within range 0.0--1.0")
        if len(color) == 3:
            return (*color, 1.0)
        if len(color) == 4:
            return color
    if isinstance(color, str):
        if color[0] == '#':
            color = color[1:]
            if len(color) == 3:
                return convert_color(tuple(
                    int(char+char, 16)/255 for char in color
                ))
            return convert_color(tuple(
                map(
                    lambda i: int(color[i:i+2], 16)/255,
                    range(0, len(color), 2)
                )
            ))
    raise TypeError("Invalid color", color)


class Style():
    def __init__(self, color):
        self.color = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = convert_color(color)


class FillStyle(Style):
    def __init__(self, color):
        super().__init__(color)


class StrokeStyle(Style):
    def __init__(self, color, width=1):
        self.width = width
        super().__init__(color)


LineStyle = StrokeStyle

BLACK_STROKE = StrokeStyle((0, 0, 0), 1)
