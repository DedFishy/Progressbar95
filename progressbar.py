import pygame
from floating_text import FloatingText
import utils
from segment import Colors, Segment, SegmentBreakParticles, color_to_sound
from fonts import fonts

class ProgressbarTrail:
    def __init__(self, location: tuple[int, int], image: pygame.Surface):
        self.image = image
        self.location = location
    def update(self, screen: pygame.Surface):
        screen.blit(self.image, self.location)

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

        self.win_target_position = utils.calculate_center_positioning(self.window_size, self.rect.size)
        self.win_target_position[1] -= self.window_size[1]/3

        self.targeted_position_speed_x = 16
        self.targeted_position_speed_y = 16
        self.previous_direction_x = 0
        self.previous_direction_y = 0

        self.update_percentage_surface()

    def update_percentage_surface(self):
        self.percentage_surface = fonts["progressbar-percentage"].render(str(self.progressbar_fill * 5) + "%", False, (255, 255, 255))

    def get_segment_rect(self):
        return pygame.Rect(self.rect.left + self.bezel[0], self.rect.top + self.rect.height - self.bezel[1] - self.segment_collision_bottom_margin, self.rect.width - self.bezel[0]*2, self.segment_collision_bottom_margin)

    def collect_segment(self, segment):

        self.collected_segments.append(segment)
        segment.progressbar_position = self.progressbar_fill
        segment.animate_collection(self)
        self.progressbar_fill += 1

    def render_precentage(self, screen: pygame.Surface):
        screen.blit(self.percentage_surface, utils.translate_coords(utils.calculate_center_positioning(self.rect.size, self.percentage_surface.get_size()), self.rect.topleft))


    def update(self, screen: pygame.Surface, segments: list[Segment], has_won: bool):
        segments_to_destroy = []
        segments_to_destroy_quietly = []
        segments_to_spawn = []
        text_to_spawn = []

        if has_won:
            direction_x = utils.difference_to_weighted_direction_factor(self.rect.left - self.win_target_position[0])
            direction_y = utils.difference_to_weighted_direction_factor(self.rect.top - self.win_target_position[1])
            if self.previous_direction_x != 0 and direction_x != self.previous_direction_x:
                self.targeted_position_speed_x -= 0.5
            if self.previous_direction_y != 0 and direction_y != self.previous_direction_y:
                self.targeted_position_speed_y -= 0.5
            self.previous_direction_x = direction_x
            self.previous_direction_y = direction_y
            self.rect.left += direction_x * self.targeted_position_speed_x
            self.rect.top += direction_y * self.targeted_position_speed_y
        else:
            mouse_pos = pygame.mouse.get_pos()
            mouse_presses = pygame.mouse.get_pressed(3)

            segment_rect = self.get_segment_rect()



            for segment in segments:
                if isinstance(segment, SegmentBreakParticles):
                    continue
                if not segment.progressbar_position > -1:
                    if segment.rect.top > self.window_size[1]:
                        segments_to_destroy_quietly.append(segment)
                    elif pygame.Rect.colliderect(segment_rect, segment.rect):

                        if self.progressbar_fill == 0 or pygame.Rect.colliderect(self.rect.move(self.progressbar_fill*segment.rect.w + self.bezel[0], 0), segment.rect) and self.progressbar_fill < 20:
                            if segment.color == Colors.BLUE:
                                self.collect_segment(segment)
                                text_to_spawn.append(FloatingText("5%", segment.rect.center))
                            elif segment.color == Colors.BLUEX2 or segment.color == Colors.BLUEX3:
                                segments_to_destroy_quietly.append(segment)

                                for _ in range(2 if segment.color == Colors.BLUEX2 else 3):
                                    added_segment = Segment(segment.rect.left, Colors.BLUE, segment.speed, segment.rect.top)
                                    added_segment.is_from_multiple = True
                                    segments_to_spawn.append(added_segment)
                                    self.collect_segment(added_segment)
                            elif segment.color == Colors.PINK:
                                segments_to_destroy_quietly.append(segment)
                                if self.progressbar_fill > 0:
                                    segments_to_destroy_quietly.append(self.collected_segments.pop())
                                    self.progressbar_fill -= 1

                            self.update_percentage_surface()

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

        return segments_to_destroy, segments_to_destroy_quietly, segments_to_spawn, text_to_spawn