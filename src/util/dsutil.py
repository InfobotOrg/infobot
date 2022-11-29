import discord

LIGHT_BLUE = 0xADD8FF
RED = 0xFF0000

def add_data(embed: discord.Embed, name: str, value: any, inline: bool=False):
  """Add a field to an embed, but only if the value is truthy.
  
  embed -- the embed
  name -- the field's name
  value -- the field's value
  inline -- whether the field should be inline"""

  if value:
    embed.add_field(name=name, value=value, inline=inline)

def add_tuple(embed: discord.Embed, fields: "list[tuple]"):
  """Call add_data on a list of tuples.
  
  embed -- the embed
  fields -- a list of `(name, value, inline?)` tuples that should be added
  """

  for field in fields:
    inline = False
    if (len(field) == 3):
      inline = field[2]
    add_data(embed, field[0], field[1], inline=inline)

def create_embed(title: str, desc: str, fields: "list[tuple]", colour: hex) -> discord.Embed:
  """Return a discord embed
  
  title -- the embed's title
  desc -- the embed's description
  fields -- a list of `(name, value, inline?)` tuples that should be added
  colour -- the embed's colour
  """
  embed = discord.Embed(title=title, description=desc, colour=colour)
  add_tuple(embed, fields)
  return embed

def create_error_embed(desc: str) -> discord.Embed:
  """Return an embed with an error.
  
  desc -- the description of the embed"""
  return create_embed('A apărut o eroare', desc, [], RED)

def create_problem_embed(title: str, data: dict) -> discord.Embed:
  """Return an embed representing problem data.

  title -- the title of the embed
  data -- the problem data
  """

  desc = data['categories']+'\n\n'
  if data['source']:
    desc += data['source']+'\n'
  if data['author']:
    desc += f'Autor: {data["author"]}\n'
  desc += f'Limită timp: `{data["time"]}s`\nLimită memorie: `{data["memory"]}MB`'

  embed = create_embed(title, desc, data['headers'], colour=LIGHT_BLUE)
  if data['poster']:
    embed.set_footer(text=f'Postată de {data["poster"][0]}', icon_url=data['poster'][1])
  return embed
