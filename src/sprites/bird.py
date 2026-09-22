import pygame as pg

pg.init()


class Bird(pg.sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32

    COLOR = (255, 240, 189)

    FLAP_STRENGTH = -10
    GRAVITY = 0.75
    TERMINAL_VEL = 24

    def __init__(
        self,
        pos: tuple[float, float],
        *groups
    ):
        super().__init__(*groups)

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0, 0)

        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        self.current_keys = pg.key.get_pressed()
        self.last_keys = pg.key.get_pressed()

    def is_pressed(self, key: int) -> bool:
        self.current_keys = pg.key.get_pressed()

        if self.current_keys[key] and not self.last_keys[key]:
            return True

        return False

    def move(self):
        if self.is_pressed(pg.K_SPACE):
            self.vel.y = self.FLAP_STRENGTH

        self.vel.y += self.GRAVITY
        self.vel.y = max(min(self.vel.y, self.TERMINAL_VEL), -self.TERMINAL_VEL)

        self.pos += self.vel

    def update(self):
        self.move()

        self.last_keys = self.current_keys
        self.rect.x, self.rect.y = self.pos
