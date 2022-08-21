import aiohttp

BASE = 'https://api.github.com'
OWNER = 'RolandPetrean'
REPO = 'infobot'

# https://docs.github.com/en/rest/repos/repos#list-repository-contributors
async def get_contributors() -> list:
  """Return the names and profile urls of the contributors of a repository."""
  async with aiohttp.ClientSession() as session:
    async with session.get(f'{BASE}/repos/{OWNER}/{REPO}/contributors') as req:
      contributors = await req.json()
      return [(contrib['login'], contrib['html_url']) for contrib in contributors]
