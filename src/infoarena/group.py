import itertools
import json
import discord
from discord import app_commands
from infoarena import infoarena
from util import dsutil
from util import util

pb=json.load(open('../gen/output/infoarena.json'))
INFOARENA_ICON = 'https://i.ibb.co/2vVNk5S/infoarena.png'
VARENA_ICON = 'https://i.ibb.co/Xybdcps/image.png'

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
  
  @app_commands.command(name='cont', description='Vezi contul de infoarena al unui utilizator')
  @app_commands.describe(nume='Numele utilizatorului')
  @app_commands.describe(varena='Contul e pe varena?')
  async def cont(self, interaction: discord.Interaction, nume: str, varena: bool=False):
    await interaction.response.defer()

    data = await infoarena.get_account(nume, varena)
    if data['error']:
      embed = dsutil.create_error_embed('Utilizatorul nu există (sau s-a întâmplat ceva foarte greșit).')
      await interaction.edit_original_response(embed=embed)
      return
    
    embed = dsutil.create_embed(nume, f':white_check_mark: {data["solved"]} Probleme rezolvate\n:no_entry: {data["unsolved"]} Probleme încercate dar nerezolvate', [
      ('Rating', data['rating']),
      ('Statut', data['statut']),
    ], colour=dsutil.LIGHT_BLUE)
    embed.set_author(name=data['display_name'], url=f'https://www.{"varena" if varena else "infoarena"}.ro/utilizator/{nume}', icon_url=VARENA_ICON if varena else INFOARENA_ICON)

    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.{"varena" if varena else "infoarena"}.ro/utilizator/{nume}', label='Cont')
    view = discord.ui.View().add_item(btn)

    await interaction.edit_original_response(view=view, embed=embed)
  
  @app_commands.command(name='monitor', description='Vizualizează monitorul infoarena')
  @app_commands.describe(nume='Numele utilizatorului', problema='Numele problemei')
  @app_commands.autocomplete(problema=problema_autocomplete)
  async def monitor(self, interaction: discord.Interaction, nume: str="", problema:str=""):
    await interaction.response.defer()

    archive = problema.split('$')[0]
    varena = (archive=='varena')
    problema = problema.split('$')[1]
    data = await infoarena.get_monitor(nume, problema, varena)
    if data['error']:
      embed = dsutil.create_error_embed('Cauza este necunoscută.')
      await interaction.edit_original_response(embed=embed)
      return

    desc = util.get_category(archive)+'\n'
    for eval in data['evals']:
      desc += f'[#{eval["id"]}](https://www.{"varena" if varena else "infoarena"}.ro/job_detail/{eval["id"]}) - [{eval["display_name"]}](https://www.{"varena" if varena else "infoarena"}.ro/utilizator/{eval["username"]}) - [{eval["task"]}](https://www.{"varena" if varena else "infoarena"}.ro/problema/{eval["task_link"]}) - {eval["points"]}p' + '\n'
    embed = dsutil.create_embed('Monitor', desc, [], colour=dsutil.LIGHT_BLUE)

    footer = None
    if nume and problema:
      footer = f'Soluțiile lui {nume} la {problema}'
    elif nume:
      footer = f'Soluțiile lui {nume}'
    elif problema:
      footer = f'Soluțiile la {problema}'

    embed.set_footer(text=footer) 

    btn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.{"varena" if varena else "infoarena"}.ro/monitor?user={nume}&task={problema}', label='Monitor')
    view = discord.ui.View().add_item(btn)

    await interaction.edit_original_response(view=view, embed=embed)
  