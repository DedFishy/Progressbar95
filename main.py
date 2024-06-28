import pygame
import utils
from colors import transparent
from progressbar import Progressbar

pygame.init()


info = pygame.display.Info()
width, height = info.current_w, info.current_h

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
done = False
dark_red = (139, 0, 0)

hwnd = pygame.display.get_wm_info()["window"]
utils.config_win32_window(hwnd)

progressbar = Progressbar([width, height])

clock = pygame.time.Clock()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(transparent)

    progressbar.update(screen)


    pygame.display.update()

    clock.tick(120)