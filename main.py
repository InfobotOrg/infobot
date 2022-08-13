# github.com/RolandPetrean/infobot

import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from util import dsutil
from infoarena.group import InfoarenaGroup
from pbinfo.group import PbinfoGroup
from solinfo.group import SolinfoGroup

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

@tree.command(name='info', description='Informații despre Infobot')
async def info(interaction: discord.Interaction):
  embed = dsutil.create_embed('Infobot', '', [
    ('Invită', '[Invită](https://discord.com/oauth2/authorize?client_id=1006240882812539043&permissions=2147485696&scope=bot) Infobot pe server-ul tău.'),
    ('Despre', 'Infobot este un discord bot care poate prelucra date de pe [pbinfo](https://www.pbinfo.ro), [solinfo](https://www.solinfo.ro/) și [infoarena](https://www.infoarena.ro). Sursa poate fi găsită pe [github](https://github.com/RolandPetrean/infobot).'),
    ('Librării folosite', f'Infobot a fost creat folosind [discordpy 2.0](https://github.com/Rapptz/discord.py) și [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/) pentru parsing.'),
    ('Mulțumesc', '- Contribuitorilor de pe github pentru ajutorul acordat;\n- Solinfo pentru că au un API și nu a trebuit să fac parsing :)')
  ], colour=dsutil.LIGHT_BLUE)
  embed.set_footer(text='Versiunea 1.0.0');
  await interaction.response.send_message(embed=embed)

client.run(os.environ.get('TOKEN'))