import itertools
import json
import discord
from discord import app_commands
from pbinfo import pbinfo
from util import dsutil

pb=json.load(open('../gen/output/pbinfo.json'))

async def problema_autocomplete(interaction: discord.Interaction, current: str):
  auto = (app_commands.Choice(name=f'#{v} {k}', value=v) for k,v in pb.items() if current.lower() in f'#{v} {k.lower()}')
  return list(itertools.islice(auto, 10)) # autocomplete up to 10 items

class PbinfoGroup(app_commands.Group):
  def __init__(self):
    super().__init__(name='pbinfo', description='Comenzi legate de pbinfo')

  @app_commands.command(name='problema', description='Caută o problemă pe pbinfo')
  @app_commands.describe(id='Numele problemei')
  @app_commands.autocomplete(id=problema_autocomplete)
  async def problema(self, interaction: discord.Interaction, id: int):
    await interaction.response.defer()
    
    data = await pbinfo.get_problem(id)
    if data['error']:
      if data['error'] == 404:
        embed = dsutil.create_error_embed('Problema nu există.')
      else:
        embed = dsutil.create_error_embed('Cauza este necunoscută.')
      await interaction.edit_original_response(embed=embed)
      return

    embed = dsutil.create_problem_embed(f'Problema #{data["id"]} {data["name"]} - {data["solutions"]} Soluții', data)

    # Link to problem button
    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.pbinfo.ro/probleme/{id}', label='Problema')
    view = discord.ui.View().add_item(btn)
    await interaction.edit_original_response(embed=embed, view=view)
  
  @app_commands.command(name='cont', description='Vezi contul de pbinfo al unui utilizator')
  @app_commands.describe(nume='Numele utilizatorului')
  async def cont(self, interaction: discord.Interaction, nume: str):
    await interaction.response.defer()
    
    data = await pbinfo.get_account(nume)
    if data['error']:
      if data['error'] == 404:
        embed = dsutil.create_error_embed('Utilizatorul nu există.')
      elif data['error'] == 403:
        embed = dsutil.create_error_embed('Utilizatorul are contul privat.')
      else:
        embed = dsutil.create_error_embed('Cauza este necunoscută.')
      await interaction.edit_original_response(embed=embed)
      return

    # General info
    problems = pbinfo.process_problems(data['problems'])
    embed = dsutil.create_embed(nume, f':white_check_mark: {len(problems["total_solved"])} Probleme rezolvate\n:no_entry: {len(problems["total_tried"])} Probleme încercate dar nerezolvate\n:triangular_flag_on_post: {problems["total_sub"]} Surse trimise\n:checkered_flag: {data["success"]}% Succes', [], colour=dsutil.LIGHT_BLUE)

    # Last problems solved    
    embedValue = ', '.join(f'[{x["denumire"]}](https://www.pbinfo.ro/probleme/{x["id"]})' for x in problems['total_solved'][:5])
    dsutil.add_data(embed, 'Jurnal probleme', embedValue)

    # Solved by classes
    for cls in range(9, 12):
      embed.add_field(name=f'Clasa a {cls}-a', value=f'{len(problems["solved"][f"{cls}"])} Probleme rezolvate - {len(problems["tried"][f"{cls}"])} Probleme nerezolvate', inline=False)

    # Profile picture and goal picture
    embed.set_author(name=data['display_name'], url=f'https://www.pbinfo.ro/profil/{nume}', icon_url=data['avatar'])
    embed.set_thumbnail(url=data['goal'])

    # Link to account button
    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.pbinfo.ro/profil/{nume}', label='Cont')
    view = discord.ui.View().add_item(btn)


    await interaction.edit_original_response(view=view, embed=embed)
