from customtkinter import set_appearance_mode

from bowlinggame.model.bowling import BowlingGame
from bowlinggame.ui.tkinter_ui import BowlingApp

if __name__ == "__main__":
    set_appearance_mode("light")
    game: BowlingGame = BowlingGame()
    app = BowlingApp(game)
    app.mainloop()
