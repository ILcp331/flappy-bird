import random

import pygame as pg

from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_SKY, PATH_FONT_DEBUG
from .sprites.bird import Bird
from .sprites.pipe import Pipe
from .sprites.ground import Ground
from .ui.score import ScoreDisplay
from .utils.text import draw_lines

pg.init()


class Game:
    GAME_OVER_RESTART_COOLDOWN = 45

    DEBUG_FONT = pg.font.Font(PATH_FONT_DEBUG, 16)
    DEBUG_COLOR = (0, 0, 0)

    def __init__(self, allow_debug: bool = False):
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pg.time.Clock()
        self.sprites = pg.sprite.LayeredUpdates()
        self.danger = pg.sprite.Group()
        self.ui_elems = pg.sprite.Group()

        pg.display.set_caption('Flappy Bird')

        # Sprites
        self.bird = Bird(self.sprites)
        Ground(self.sprites, self.danger)

        # UI
        self.score_disp = ScoreDisplay(self.ui_elems)
        self.score_disp.bounce()

        self.debug_active = False
        self.allow_debug = allow_debug
        self.running = True
        self.frames = 0

        self.is_game_over = False
        self.game_over_timer = 0

        self.debug_lines = []

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
        self.game_over_timer = 0

        self.sprites.empty()
        self.danger.empty()

        self.bird = Bird(self.sprites)
        Ground(self.sprites, self.danger)

        self.score_disp.value = 0
        self.score_disp.bounce()

    def collisions(self):
        if pg.sprite.spritecollide(self.bird, self.danger, dokill=False):
            self.game_over()

    def draw_sprites(self):
        self.sprites.draw(self.window)
        self.ui_elems.draw(self.window)

    def update_game_over(self):
        self.sprites.update()
        self.ui_elems.update()

        if self.game_over_timer >= self.GAME_OVER_RESTART_COOLDOWN:
            # Ran after updating bird sprite to override its color
            self.bird.image.fill(self.bird.COLOR_READY)

            if self.bird.is_pressed(self.bird.FLAP_KEY):
                self.reset()
                return

        self.draw_sprites()

        self.game_over_timer += 1

    def update(self):
        if self.frames % (Pipe.SPAWN_SECS * FPS) == 0:
            self.spawn_pipe_pair()

        self.sprites.update()
        self.ui_elems.update()
        self.collisions()
        self.draw_sprites()

    def update_debug_lines(self):
        self.debug_lines = [
            f'frame {self.frames} (fps: {self.clock.get_fps():.2f})',
            f'sprites: {len(self.sprites)}',
            f'bird pos {self.bird.pos.xy}',
            f'bird vel {self.bird.vel.xy}',
            f'game over? {self.is_game_over}',
        ]

        if self.is_game_over:
            can_restart = self.game_over_timer >= self.GAME_OVER_RESTART_COOLDOWN
            self.debug_lines.append(
                f'can restart? {can_restart}, '
                f'{self.game_over_timer}/{self.GAME_OVER_RESTART_COOLDOWN}',
            )

    def debug(self):
        self.update_debug_lines()

        draw_lines(
            self.window,
            (8, 8),
            self.DEBUG_FONT,
            self.debug_lines,
            self.DEBUG_COLOR,
            alignment='left'
        )

    def mainloop(self):
        self.window.fill(COLOR_SKY)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_0:
                    if self.allow_debug:
                        self.debug_active = not self.debug_active

                if e.key == pg.K_EQUALS:
                    if self.debug_active:
                        self.score_disp.value += 1
                        self.score_disp.bounce()

        if self.is_game_over:
            self.update_game_over()
        else:
            self.update()

        if self.debug_active:
            self.debug()

        pg.display.update()
        self.clock.tick(FPS)

        self.frames += 1
