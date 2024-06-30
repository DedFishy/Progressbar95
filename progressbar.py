from gc import collect
import pygame
import utils
from segment import Colors, Segment, SegmentBreakParticles

class Progressbar:
    def __init__(self, window_size: list[int]):
        self.progressbar = pygame.image.load("progressbar.png")

        self.bezel = (30, 26)

        self.segment_collision_bottom_margin = 1

        self.is_progressbar_grabbed = False
        self.progressbar_grabbed_offset = [0, 0]

        self.window_size = window_size

        rect_size = [380, 86]
        self.rect = pygame.Rect(*utils.calculate_center_positioning(window_size, rect_size), *rect_size)
        self.progressbar_grabbed_offset = [0, 0]
        self.progressbar_fill = 0
        self.collected_segments = []

    def get_segment_rect(self):
        return pygame.Rect(self.rect.left + self.bezel[0], self.rect.top + self.rect.height - self.bezel[1] - self.segment_collision_bottom_margin, self.rect.width - self.bezel[0]*2, self.segment_collision_bottom_margin)

    def collect_segment(self, segment):
        self.collected_segments.append(segment)
        segment.progressbar_position = self.progressbar_fill
        segment.animate_collection(self)
        self.progressbar_fill += 1

    def update(self, screen: pygame.Surface, segments: list[Segment]):
        mouse_pos = pygame.mouse.get_pos()
        mouse_presses = pygame.mouse.get_pressed(3)

        segment_rect = self.get_segment_rect()

        segments_to_destroy = []
        segments_to_destroy_quietly = []

        for segment in segments:
            if isinstance(segment, SegmentBreakParticles):
                continue
            if not segment.progressbar_position > -1:
                if pygame.Rect.colliderect(segment_rect, segment.rect):

                    if self.progressbar_fill == 0 or pygame.Rect.colliderect(self.rect.move(self.progressbar_fill*segment.rect.w + self.bezel[0], 0), segment.rect):
                        if segment.color == Colors.BLUE:
                            self.collect_segment(segment)
                        elif segment.color == Colors.BLUEX2 or segment.color == Colors.BLUEX3:
                            segments_to_destroy_quietly.append(segment)

                            for _ in range(2 if segment.color == Colors.BLUEX2 else 3):
                                added_segment = Segment(segment.rect.left, Colors.BLUE, segment.speed, segment.rect.top)
                                segments.append(added_segment)
                                self.collect_segment(added_segment)
                    else:
                        segments_to_destroy.append(segment)

        if mouse_presses[0] and not self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = True
            self.progressbar_grabbed_offset = [mouse_pos[0]-self.rect.left, mouse_pos[1]-self.rect.top]
        elif not mouse_presses[0] and self.is_progressbar_grabbed:
            self.is_progressbar_grabbed = False

        if self.is_progressbar_grabbed:
            self.rect.x = mouse_pos[0]-self.progressbar_grabbed_offset[0]
            self.rect.y = mouse_pos[1]-self.progressbar_grabbed_offset[1]

        screen.blit(self.progressbar, self.rect.topleft)

        return segments_to_destroy, segments_to_destroy_quietly