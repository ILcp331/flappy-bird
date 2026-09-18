import pygame as pg

from .constants import WIDTH, HEIGHT, FPS, COLOR_SKY

pg.init()


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        pg.display.set_caption('Flappy Bird')

        self.running = True

    def update(self):
        self.window.fill(COLOR_SKY)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        pg.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()

    while game.running:
        game.update()
