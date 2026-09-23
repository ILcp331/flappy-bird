import random

import pygame as pg

from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_SKY
from .sprites.bird import Bird
from .sprites.pipe import Pipe
from .sprites.ground import Ground

pg.init()


class Game:
    def __init__(self, debug: bool = False):
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pg.time.Clock()
        self.sprites = pg.sprite.LayeredUpdates()
        self.danger = pg.sprite.Group()

        pg.display.set_caption('Flappy Bird')

        self.bird = Bird(self.sprites)
        Ground(self.sprites, self.danger)

        self.debug = debug
        self.running = True
        self.is_game_over = False
        self.frames = 0

    def spawn_pipe_pair(self):
        gap_y = random.randint(0 + Pipe.GAP_MARGIN_SIZE,
                               WINDOW_HEIGHT - Pipe.GAP_SIZE - Pipe.GAP_MARGIN_SIZE)

        top_pipe = Pipe(0, gap_y)
        bottom_pipe = Pipe(gap_y + Pipe.GAP_SIZE,
                           WINDOW_HEIGHT - (gap_y + Pipe.GAP_SIZE))

        self.sprites.add(top_pipe, bottom_pipe)
        self.danger.add(top_pipe, bottom_pipe)

    def game_over(self):
        self.is_game_over = True

        self.bird.die()
        for sprite in self.sprites:
            sprite.is_game_over = True

    def reset(self):
        self.is_game_over = False

        self.sprites.empty()
        self.danger.empty()

        self.bird = Bird(self.sprites)
        Ground(self.sprites, self.danger)

    def collisions(self):
        if pg.sprite.spritecollide(self.bird, self.danger, dokill=False):
            self.game_over()

    def draw_sprites(self):
        self.sprites.draw(self.window)

    def update(self):
        if self.is_game_over:
            if self.bird.is_pressed(self.bird.FLAP_KEY):
                self.reset()

        if self.frames % (Pipe.SPAWN_SECS * FPS) == 0:
            self.spawn_pipe_pair()

        self.sprites.update()
        self.collisions()
        self.draw_sprites()

        if self.debug:
            print(f'({self.frames} | {self.clock.get_fps():.2f})')
            print(f'game over? {self.is_game_over}')
            print(f'sprites: {len(self.sprites)}')
            print(f'bird pos {self.bird.pos.xy}')
            print(f'bird vel {self.bird.vel.xy}')
            print()

    def mainloop(self):
        self.window.fill(COLOR_SKY)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        self.update()

        pg.display.update()
        self.clock.tick(FPS)

        self.frames += 1
