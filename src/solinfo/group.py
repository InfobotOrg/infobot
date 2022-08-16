import itertools
import json
import discord
from discord import app_commands
from solinfo import solinfo
from util import dsutil, util

pb = json.load(open('pbinfo/_pb.json'))
solpb = json.load(open('solinfo/_pb.json'))

async def solinfo_autocomplete(interaction: discord.Interaction, current: str):
  auto = (app_commands.Choice(name=f'#{p["id"]} {p["name"]}', value=p['name']) for p in solpb if current.lower() in f'#{p["id"]} {p["name"]}')
  return list(itertools.islice(auto, 10))

class SolinfoGroup(app_commands.Group):
  def __init__(self):
    super().__init__(name='solinfo', description='Comenzi legate de solinfo')

  @app_commands.command(name='solutie', description='Găsește soluția la o problemă')
  @app_commands.describe(nume='Numele problemei')
  @app_commands.autocomplete(nume=solinfo_autocomplete)
  async def solutie(self, interaction: discord.Interaction, nume: str):
    await interaction.response.defer()

    solutions, source = await solinfo.get_solution(nume)
    if len(solutions) == 0:
      embed = dsutil.create_error_embed('Problema nu are nicio soluție.')
      if nume not in pb:
        embed = dsutil.create_error_embed('Problema nu există.')
      await interaction.edit_original_response(embed=embed)
      return
    id = pb[nume.replace('-', '_')]
    sol = solutions[0]
    author = await solinfo.get_profile(sol['author']['username'])

    embed = dsutil.create_embed(f'Problema #{id} {nume}', f'Problema are **{len(solutions)}** soluții.', [
      (f'sol-{sol["id"]} - {":star:"*int(sol["rating"])} ({sol["rating_count"]} voturi)', f'```{sol["language"]}\n{util.prettify(source, 500)}```')
    ], colour=dsutil.LIGHT_BLUE)
    embed.set_footer(text=f'Postată de {author["profile"]["first_name"]} {author["profile"]["last_name"]} (@{author["profile"]["username"]})', icon_url=author['profile']['profile_img'])

    pbbtn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.pbinfo.ro/probleme/{id}', label='Problema')
    solbtn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.solinfo.ro/problema/{nume}', label=f'Alte soluții')
    view = discord.ui.View().add_item(pbbtn).add_item(solbtn)
    await interaction.edit_original_response(embed=embed, view=view)
