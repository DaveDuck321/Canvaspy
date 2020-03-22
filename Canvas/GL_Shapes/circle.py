import ctypes

from Canvas.GL_Shapes.shape import Shape_GL


BOUNDING_VERTICES = (ctypes.c_float * 12)(
    -1, -1,
    -1, 1,
    1, -1,

    -1, 1,
    1, 1,
    1, -1
)


vertex_shader = """#version 330
in vec2 position;

in vec3 center;
in vec2 radii;  //x: radius, y: stroke width
in vec4 colorFill;
in vec4 colorStroke;

uniform vec2 window;

out vec2 fragRadii;
out vec4 fragColorF;
out vec4 fragColorS;
out vec2 toCenter;

void main() {
    gl_Position = vec4(
        2.0f * (position.x*radii.x+center.x)/window.x - 1.0f,
        1.0f - 2.0f * (position.y*radii.x+center.y)/window.y,
        -center.z, 1.0
    );
    toCenter = vec2(
        radii.x*position.x,
        radii.x*position.y
    );
    fragRadii = radii;
    fragColorF = colorFill;
    fragColorS = colorStroke;
}
"""

fragment_shader = """#version 330
in vec2 toCenter;

in vec2 fragRadii;
in vec4 fragColorF;
in vec4 fragColorS;

out vec4 color;
void main() {
    float r = length(toCenter);
    if(r <= fragRadii.x) {
        if(r >= fragRadii.x-fragRadii.y)
            color = fragColorS;
        else
            color = fragColorF;
    } else
        color = vec4(0, 0, 0, 0);
}
"""


class Circle_GL(Shape_GL):
    def __init__(self):
        super().__init__(vertex_shader, fragment_shader, BOUNDING_VERTICES)

        self._add_config_attrib("center", 3)
        self._add_config_attrib("radii", 2)
        self._add_config_attrib("colorFill", 4)
        self._add_config_attrib("colorStroke", 4)

        self._finalise_config_attribs()

    def add(self, pos, radius, stroke_width, fill_color, stroke_color, zindex):
        self.configBuffer.push_row((
            *pos, zindex,
            radius, stroke_width,
            *fill_color, *stroke_color
        ))
