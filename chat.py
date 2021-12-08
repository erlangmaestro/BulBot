import discord
from discord.ext import commands
import os
import requests
import json
from json import loads
from keep_alive import keep_alive
from urllib.request import urlopen
import sys


class chat(commands.Cog):
  def __init__(self,client):
    self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == client.user:
        return
      await self.bot.process_commands(message)


  #This functions checks every message that has been sent by users. In this case if the specified message is an emote, the bot sends a message of the same emote. 
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.client.user:
        return
    if message.content in ['<:payoS:824437843937722409>', 'values']:
                          
      await message.channel.send("<:payoS:824437843937722409>")

    
  #This command connects to the Riot API and returns a rank based on the arguments passed after the command.
  @commands.command()
  async def rank (self,ctx, *args):

    region = args[-1]
    region_for_api = formatRegion(region)
    message_list= []
    for x in args:
      message_list.append(x)
    message_list.pop()
    summ_name = " ".join(message_list)
    
    reponseJSON = requestSummonerData(summ_name, region_for_api)
    id = reponseJSON['id']
    ranked_data_list = requestSummonerRank(id, region_for_api)
    ranked_data_json = ranked_data_list[0]

    tier = ranked_data_json['tier']
    rank = ranked_data_json["rank"]
    wins = str(ranked_data_json['wins'])
    losses = str(ranked_data_json['losses'])
    total_games = str(ranked_data_json['wins'] +
                      ranked_data_json['losses'])

    #Bot output handling.
    bot_output_msg = summ_name + "-" + region + " " + tier + " " + rank + " " "Wins: " + wins + " Losses: " + losses + " Total played: " + total_games
    if summ_name == "MadNanashi":
        await ctx.send(bot_output_msg + " " +
                                    "<:payoS:824437843937722409>")
    else:
        await ctx.send(bot_output_msg)

  #This command returns a player's 20 highest champipon masteries.   
  @commands.command()
  async def mastery(self,ctx,*args):


    region = args[-1]
    region_for_api = formatRegion(region)
    message_list= []
    for x in args:
      message_list.append(x)
    message_list.pop()
    summ_name = " ".join(message_list)
        #Handle the splitting of the initial chat command sent.
    region_for_api = formatRegion(region)
    reponseJSON = requestSummonerData(summ_name, region_for_api)
    id = reponseJSON['id']
    display_list = []
    all_data = requestChampionMastery(region_for_api, id)
    
    #champ_id1 = all_data[0]['championId']
    for x in range(0, 20):
      champ_id = all_data[x]['championId']
      champ_name = get_champions_name(champ_id)
      champ_points = all_data[x]['championPoints']
      display_list.append(champ_name + "-" + str(champ_points))

    await ctx.send(display_list)

  #This commands prints a large string of every functionality the bot offers.
  @commands.command()
  async def commands(self,ctx,*args):

    all_commands = "**!rank to view LoL rank. [*!rank Doublelift NA*] the regions are NA/EUW \n!mastery to view LoL mastery level for your top 20 Champions. [*!mastery Doublelift NA*]\n!play to play a Youtube video. [*!play YOUTUBE_URL*] \n!pause to pause a Youtube video. [*!pause*]\n!resume to resume a Youtube video. [*!resume*]\n!tictactoe to play a game of tictactoe vs AI [*!tictactoe*]**"
    await ctx.send(all_commands)

#Add the current cog to the client.
def setup(client):
  client.add_cog(chat(client))

#Change region string for the API call.
def formatRegion(region):
    if region == "EUW":
        return 'euw1'
    if region == "NA":
        return "na1"

#Function that returns a JSON object that is needed to view the summoner id.
def requestSummonerData(summonerName, region):
    sumname = summonerName
    url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sumname + "?api_key=RGAPI-24e4035d-2010-489f-af46-3282770d7e7a"
    data = requests.get(url)
    return data.json()

#Function that returns a JSON object that is needed to view the summoner rank.
def requestSummonerRank(id, region):
  url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + id + "?api_key=RGAPI-24e4035d-2010-489f-af46-3282770d7e7a"
  data = requests.get(url).json()
  return data

#Function that returns a JSON object of the summoner masteries. 
def requestChampionMastery(region, id):
  url = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + id + "?api_key=RGAPI-24e4035d-2010-489f-af46-3282770d7e7a"
  data = requests.get(url).json()
  return data

