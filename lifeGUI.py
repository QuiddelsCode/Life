import tkinter as tk
import tkinter.filedialog as fdlg
import life

class LifeGUI (tk.Frame):
    def __init__(self, master, *args, size=45, scale=8, **kwargs):
        super().__init__(master, *args, **kwargs)
        # set some constants for later
        self.size= size
        self.scale = scale
        self.delta = 250
        # add some interface buttons
        self.import_button = tk.Button(self, text="import image", command=self.import_img)
        self.clear_button = tk.Button(self, text="clear board", command=self.clear)
        self.toggle_sim_button = tk.Button(self, text="toggle simulation",
                                           command=lambda: self.toggle_sim(None))
        self.save_button = tk.Button(self, text="save board", command=self.save)
        self.restore_button = tk.Button(self, text="restore board", command=self.restore)
        # set up a nice black canvas
        dim = size * scale
        self.disp = tk.Canvas(self, width=dim, height=dim, bg="black")
        self.disp.grid(row=0, column=0, columnspan=3)
        self.save_button.grid(row=1, column=0)
        self.restore_button.grid(row=1, column=1)
        self.clear_button.grid(row=1, column=2)
        self.import_button.grid(row=2, column=0)
        self.toggle_sim_button.grid(row=2, column=1)
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

    def clear(self):
        self.gs.clear_board()

    def import_img(self):
        path = fdlg.askopenfilename()
        self.gs.load_image(path)

    def save(self):
        self.gs.save_board()
        print("board saved")

    def restore(self):
        self.gs.restore_board()
        print("board restored")

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
    game = LifeGUI(root, size=150, scale=6)
    game.pack()
    game.focus_set()
    root.mainloop()
