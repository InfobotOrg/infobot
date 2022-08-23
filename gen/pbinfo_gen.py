import sys
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

MAX_PB = 4200 # Increase if needed

async def generate(filename: str):
  """Generate a JSON file that contains pbinfo problem data."""

  sys.stdout.write('=> Generating pbinfo problem data (')
  data = {}
  for i in range(MAX_PB):
    async with aiohttp.ClientSession() as session:
      async with session.get(f'https://www.pbinfo.ro/probleme/{i}') as req:
        if req.status == 200:
          content = await req.read()
          soup = BeautifulSoup(content, 'lxml')
          name = soup.find('h1', class_='text-primary').find('a').get_text().strip()
          data[name] = i
    sys.stdout.write(f'{i}/{MAX_PB})')
    sys.stdout.flush()
    sys.stdout.write('\b'*(len(str(i)) + 6))
  
  json.dump(data, open(filename, 'w'))
  print('\nDone!')

if __name__ == '__main__':
  filename = sys.argv[1] if len(sys.argv) > 1 else 'output/pbinfo.json'
  asyncio.run(generate(filename))