#The champions on Riot's API are returned as keys so we need to transalte them to their actual names.
def get_champions_name(_id):
    all_champion_id = {
        1: 'Annie',
        2: 'Olaf',
        3: 'Galio',
        4: 'Twisted Fate',
        5: 'Xin Zhao',
        6: 'Urgot',
        7: 'LeBlanc',
        8: 'Vladimir',
        9: 'Fiddlesticks',
        10: 'Kayle',
        11: 'Master Yi',
        12: 'Alistar',
        13: 'Ryze',
        14: 'Sion',
        15: 'Sivir',
        16: 'Soraka',
        17: 'Teemo',
        18: 'Tristana',
        19: 'Warwick',
        20: 'Nunu & Willump',
        21: 'Miss Fortune',
        22: 'Ashe',
        23: 'Tryndamere',
        24: 'Jax',
        25: 'Morgana',
        26: 'Zilean',
        27: 'Singed',
        28: 'Evelynn',
        29: 'Twitch',
        30: 'Karthus',
        31: "Cho'Gath",
        32: 'Amumu',
        33: 'Rammus',
        34: 'Anivia',
        35: 'Shaco',
        36: 'Dr.Mundo',
        37: 'Sona',
        38: 'Kassadin',
        39: 'Irelia',
        40: 'Janna',
        41: 'Gangplank',
        42: 'Corki',
        43: 'Karma',
        44: 'Taric',
        45: 'Veigar',
        48: 'Trundle',
        50: 'Swain',
        51: 'Caitlyn',
        53: 'Blitzcrank',
        54: 'Malphite',
        55: 'Katarina',
        56: 'Nocturne',
        57: 'Maokai',
        58: 'Renekton',
        59: 'JarvanIV',
        60: 'Elise',
        61: 'Orianna',
        62: 'Wukong',
        63: 'Brand',
        64: 'LeeSin',
        67: 'Vayne',
        68: 'Rumble',
        69: 'Cassiopeia',
        72: 'Skarner',
        74: 'Heimerdinger',
        75: 'Nasus',
        76: 'Nidalee',
        77: 'Udyr',
        78: 'Poppy',
        79: 'Gragas',
        80: 'Pantheon',
        81: 'Ezreal',
        82: 'Mordekaiser',
        83: 'Yorick',
        84: 'Akali',
        85: 'Kennen',
        86: 'Garen',
        89: 'Leona',
        90: 'Malzahar',
        91: 'Talon',
        92: 'Riven',
        96: "Kog'Maw",
        98: 'Shen',
        99: 'Lux',
        101: 'Xerath',
        102: 'Shyvana',
        103: 'Ahri',
        104: 'Graves',
        105: 'Fizz',
        106: 'Volibear',
        107: 'Rengar',
        110: 'Varus',
        111: 'Nautilus',
        112: 'Viktor',
        113: 'Sejuani',
        114: 'Fiora',
        115: 'Ziggs',
        117: 'Lulu',
        119: 'Draven',
        120: 'Hecarim',
        121: "Kha'Zix",
        122: 'Darius',
        126: 'Jayce',
        127: 'Lissandra',
        131: 'Diana',
        133: 'Quinn',
        134: 'Syndra',
        136: 'AurelionSol',
        141: 'Kayn',
        142: 'Zoe',
        143: 'Zyra',
        145: "Kai'sa",
        147: "Seraphine",
        150: 'Gnar',
        154: 'Zac',
        157: 'Yasuo',
        161: "Vel'Koz",
        163: 'Taliyah',
        166: "Akshan",
        164: 'Camille',
        201: 'Braum',
        202: 'Jhin',
        203: 'Kindred',
        222: 'Jinx',
        223: 'TahmKench',
        234: 'Viego',
        235: 'Senna',
        236: 'Lucian',
        238: 'Zed',
        240: 'Kled',
        245: 'Ekko',
        246: 'Qiyana',
        254: 'Vi',
        266: 'Aatrox',
        267: 'Nami',
        268: 'Azir',
        350: 'Yuumi',
        360: 'Samira',
        412: 'Thresh',
        420: 'Illaoi',
        421: "Rek'Sai",
        427: 'Ivern',
        429: 'Kalista',
        432: 'Bard',
        497: 'Rakan',
        498: 'Xayah',
        516: 'Ornn',
        517: 'Sylas',
        526: 'Rell',
        518: 'Neeko',
        523: 'Aphelios',
        555: 'Pyke',
        875: "Sett",
        711: "Vex",
        777: "Yone",
        887: "Gwen",
        876: "Lillia",
    }
    return all_champion_id.get(_id)
