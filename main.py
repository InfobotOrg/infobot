# github.com/RolandPetrean/infobot

import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from pbinfo.group import PbinfoGroup
from solinfo.group import SolinfoGroup

load_dotenv()

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
client.run(os.environ.get('TOKEN'))