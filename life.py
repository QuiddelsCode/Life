import numpy as np
from PIL import Image

class GameState:
    def __init__(self, size=45):
        self.board = np.zeros((size, size))
        self.saved = np.zeros((size, size))
        self.size = size

    def handle_input(self, flipped):
        for cell in flipped:
            self.board[cell] = 1 - self.board[cell]

    def game_tick(self):
        # Generate a new board full of dead cells
        newboard = np.zeros((self.size, self.size))
        for x in range(self.size):
            for y in range(self.size):
                # prevent accessing indices outside our array
                x1 = max(0, x-1)
                y1 = max(0, y-1)
                x2 = min(x+2, self.size-1)
                y2 = min(y+2, self.size-1)
                # get the 3x3 area of our array around (x, y) to look at
                subboard = self.board[x1:x2, y1:y2]
                cell = self.board[x, y]
                alive = np.count_nonzero(subboard)
                # make sure we don't count our cell itself
                alive -= cell
                # here are the rules for living cells in GoL
                if alive == 2 and cell == 1:
                    newboard[x, y] = 1
                elif alive == 3:
                    newboard[x, y] = 1
        self.board = newboard

    def load_image(self, path):
        img = Image.open(path)
        # make the image black-and-white
        img = img.convert("1")
        data = np.asarray(img, dtype="int32")
        data = np.rot90(data)
        data = 1-data
        # center the image on the map
        width, height = data.shape
        x_offset = int((self.size - width) / 2)
        y_offset = int((self.size - height) / 2)
        self.board[x_offset:x_offset+width, y_offset:y_offset+height] = data

    def save_board(self):
        self.saved = self.board.copy()

    def restore_board(self):
        self.board = self.saved.copy()

    def clear_board(self):
        self.board = np.zeros((self.size, self.size))

    def print_display(self):
        # print the game state into stdout
        rows, cols = self.board.shape
        for i in range(rows):
            line = ""
            for j in range(cols):
                line += str(int(self.board[(j, i)])) + "\t"
            print(line)

if __name__ == "__main__":
    g = GameState(size=5)
    g. print_display()
    while True:
        flipped = []
        while True:
            coords = input("?")
            if coords.strip() == "":
                break
            x = int(coords.split(" ")[0].strip())
            y = int(coords.split(" ")[1].strip())
            flipped.append((x, y))
        g.handle_input(flipped)
        g.game_tick()
        g.print_display()
