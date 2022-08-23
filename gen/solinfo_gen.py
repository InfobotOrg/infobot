import sys
import aiohttp
import asyncio
import json

async def generate(filename: str):
  """Generate a JSON file that contains solinfo problem data."""

  sys.stdout.write('=> Generating solinfo problem data (')
  data = {}
  async with aiohttp.ClientSession() as session:
    async with session.get('https://api.solinfo.ro/v2.0/endpoint/problems.json') as req:
      content = await req.json()
      for i in range(len(content)):
        data[content[i]['name']] = content[i]['id']
        sys.stdout.write(f'{i}/{len(content)-1})')
        sys.stdout.flush()
        sys.stdout.write('\b'*(len(str(i)) + len(str(len(content))) + 2))
  json.dump(data, open(filename, 'w'))
  print('\nDone!')

if __name__ == '__main__':
  filename = sys.argv[1] if len(sys.argv) > 1 else 'output/solinfo.json'
  asyncio.run(generate(filename))