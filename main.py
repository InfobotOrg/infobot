# github.com/RolandPetrean/infobot

import sys
import discord
from discord import app_commands
from pbinfo.group import PbinfoGroup
from solinfo.group import SolinfoGroup

if len(sys.argv) != 2:
  print('You need to pass the token of the bot as a single argument')
  exit()


class Infobot(discord.Client):
  def __init__(self):
    super().__init__(intents=discord.Intents.none())
  
  async def setup_hook(self):
    tree.add_command(PbinfoGroup())
    tree.add_command(SolinfoGroup())
    await tree.sync()

  async def on_ready(self):
    print('Ready')

client = Infobot()
tree = app_commands.CommandTree(client)
client.run(sys.argv[1])