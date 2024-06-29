import pygame
import utils
from segment import Segment

class Progressbar:
    def __init__(self, window_size: list[int]):
        self.progressbar = pygame.image.load("progressbar.png")

        self.bezel = (30, 26)

        self.is_progressbar_grabbed = False
        self.progressbar_grabbed_offset = [0, 0]

        self.window_size = window_size

        rect_size = [380, 86]
        self.rect = pygame.Rect(*utils.calculate_center_positioning(window_size, rect_size), *rect_size)
        self.progressbar_grabbed_offset = [0, 0]
        self.progressbar_fill = 0

    def update(self, screen: pygame.Surface, segments: list[Segment]):
        mouse_pos = pygame.mouse.get_pos()
        mouse_presses = pygame.mouse.get_pressed(3)

        for segment in segments:
            if not segment.progressbar_position > -1:
                if pygame.Rect.colliderect(self.rect, segment.rect):

                    if self.progressbar_fill > 0 and pygame.Rect.colliderect(self.rect.move(self.progressbar_fill*segment.rect.w + self.bezel[0], 0), segment.rect):

                        segment.progressbar_position = self.progressbar_fill
                        self.progressbar_fill += 1

        if mouse_presses[0] and not self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = True
            self.progressbar_grabbed_offset = [mouse_pos[0]-self.rect.left, mouse_pos[1]-self.rect.top]
        elif not mouse_presses[0] and self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = False

        if self.is_progressbar_grabbed:
            self.rect.x = mouse_pos[0]-self.progressbar_grabbed_offset[0]
            self.rect.y = mouse_pos[1]-self.progressbar_grabbed_offset[1]

        screen.blit(self.progressbar, self.rect.topleft)