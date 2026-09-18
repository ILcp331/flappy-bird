import pygame as pg

pg.init()


class Bird(pg.sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32

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
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        self.space_key_pressed = False
        self.space_key_last_state = False

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            if self.space_key_last_state:
                self.space_key_pressed = False
            else:
                self.space_key_pressed = True

        self.space_key_last_state = keys[pg.K_SPACE]

    def move(self):
        keys = pg.key.get_pressed()

        if self.space_key_pressed:
            self.vel.y = self.FLAP_STRENGTH

        self.vel.y += self.GRAVITY
        self.vel.y = max(min(self.vel.y, self.TERMINAL_VEL), -self.TERMINAL_VEL)

        self.pos += self.vel

    def update(self):
        self.get_input()
        self.move()

        self.rect.x, self.rect.y = self.pos
