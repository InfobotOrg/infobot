import itertools
import json
import discord
from discord import app_commands
from infoarena import infoarena
from util import dsutil

pb=json.load(open('infoarena/_pb.json'))

async def problema_autocomplete(interaction: discord.Interaction, current: str):
  auto = (app_commands.Choice(name=f'{v} ({k})', value=k) for k,v in pb.items() if current.lower() in f'{v.lower()} ({k})')
  return list(itertools.islice(auto, 10)) # autocomplete up to 10 items

class InfoarenaGroup(app_commands.Group):
  def __init__(self):
    super().__init__(name='infoarena', description='Comenzi legate de infoarena')

  @app_commands.command(name='problema', description='Caută o problemă pe infoarena')
  @app_commands.describe(nume='Numele problemei')
  @app_commands.autocomplete(nume=problema_autocomplete)
  async def problema(self, interaction: discord.Interaction, nume: str):
    await interaction.response.defer()
    
    data = await infoarena.get_problem(nume)
    if data['error']:
      if data['error'] == 302:
        embed = dsutil.create_error_embed('Problema nu există.')
      else:
        embed = dsutil.create_error_embed('Cauza este necunoscută.')
      await interaction.edit_original_response(embed=embed)
      return
    
    embed = dsutil.create_problem_embed(f'Problema {pb[nume]} ({nume})', data)

    # Link to problem button
    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.infoarena.ro/problema/{nume}', label='Problema')
    view = discord.ui.View().add_item(btn)
    await interaction.edit_original_response(embed=embed, view=view)