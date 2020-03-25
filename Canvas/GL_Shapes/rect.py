import ctypes

from Canvas.GL_Shapes.shape import Shape_GL

RECT_VERTICES = (ctypes.c_float * 12)(
    0, 0,
    0, 1,
    1, 0,

    0, 1,
    1, 1,
    1, 0,
)


vertex_shader = """#version 330
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

fragment_shader = """#version 330
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


class Rect_GL(Shape_GL):
    def __init__(self):
        super().__init__(vertex_shader, fragment_shader, RECT_VERTICES)

        self._add_config_attrib("offset", 3)
        self._add_config_attrib("dimensions", 3)
        self._add_config_attrib("colorFill", 4)
        self._add_config_attrib("colorStroke", 4)

        self._finalise_config_attribs()

    def add(self, pos, size, stroke_width, fill_color, stroke_color, zindex):
        self._configBuffer.push_row((
            *pos, zindex,
            *size, stroke_width,
            *fill_color, *stroke_color
        ))
