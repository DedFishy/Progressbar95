import pygame
import colors
import random
import utils

class Colors:
    BLUE=0
    YELLOW=1
    BLUEX2=2
    BLUEX3=3
    PINK=4
    GRAY=5
    RED=6

color_to_rgb = {
    Colors.BLUE: colors.blue,
    Colors.YELLOW: colors.yellow,
    Colors.BLUEX2: colors.lightblue,
    Colors.BLUEX3: colors.lightblue,
    Colors.PINK: colors.pink,
    Colors.GRAY: colors.gray,
    Colors.RED: colors.red
}

color_list =     [Colors.BLUE, Colors.YELLOW, Colors.BLUEX2, Colors.BLUEX3, Colors.PINK, Colors.GRAY, Colors.RED]
weights =        [100,         75,            20,            10,            60,          50,          20]
segment_speeds = [2,           2,             5,             4,             4,           2,           2]
segment_speed_variance = min(segment_speeds) - 1

class Segment:
    def __init__(self, pos_x, color=None, speed=None):
        if not color:
            color = random.choices(color_list, weights)[0]
        if not speed:
            speed_middle = segment_speeds[color_list.index(color)]
            speed = random.randint(speed_middle-segment_speed_variance, speed_middle+segment_speed_variance)
        self.color = color
        self.speed = speed
        size = [15, 32]
        self.rgb = color_to_rgb[color]

        self.rect = pygame.Rect(pos_x, -size[1], *size)

        self.progressbar_position = -1 # if it's > -1, we're in the progress bar

    def update(self, screen: pygame.Surface, progressbar):

        if self.progressbar_position > -1:
            self.rect.x = progressbar.rect.left + progressbar.bezel[0] + (self.rect.size[0] * self.progressbar_position)
            self.rect.y = progressbar.rect.top + progressbar.bezel[1]
        else:
            self.rect.y += self.speed

        pygame.draw.rect(screen, self.rgb, self.rect)