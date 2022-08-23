import itertools
import json
import discord
from discord import app_commands
from infoarena import infoarena
from util import dsutil

pb=json.load(open('../gen/output/infoarena.json'))

async def problema_autocomplete(interaction: discord.Interaction, current: str):
  auto = [app_commands.Choice(name=f'{v} ({k.split("$")[1]})', value=k) for k,v in pb.items() if current.lower() in f'{k.split("$")[0]} {v.lower()} ({k.split("$")[1]})']
  return list(itertools.islice(auto, 10)) # autocomplete up to 10 items

class InfoarenaGroup(app_commands.Group):
  def __init__(self):
    super().__init__(name='infoarena', description='Comenzi legate de infoarena')

  @app_commands.command(name='problema', description='Caută o problemă pe infoarena')
  @app_commands.describe(nume='Numele problemei')
  @app_commands.autocomplete(nume=problema_autocomplete)
  async def problema(self, interaction: discord.Interaction, nume: str):
    await interaction.response.defer()
    
    archive = nume.split('$')[0]
    name = nume.split('$')[1]
    data = await infoarena.get_problem(name, archive)
    if data['error']:
      if data['error'] == 302:
        embed = dsutil.create_error_embed('Problema nu există.')
      else:
        embed = dsutil.create_error_embed('Cauza este necunoscută.')
      await interaction.edit_original_response(embed=embed)
      return
    
    embed = dsutil.create_problem_embed(f'Problema {pb[nume]} ({name})', data)

    # Link to problem button
    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.{"varena" if archive == "varena" else "infoarena"}.ro/problema/{name}', label='Problema')
    view = discord.ui.View().add_item(btn)
    await interaction.edit_original_response(embed=embed, view=view)