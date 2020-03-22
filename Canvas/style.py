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
    raise ValueError("Invalid color")


class Style():
    def __init__(self, color=(0, 0, 0)):
        self.__color = color

    def __hash__(self):
        return 0

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = convert_color(color)


BLACK = Style((0, 0, 0))
WHITE = Style((1, 1, 1))
RED = Style((1, 0, 0))
GREEN = Style((0, 1, 0))
BLUE = Style((0, 0, 1))
CYAN = Style((0, 1, 1))
YELLOW = Style((1, 1, 0))
MAGENTA = Style((1, 0, 1))
