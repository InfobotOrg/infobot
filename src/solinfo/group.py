import itertools
import json
import discord
from discord import app_commands
from solinfo import solinfo
from util import dsutil, util

pb = json.load(open('../gen/output/pbinfo.json'))
solinfo_pb = json.load(open('../gen/output/solinfo.json'))

async def solinfo_autocomplete(interaction: discord.Interaction, current: str):
  auto = (app_commands.Choice(name=f'#{v} {k}', value=k) for k,v in solinfo_pb.items() if current.lower() in f'#{v} {k}')
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
      await interaction.edit_original_response(embed=embed)
      return
    id = solinfo_pb[nume]
    sol = solutions[0]
    author = await solinfo.get_profile(sol['author']['username'])

    # Solution data
    embed = dsutil.create_embed(f'Problema #{id} {nume}', f'Problema are **{len(solutions)}** soluții.', [
      (f'sol-{sol["id"]} - {":star:"*int(sol["rating"])} ({sol["rating_count"]} voturi)', f'```{sol["language"]}\n{util.prettify(source, 500)}```')
    ], colour=dsutil.LIGHT_BLUE)
    embed.set_footer(text=f'Postată de {author["profile"]["first_name"]} {author["profile"]["last_name"]} (@{author["profile"]["username"]})', icon_url=author['profile']['profile_img'])

    # Links to the problem and solutions
    pbbtn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.pbinfo.ro/probleme/{id}', label='Problema')
    solbtn = discord.ui.Button(style=discord.ButtonStyle.link, url=f'https://www.solinfo.ro/problema/{nume}', label=f'Alte soluții')
    view = discord.ui.View().add_item(pbbtn).add_item(solbtn)
    await interaction.edit_original_response(embed=embed, view=view)
