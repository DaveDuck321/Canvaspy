import sdl2
import ctypes
from Canvas.surface import Surface


def main():
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(
        sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
        sdl2.SDL_GL_CONTEXT_PROFILE_CORE
    )
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, 4)
    sdl2.SDL_GL_SetSwapInterval(1)

    DISPLAY_DIMENSIONS = (640, 480)
    window = sdl2.SDL_CreateWindow(
        b"Hello world",
        sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
        *DISPLAY_DIMENSIONS,
        sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_OPENGL
    )
    sdl2.SDL_GL_CreateContext(window)
    surface = Surface(DISPLAY_DIMENSIONS)

    running = True
    event = sdl2.SDL_Event()
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False

        surface.render()
        sdl2.SDL_GL_SwapWindow(window)

    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


if __name__ == '__main__':
    main()
