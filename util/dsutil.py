import discord

LIGHT_BLUE = 0xADD8FF
RED = 0xFF0000

def create_embed(title: str, desc: str, fields, colour) -> discord.Embed:
  embed = discord.Embed(title=title, description=desc, colour=colour)
  for field in fields:
    embed.add_field(name=field[0], value=field[1], inline=False)
  return embed

def create_error_embed(desc: str) -> discord.Embed:
  return create_embed('A apărut o eroare', desc, [], RED)

def add_data(embed: discord.Embed, name: str, value, inline=False):
  if value:
    embed.add_field(name=name, value=value, inline=inline)