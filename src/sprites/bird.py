import pygame as pg

pg.init()


class Bird(pg.sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32

    COLOR_DEFAULT = (255, 240, 189)
    COLOR_DEAD = (255, 89, 89)
    COLOR_READY = (255, 143, 143)

    FLAP_KEY = pg.K_SPACE
    FLAP_STRENGTH = -10
    GRAVITY = 0.75
    TERMINAL_VEL = 24

    INIT_X = 128
    INIT_Y = 256
    INIT_Y_VEL = -10

    def __init__(
        self,
        *groups
    ):
        self._layer = 2
        super().__init__(*groups)

        self.pos = pg.Vector2(self.INIT_X, self.INIT_Y)
        self.vel = pg.Vector2(0, self.INIT_Y_VEL)
        self.is_game_over = False

        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR_DEFAULT)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        self.current_keys = pg.key.get_pressed()
        self.last_keys = pg.key.get_pressed()

    def is_pressed(self, key: int) -> bool:
        self.current_keys = pg.key.get_pressed()

        if self.current_keys[key] and not self.last_keys[key]:
            return True

        return False

    def die(self):
        self.image.fill(self.COLOR_DEAD)

    def move(self):
        if self.is_pressed(self.FLAP_KEY):
            self.vel.y = self.FLAP_STRENGTH

        self.vel.y += self.GRAVITY
        self.vel.y = max(min(self.vel.y, self.TERMINAL_VEL), -self.TERMINAL_VEL)

        self.pos += self.vel

        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0

    def update(self):
        if self.is_game_over:
            self.image.fill(self.COLOR_DEAD)
        else:
            self.image.fill(self.COLOR_DEFAULT)
            self.move()

        self.last_keys = self.current_keys
        self.rect.x, self.rect.y = self.pos
