import discord
from discord.ext import commands
import youtube_dl
import asyncio
from grid import Grid
import player
import ai
from player import Player, HumanPlayer, RandomAIPlayer
import random


class game(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def tictactoe (self,ctx, args):

    my_grid = Grid(int(args))
    inputs = list(range(1, (my_grid.size)*my_grid.size +1))
    my_grid.generate_grid()
    player = HumanPlayer(":o2")
    ai = RandomAIPlayer(":regional_indicator_x:")
    full_grid = my_grid.draw_grid()

    for row in full_grid:
      await ctx.send(row)   
    #Main loop. Exits if board is full. 
    while my_grid.grid_has_space():
      message = await ctx.send(f"Your turn")
    
      #Lambda function that is used to check that the input of the player is correct.
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel and self.check_valid_player_turn(m.content,inputs) == True
    
      #Check if player has input 1..9, if not wait 30 seconds for them to input or quit.
      try:
        confirm = await self.client.wait_for("message", check=check, timeout=30)
      except asyncio.TimeoutError:
        await message.edit(content="Game timed out, you took too long.")
        return
      
      #Add player input.
      my_grid.grid_input (confirm.content,":o2:")
      #Check for player win.
      if my_grid.check_for_win(my_grid):
        full_grid = my_grid.draw_grid()
        for row in full_grid:
          await ctx.send(row)
        await ctx.send("Player wins!")
        return
    
      #Check if board is full, if its not AI's turn.
      if  my_grid.grid_has_space():
        #Get a random tile that has not been played yet.
        rand_num = self.generate_ai_turn(my_grid)
        check = isinstance(rand_num, int)
        while not check:
          rand_num = self.generate_ai_turn(my_grid)
          check = isinstance(rand_num, int)
        #Input AI choice and remove tile played from the avaliable turns.      
        my_grid.grid_input (rand_num,":regional_indicator_x:")
        inputs.remove(rand_num)    
        #Check for AI win.
        if my_grid.check_for_win(my_grid):
          full_grid = my_grid.draw_grid()
          for row in full_grid:
            await ctx.send(row)
          await ctx.send("AI wins!")
          return
      #Draw the board  
      full_grid = my_grid.draw_grid()    
      for row in full_grid:
        await ctx.send(row)
    await ctx.send ("Draw!")

  #Function that checks if a move is possible. Returns true or false.       
  def move_possible(self, grid, input):
      
      inputs = input -1
      for x in range(grid.size):
          for y in range(grid.size):
              if grid.grid[x][y].key == inputs and grid.grid[x][y].value == ":white_large_square:":
                  return True
      return False  

  #Recursirve function that genereates AI's turn. 
  def generate_ai_turn(self,grid):
    move = random.randint(1,grid.size*grid.size)
    if self.move_possible(grid, move):
      return move
    else:
      print("Square is already taken, please try again")
      self.generate_ai_turn(grid)
  

  #A function that checks if the user input is allowed.
  def check_valid_player_turn(self, input,list):
    try :
      num = int(input)
      if num in list:
        list.remove(num)
        return True
    except ValueError :
      return False


def setup(client):
  client.add_cog(game(client))
