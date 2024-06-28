import pygame
import utils

class Progressbar:
    def __init__(self, window_size: list[int]):
        self.progressbar = pygame.image.load("progressbar.png")

        self.is_progressbar_grabbed = False
        self.progressbar_grabbed_offset = [0, 0]
        self.rect_size = [380, 86]
        self.window_size = window_size
        self.rect_pos = utils.calculate_center_positioning(window_size, self.rect_size)
        self.progressbar_grabbed_offset = [0, 0]

    def update(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        mouse_presses = pygame.mouse.get_pressed(3)

        if mouse_presses[0] and not self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = True
            self.progressbar_grabbed_offset = [mouse_pos[0]-self.rect_pos[0], mouse_pos[1]-self.rect_pos[1]]
        elif not mouse_presses[0] and self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = False

        if self.is_progressbar_grabbed:
            self.rect_pos = [mouse_pos[0]-self.progressbar_grabbed_offset[0], mouse_pos[1]-self.progressbar_grabbed_offset[1]]

        screen.blit(self.progressbar, self.rect_pos)