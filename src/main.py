import pygame as pg

from .constants import WIDTH, HEIGHT, FPS, COLOR_SKY
from .sprites.bird import Bird

pg.init()


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.sprites = pg.sprite.Group()

        pg.display.set_caption('Flappy Bird')

        self.bird = Bird((WIDTH/4, 0), self.sprites)

        self.running = True

    def draw_sprites(self):
        self.sprites.draw(self.window)

    def update(self):
        self.window.fill(COLOR_SKY)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        self.bird.update()
        self.draw_sprites()

        pg.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()

    while game.running:
        game.update()
