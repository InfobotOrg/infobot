import aiohttp
import json

async def get_profile(username):
  URL = 'https://api.solinfo.ro/v2.0/endpoint/page/profil'

  async with aiohttp.ClientSession() as session:
    async with session.post(URL, data=json.dumps({'username': username})) as req:
      return await req.json()

async def get_solution(name):
  URL_PB = 'https://api.solinfo.ro/v2.0/endpoint/page/problema'
  URL_SOL = 'https://api.solinfo.ro/v2.0/endpoint/page/problema-solutie'

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
