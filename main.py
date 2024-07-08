import time
from turtle import window_height
import pygame

pygame.init()

from floating_text import FloatingText
import utils
from colors import transparent
from progressbar import Progressbar, ProgressbarTrail
import random
from segment import Segment, SegmentBreakParticles

music = pygame.mixer.Sound("music.mp3")
music.set_volume(0.3)
music.play(-1)

info = pygame.display.Info()
width, height = info.current_w, info.current_h

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
done = False
dark_red = (139, 0, 0)

hwnd = pygame.display.get_wm_info()["window"]
utils.config_win32_window(hwnd)

progressbar = Progressbar([width, height])
progressbartrail: list[ProgressbarTrail] = []
progressbartrail_max_len = 20
segments: list[Segment] = []
segment_particles: list[SegmentBreakParticles] = []
text: list[FloatingText] = []

segment_timer_range = (10, 100)

segment_time_remaining = 0

segment_spawn_queue_time = 20
segment_spawn_queue_remaining = 0
segment_spawn_queue = []

clock = pygame.time.Clock()

has_won = False
win_close_timer = 300

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    segment_time_remaining -= 1

    if segment_time_remaining <= 0 and not has_won:
        segments.append(Segment(random.randint(0, width)))
        segment_time_remaining = random.randint(*segment_timer_range)

    screen.fill(transparent)

    if not has_won:
        progressbartrail.append(ProgressbarTrail(progressbar.rect.topleft, progressbar.progressbar))
        for trail in progressbartrail:
            trail.update(screen)
        while len(progressbartrail) > progressbartrail_max_len:
            del progressbartrail[0]

    segments_to_destroy, segments_to_destroy_quietly, segments_to_spawn, text_to_spawn, crashed = progressbar.update(screen, segments, has_won)

    for segment in segments_to_destroy_quietly:
        if segment in segments_to_destroy: segments_to_destroy.remove(segment)
        if segment in segments: segments.remove(segment)
    for segment in segments_to_destroy:
        segment_particles.append(segment.destroy())
        segments.remove(segment)

    segment_spawn_queue.extend(segments_to_spawn)

    text.extend(text_to_spawn)

    if len(segment_spawn_queue) > 0:
        segment_spawn_queue_remaining -= 1
        if segment_spawn_queue_remaining <= 0:
            segment_spawn_queue_remaining = segment_spawn_queue_time
            segments.append(segment_spawn_queue.pop(0))
    else:
        segment_spawn_queue_remaining = 0

    for segment in segments:
        result = segment.update(screen, progressbar)
        if result == False:
            segments.remove(segment)

    for segment in segment_particles:
        result = segment.update(screen)
        if result == False:
            segment_particles.remove(segment)

    for floating_text in text:
        result = floating_text.update(screen)
        if result == False:
            text.remove(floating_text)

    progressbar.render_precentage(screen)

    if progressbar.progressbar_fill >= 20 and not has_won:
        unused_segments = []
        for segment in segments:
            if segment.progressbar_position == -1:
                unused_segments.append(segment)
        for segment in unused_segments:
            segments.remove(segment)
        has_won = True
        music.stop()
        pygame.mixer.Sound("win.mp3").play()

    if has_won:
        win_close_timer -= 1
        if win_close_timer <= 0:
            done = True

    if crashed:
        pygame.mixer.Sound("bsod.mp3").play()
        image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        image.fill((255, 0, 0, 100))
        screen.blit(image, [0, 0])
        pygame.display.update()
        time.sleep(2)
        utils.raise_bsod()
        done = True
        break

    pygame.display.update()

    clock.tick(120)