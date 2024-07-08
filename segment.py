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

color_to_sound = {
    Colors.BLUE: pygame.mixer.Sound("collect_blue.mp3"),
    Colors.YELLOW: pygame.mixer.Sound("collect_yellow.mp3")
}
break_sound = pygame.mixer.Sound("break.mp3")
collect_multiple_sound = pygame.mixer.Sound("collect_blue_multiple.mp3")

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

font = pygame.Font("progresspixel.ttf", 15)

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

        self.text: pygame.Surface | None = None

        if color == Colors.BLUEX2:
            self.text = font.render(" 2 x", False, (255, 255, 255))
        if color == Colors.BLUEX3:
            self.text = font.render(" 3 x", False, (255, 255, 255))

        self.on_collected = None

        self.targeted_position = 0
        self.current_position = 0
        self.targeted_position_speed = 8
        self.targeted_position_translation = lambda x: [0, 0]
        self.previous_direction = 0
        self.is_animating = False

        self.has_played_collection = False

        self.is_from_multiple = False
    def destroy(self):
        break_sound.play()
        return SegmentBreakParticles(list(self.rect.topleft), self.color)

    def animate_collection(self, progressbar):
        self.targeted_position = self.rect.width*self.progressbar_position
        self.current_position = self.rect.left - progressbar.rect.left - progressbar.bezel[0]
        self.targeted_position_translation = lambda x: [
            progressbar.rect.left + progressbar.bezel[0] + x,
            progressbar.rect.top + progressbar.bezel[1]]

        self.is_animating = True

    def update(self, screen: pygame.Surface, progressbar):
        if self.is_animating:
            direction = utils.difference_to_direction_factor(self.current_position - self.targeted_position)
            if self.previous_direction != 0 and direction != self.previous_direction:
                self.targeted_position_speed -= 0.5
            self.previous_direction = direction
            self.current_position += direction * self.targeted_position_speed
            self.rect.topleft = self.targeted_position_translation(self.current_position)
            if self.current_position == self.targeted_position:
                if not self.targeted_position_speed == 0:
                    self.current_position += -self.previous_direction * self.targeted_position_speed
                self.is_animating = False
        elif self.progressbar_position > -1:
            if self.on_collected != None:
                self.on_collected()
            if not self.has_played_collection:
                self.has_played_collection = True
                if self.is_from_multiple:
                    collect_multiple_sound.play()
                elif self.color in color_to_sound.keys():
                    color_to_sound[self.color].play()
            self.rect.x = progressbar.rect.left + progressbar.bezel[0] + (self.rect.size[0] * self.progressbar_position)
            self.rect.y = progressbar.rect.top + progressbar.bezel[1]
        else:
            self.rect.y += self.speed

        pygame.draw.rect(screen, self.rgb, self.rect)
        if self.text:
            screen.blit(self.text, [self.rect.right, self.rect.centery - self.text.height/2])