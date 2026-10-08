import pygame as pg

from ..constants import PATH_FONT_SCORE, WINDOW_WIDTH

pg.init()


class ScoreDisplay(pg.sprite.Sprite):
    CENTER_X = WINDOW_WIDTH / 2
    CENTER_Y = 64

    COLOR = (255, 255, 0)

    IDLE_SIZE = 64
    BOUNCE_SIZE = 96
    BOUNCE_EASE_COEF = 0.1

    def __init__(
        self,
        score_init: int = 0,
        *groups
    ):
        super().__init__(*groups)

        self.value = score_init
        self.size = self.IDLE_SIZE

        font = pg.font.Font(PATH_FONT_SCORE, self.size)
        self.image = font.render(str(self.value), True, self.COLOR)
        self.pos = self.center_pos()

    def increment(self):
        self.value += 1
        self.size = self.BOUNCE_SIZE

    def reset(self):
        self.value = 0
        self.size = self.BOUNCE_SIZE

    def render_text(self):
        self.size -= (self.size - self.IDLE_SIZE) * self.BOUNCE_EASE_COEF
        self.size = round(self.size)

        font = pg.font.Font(PATH_FONT_SCORE, self.size)
        self.image = font.render(str(self.value), True, self.COLOR)

    def center_pos(self):
        return (
            self.CENTER_X - self.image.get_width() / 2,
            self.CENTER_Y - self.image.get_height() / 2
        )

    def update(self):
        self.render_text()
        self.pos = self.center_pos()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
