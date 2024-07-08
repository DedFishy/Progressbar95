import pygame

TEXT_FRAMES = [
    "",
    "·",
    "<>",
    "< >"
    "< T >"
    "  T  "
]
FRAME_TIME = 5
MOVE_SPEED = 10

class FloatingText:
    def __init__(self, text: str, position: tuple[int, int]):
        self.current_frame = -1
        self.current_frame_time = 0

        self.current_frame_render: pygame.Surface = pygame.Surface([0, 0])

        self.font = pygame.font.Font("progresspixel-bold.ttf", 10)

        self.position = list(position)

    def update(self, screen: pygame.Surface):
        self.current_frame_time -= 1
        if self.current_frame_time <= 0:
            self.current_frame += 1
            self.current_frame_time = FRAME_TIME
            if self.current_frame >= len(TEXT_FRAMES):
                return False
            self.current_frame_render = self.font.render(TEXT_FRAMES[self.current_frame], False, (255, 255, 255))
        self.position[1] -= MOVE_SPEED
        screen.blit(self.current_frame_render, self.position)

