from src.main import Game


if __name__ == "__main__":
    game = Game(debug=True)

    while game.running:
        game.mainloop()
