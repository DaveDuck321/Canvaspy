import ctypes

from Canvas.GL_Shapes.shape import Shape_GL

LINE_VERTICES = (ctypes.c_float * 12)(
    0, -1,
    0, 1,
    1, -1,

    0, 1,
    1, 1,
    1, -1
)


vertex_shader = """#version 330
in vec2 position;

in vec2 startPos;
in vec2 endPos;
in float width;
in vec4 color;

uniform vec2 window;

out vec4 fragColor;

void main() {
    vec3 direction = vec3(endPos - startPos, 0.0f);
    vec3 perp = normalize(cross(direction, vec3(0.0f, 0.0f, 1.0f)));

    vec3 onLine = direction*position.x + 0.5f*width*perp*position.y;
    gl_Position = vec4(
        2.0f * (onLine.x+startPos.x)/window.x - 1.0f,
        1.0f - 2.0f * (onLine.y+startPos.y)/window.y,
        0.0f, 1.0f
    );
    fragColor = color;
}
"""

fragment_shader = """#version 330
in vec4 fromEdge;

in vec4 fragColor;

out vec4 color;
void main() {
    color = fragColor;
}
"""


class Line_GL(Shape_GL):
    def __init__(self):
        super().__init__(vertex_shader, fragment_shader, LINE_VERTICES)

        self._add_config_attrib("startPos", 2)
        self._add_config_attrib("endPos", 2)
        self._add_config_attrib("width", 1)
        self._add_config_attrib("color", 4)

        self._finalise_config_attribs()

    def add(self, start, end, width, color):
        self._configBuffer.push_row((
            *start, *end,
            width, *color
        ))
