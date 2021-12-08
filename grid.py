from tile import Tile
import discord
from discord.ext import commands



class Grid():
  def __init__(self, size):
      self.size = size
      self.state = "X"
      self.grid = [["X" for x in range(size)] for y in range(size)]


  #Generate a grid and assign each Tile an empty value.
  def generate_grid(self):
      key = 0
      for x in range(self.size):
          for y in range(self.size):
              self.grid[x][y] = Tile()
              self.grid[x][y].key = key
              self.grid[x][y].value = ":white_large_square:" 
              key +=1

  #Check if move is possible. Currentely not used.
  def move_possible(self, input):
      
      for x in range(self.size):
          for y in range(self.size):
              if self.grid[x][y].key == input and self.grid[x][y].value == ":white_large_square:":
                  return True
      return False


  #Input a move on the grid.
  def grid_input(self, input, emote):

      input = int(input)-1
      for x in range(self.size):
          for y in range(self.size):
              if self.grid[y][x].key == input:
                  self.grid[y][x].value = emote
                  
  #Check if grid is full.
  def grid_has_space(self):
      for x in range(self.size):
          for y in range(self.size):
              if self.grid[x][y].value == ":white_large_square:":
                  return True
      return False

  #Returns a list of rows that are to be printed. 
  def draw_grid(self):

      full_grid = []
      for x in range(self.size):
          row = ""
          for y in range(self.size):
              row += self.grid[x][y].value + " "
          full_grid.append(row)
      return full_grid

  #Check win condition for rows.
  def check_rows(self, grid):
      for row in grid.grid:
          values_row = []
          for ele in row:
              values_row.append(ele.value)
          win = all(elem == values_row[0] for elem in values_row)
          if win and values_row[0] != ":white_large_square:":
              return True
      return False

  #Check win condition for cols.
  def check_cols(self, count, grid):
      if count ==grid.size:
          return False
      values_col = []
      values_col.clear()
      for col in grid.grid:
          values_col.append(col[count].value)
      win = all(elem == values_col[0] for elem in values_col)


      if win and values_col[0] != ":white_large_square:":
          return True
      else:
          return grid.check_cols(count+1, grid)

  #Check win conditions for diagonals.
  def check_diagonal(self, grid):
      count_first_diag = 0
      values_diag = []
      for col in grid.grid:
          values_diag.append(col[count_first_diag].value)
          count_first_diag += 1
      win = all(elem == values_diag[0] for elem in values_diag)
      if win and values_diag[0] != ":white_large_square:":
          return win

      values_diag_second = []
      count_second_diag = grid.size-1
      for col in grid.grid:
          values_diag_second.append(col[count_second_diag].value)
          count_second_diag -= 1
      win = all(elem == values_diag_second[0] for elem in values_diag_second)
      if win and values_diag_second[0] != ":white_large_square:":
          return win
      else:
          return False

  def check_all_cols(self, counter):
      return self.check_cols(counter)
  #Check if game has been won.
  def check_for_win(self, grid):
      if self.check_diagonal(grid) or self.check_rows(grid) or self.check_cols(0,grid):
        return True
      else:
        return False


