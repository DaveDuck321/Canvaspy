import time

import tkinter
from pyopengltk import OpenGLFrame

from Canvas.surface import Surface
from Canvas import style
from Canvas.settings import Settings


class Canvas(OpenGLFrame):
    def __init__(self, root, **kwargs):
        self.surface = None
        super(Canvas, self).__init__(root, **kwargs)

    def initgl(self):
        """Initalize gl states when the frame is created"""
        print("Ran init")
        if self.surface is None:
            self.surface = Surface((self.width, self.height))

        self.start = time.time()-0.01
        self.nframes = 0

    def redraw(self):
        """Render a single frame"""
        # self.surface.add_rect((0, 0), (0.5, 0.5), Settings(fill=style.BLACK))
        self.surface.render()

        tm = time.time() - self.start
        self.nframes += 1
        print("fps", self.nframes / tm, end="\r")

    def tkResize(self, evt):
        self.width, self.height = evt.width, evt.height
        if self.surface is not None:
            self.surface.resize((self.width, self.height))

    # Drawing shapes
    def draw_line(self, pos1, pos2, settings=Settings(fill=style.BLACK)):
        raise NotImplementedError()

    def draw_rect(self, pos, size, settings=Settings(fill=style.BLACK)):
        raise NotImplementedError()

    def draw_circle(self, pos, r, settings=Settings(fill=style.BLACK)):
        raise NotImplementedError()

    def draw_arc(
        self, pos, r, start_angle, end_angle,
        clockwise=True,
        settings=Settings(fill=style.BLACK)
    ):
        pass

    # Drawing text
    def draw_text(self, text, pos, max_width=0):
        raise NotImplementedError()

    def measure_text(self, text):
        raise NotImplementedError()


if __name__ == '__main__':
    root = tkinter.Tk()
    app = Canvas(root, width=500, height=500)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.mainloop()
