import tkinter as tk
import life

class LifeGUI (tk.Frame):
    def __init__(self, master, *args, size=45, scale=8, **kwargs):
        super().__init__(master, *args, **kwargs)
        # set some constants for later
        self.size= size
        self.scale = scale
        self.delta = 250
        # set up a nice black canvas
        dim = size * scale
        self.disp = tk.Canvas(self, width=dim, height=dim, bg="black")
        self.disp.pack()
        # create and render the initial game state
        self.coords = []
        self.sim = False
        self.gs = life.GameState(size=size)
        self.render()
        # bind the mouse inputs to flip cells
        self.bind("<space>", self.toggle_sim)
        # bind the space key to start / pause simulation
        self.disp.bind("<Button-1>", self.register_click)
        # set up the game loop timer
        self.after(self.delta, self.advance)

    def toggle_sim(self, e):
        self.sim = not self.sim

    def register_click(self, e):
        x = int(e.x / self.scale)
        y = int(e.y / self.scale)
        if x < 0 or x >= self.size:
            return
        if y < 0 or y >= self.size:
            return
        if (x, y) not in self.coords:
            self.coords.append((x, y))

    def render(self):
        self.disp.delete("all")
        for x in range(self.size):
            for y in range(self.size):
                if self.gs.board[x, y] == 0:
                    continue
                xpos1 = x*self.scale
                ypos1 = y*self.scale
                xpos2 = (x+1)*self.scale
                ypos2 = (y+1)*self.scale
                if self.sim:
                    self.disp.create_rectangle(xpos1, ypos1, xpos2, ypos2,
                                               fill = "green")
                else:
                    self.disp.create_rectangle(xpos1, ypos1, xpos2, ypos2,
                                               fill = "white")

    def advance(self):
        if self.sim:
            self.gs.game_tick()
        else:
            self.gs.handle_input(self.coords)
            self.coords = []
        self.render()
        self.after(self.delta, self.advance)

if __name__ == "__main__":
    root = tk.Tk()
    game = LifeGUI(root)
    game.pack()
    game.focus_set()
    root.mainloop()