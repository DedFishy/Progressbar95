import pygame
import colors
import random

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

color_list = [Colors.BLUE, Colors.YELLOW, Colors.BLUEX2, Colors.BLUEX3, Colors.PINK, Colors.GRAY, Colors.RED]
weights =    [100,         75,            20,            10,            60,          50,          20]

class Segment:
    def __init__(self, pos_x, color=None):
        if not color:
            color = random.choices(color_list, weights)[0]
        self.color = color
        self.rgb = color_to_rgb[color]
        self.pos = [pos_x, -10]
    def update():