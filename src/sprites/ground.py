import pygame as pg

from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT

pg.init()


class Ground(pg.sprite.Sprite):
    HEIGHT = 32

    COLOR = (117, 83, 46)

    def __init__(
        self,
        *groups
    ):
        self._layer = 1
        super().__init__(*groups)

        self.pos = pg.Vector2(0, WINDOW_HEIGHT - self.HEIGHT)
        self.is_game_over = False

        self.image = pg.Surface((WINDOW_WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update(self):
        if not self.is_game_over:
            pass
