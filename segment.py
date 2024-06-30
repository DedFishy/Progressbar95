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

particle_count = 5
particle_size = 5
particle_size_variance = 2
particle_size_factor = 2 # ratio between width and height
particle_angular_velocity = 1
particle_velocity = 2
particle_lifetime = 40
particle_lifetime_variance = 10

class SegmentBreakParticles:
    def __init__(self, pos, color):
        self.particles = []

        for _ in range(particle_count):
            particle = {}
            particle_width = random.randint(particle_size-particle_size_variance, particle_size+particle_size_variance)
            particle["surface"] = pygame.Surface(
                (
                    particle_width,
                    particle_width * particle_size_factor
                )
            )
            particle["surface"].set_colorkey((0, 0, 0))
            particle["surface"].fill(color_to_rgb[color])
            particle["pos"] = pos.copy()
            particle["velocity"] = [random.randint(-particle_velocity, particle_velocity), random.randint(-particle_velocity, particle_velocity)]
            particle["angle"] = random.randint(0, 360)
            particle["angular_velocity"] = random.choice([-1, 1]) * particle_angular_velocity
            particle["lifetime"] = random.randint(particle_lifetime-particle_lifetime_variance, particle_lifetime+particle_lifetime_variance)
            self.particles.append(particle)


    def update(self, screen: pygame.Surface):
        if len(self.particles) == 0:
            return False
        for particle in self.particles:
            particle["lifetime"] -= 1
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                continue
            particle["pos"][0] += particle["velocity"][0]
            particle["pos"][1] += particle["velocity"][1]
            particle["angle"] += particle["angular_velocity"]
            particle["angle"] %= 360
            screen.blit(pygame.transform.rotate(particle["surface"], particle["angle"]), particle["pos"])

class Segment:
    def __init__(self, pos_x, color=None, speed=None, pos_y=None):
        if color == None:
            color = random.choices(color_list, weights)[0]
        if speed == None:
            speed_middle = segment_speeds[color_list.index(color)]
            speed = random.randint(speed_middle-segment_speed_variance, speed_middle+segment_speed_variance)
        self.color = color
        self.speed = speed
        size = [16, 32]
        self.rgb = color_to_rgb[color]

        self.rect = pygame.Rect(pos_x, -size[1] if pos_y == None else pos_y, *size)

        self.progressbar_position = -1 # if it's > -1, we're in the progress bar

        self.targeted_position = 0
        self.current_position = lambda: 0
        self.targeted_position_speed = 1
        self.targeted_position_current_speed = 0
        self.targeted_position_translation = None
        self.is_animating = False

    def destroy(self):
        return SegmentBreakParticles(list(self.rect.topleft), self.color)

    def animate_collection(self, progressbar):
        self.targeted_position = self.rect.width*self.progressbar_position
        self.current_position = lambda: self.rect.left - progressbar.rect.left - progressbar.bezel[0]
        self.targeted_position_translation = lambda x: [
            progressbar.rect.left + progressbar.bezel[0] + x,
            progressbar.rect.top + progressbar.bezel[1]]

        self.is_animating = True

    def update(self, screen: pygame.Surface, progressbar):
        if self.is_animating:
            self.current_position = utils.difference_to_direction_factor(self.current_position() - self.targeted_position)
        elif self.progressbar_position > -1:
            self.rect.x = progressbar.rect.left + progressbar.bezel[0] + (self.rect.size[0] * self.progressbar_position)
            self.rect.y = progressbar.rect.top + progressbar.bezel[1]
        else:
            self.rect.y += self.speed

        pygame.draw.rect(screen, self.rgb, self.rect)