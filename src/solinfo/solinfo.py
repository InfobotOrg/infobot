import aiohttp
import json

BASE = 'https://api.solinfo.ro/v2.0/endpoint'

async def get_profile(username: str) -> dict:
  """Return data about a solinfo account.
  
  username - the name of the account
  """

  URL = f'{BASE}/page/profil'

  async with aiohttp.ClientSession() as session:
    async with session.post(URL, data=json.dumps({'username': username})) as req:
      pfjson = await req.text()
      return json.loads(pfjson)

async def get_solution(name: str) -> dict:
  """Return data about a pbinfo problem's solution.
  
  name - the name of the problem
  """

  URL_PB = f'{BASE}/page/problema'
  URL_SOL = f'{BASE}/page/problema-solutie'

  async with aiohttp.ClientSession() as session:
    async with session.post(URL_PB, data=json.dumps({'name': name})) as pb:
      pbjson = await pb.text()
      pbjson = json.loads(pbjson)
      solutions = pbjson['solutions']
      if (len(solutions) == 0):
        return [], ''
      solID = solutions[0]['id']
      async with session.post(URL_SOL, data=json.dumps({'solutionId': solID})) as sol:
        soljson = await sol.text()
        soljson = json.loads(soljson)
        return solutions, soljson['content']
