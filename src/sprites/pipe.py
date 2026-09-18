import pygame as pg

from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT

pg.init()


class Pipe(pg.sprite.Sprite):
    WIDTH = 96

    GAP_SIZE = 128
    GAP_MARGIN_SIZE = 48

    SPAWN_SECS = 2.5
    INIT_XPOS = WINDOW_WIDTH
    SPEED = 2
    DIRECTION = -1

    def __init__(
        self,
        ypos: float,
        height: float,
        *groups
    ):
        super().__init__(*groups)

        self.pos = pg.Vector2(self.INIT_XPOS, ypos)

        self.image = pg.Surface((self.WIDTH, height))
        self.image.fill((48, 161, 48))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def move(self):
        self.pos.x += self.DIRECTION * self.SPEED

    def check_despawn(self):
        if self.DIRECTION > 0:
            if self.pos.x > WINDOW_WIDTH:
                self.kill()
                return

        if self.pos.x + self.WIDTH < 0:
            self.kill()
            return

    def update(self):
        self.move()
        self.check_despawn()

        self.rect.x, self.rect.y = self.pos
