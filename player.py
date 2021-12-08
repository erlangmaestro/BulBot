import random


class Player():
    def __init__(self, letter):
        self.letter = letter
    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, grid):
        move = input()
        if grid.move_possible(move):
            grid.grid_input(move, self.letter)
        else:
            print("Square is already taken, please try again")
            self.get_move(grid)


class RandomAIPlayer(Player):
    def __init__(self, letter):
        self.letter = letter

    
    def get_move(self, grid):
        move = random.randint(0,8)
        if grid.move_possible(move):
            return move
        else:
            print("Square is already taken, please try again")
            self.get_move(grid)

