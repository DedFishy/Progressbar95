import pygame
import utils
from colors import transparent
from progressbar import Progressbar
import random
from segment import Segment, SegmentBreakParticles

pygame.init()


info = pygame.display.Info()
width, height = info.current_w, info.current_h

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
done = False
dark_red = (139, 0, 0)

hwnd = pygame.display.get_wm_info()["window"]
utils.config_win32_window(hwnd)

progressbar = Progressbar([width, height])
segments: list[Segment] = []
segment_particles: list[SegmentBreakParticles] = []

segment_timer_range = (10, 100)

segment_time_remaining = 0

clock = pygame.time.Clock()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    segment_time_remaining -= 1

    if segment_time_remaining <= 0:
        segments.append(Segment(random.randint(0, width)))
        segment_time_remaining = random.randint(*segment_timer_range)

    screen.fill(transparent)

    segments_to_destroy, segments_to_destroy_quietly = progressbar.update(screen, segments)

    for segment in segments_to_destroy_quietly:
        if segment in segments_to_destroy: segments_to_destroy.remove(segment)
        if segment in segments: segments.remove(segment)
    for segment in segments_to_destroy:
        segment_particles.append(segment.destroy())
        segments.remove(segment)


    for segment in segments:
        result = segment.update(screen, progressbar)
        if result == False:
            segments.remove(segment)

    for segment in segment_particles:
        result = segment.update(screen)
        if result == False:
            segment_particles.remove(segment)

    pygame.display.update()

    clock.tick(120)
