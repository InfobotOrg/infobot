# github.com/RolandPetrean/infobot

import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from util import dsutil
from infoarena.group import InfoarenaGroup
from pbinfo.group import PbinfoGroup
from solinfo.group import SolinfoGroup
import github
import configparser

class Infobot(discord.Client):
  def __init__(self):
    super().__init__(intents=discord.Intents.none())
  
  async def setup_hook(self):
    tree.add_command(PbinfoGroup())
    tree.add_command(SolinfoGroup())
    tree.add_command(InfoarenaGroup())
    await tree.sync()

  async def on_ready(self):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='pbinfo'))
    print('Ready')

load_dotenv()
client = Infobot()
tree = app_commands.CommandTree(client)

# TODO maybe move this to a separate group?
configReader = configparser.RawConfigParser()
configReader.read("../.bumpversion.cfg")
CURRENT_VERSION = configReader.get("bumpversion", "current_version")
@tree.command(name='ajutor', description='Informații despre Infobot')
async def ajutor(interaction: discord.Interaction):
  contributors = [f'[{contrib[0]}]({contrib[1]})' for contrib in await github.get_contributors()]

  embed = dsutil.create_embed('Informații', '[Adaugă pe server](https://discord.com/oauth2/authorize?client_id=1006240882812539043&permissions=2147485696&scope=bot)', [
    ('Despre', f'Infobot este un discord bot care poate prelucra date de pe [pbinfo](https://www.pbinfo.ro), [solinfo](https://www.solinfo.ro/) și [infoarena](https://www.infoarena.ro). Sursa poate fi găsită pe [github](https://github.com/RolandPetrean/infobot).'),
    ('Librării folosite', f'Am folosit [discordpy 2.0](https://github.com/Rapptz/discord.py) și [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/) pentru parsing.'),
    (f'Contribuitori ({len(contributors)})', ', '.join(contributors))
  ], colour=dsutil.LIGHT_BLUE)
  embed.set_footer(text=f'Infobot v{CURRENT_VERSION}')
  await interaction.response.send_message(embed=embed)

client.run(os.environ.get('TOKEN'))