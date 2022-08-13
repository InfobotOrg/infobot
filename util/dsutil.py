import discord

LIGHT_BLUE = 0xADD8FF
RED = 0xFF0000

def add_data(embed: discord.Embed, name: str, value, inline=False):
  if value:
    embed.add_field(name=name, value=value, inline=inline)

def create_embed(title: str, desc: str, fields, colour) -> discord.Embed:
  embed = discord.Embed(title=title, description=desc, colour=colour)
  for field in fields:
    inline = False
    if (len(field) == 3):
      inline = field[2]
    add_data(embed, field[0], field[1], inline=inline)
  return embed

def create_error_embed(desc: str) -> discord.Embed:
  return create_embed('A apărut o eroare', desc, [], RED)

def create_problem_embed(name, data) -> discord.Embed:
  embed = create_embed(name, data['categories'], [
    ('Enunț', data['statement']),
    ('Cerința', data['task']),
    ('Date de intrare', data['input']),
    ('Date de ieșire', data['output']),
    ('Exemplu', data['example'])
  ], colour=LIGHT_BLUE)
  if data['file_in']:
    add_data(embed, name='Exemplu', value=f'**{data["file_in"].replace("`", "")}**\n```{data["in_example"]}```\n**{data["file_out"].replace("`", "")}**\n```{data["out_example"]}```')
  if data['author']:
    embed.set_footer(text=f'Postată de {data["author"][0]}', icon_url=data['author'][1])
  return embed
