import sys
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

ARCHIVES = {
  'pb': 'https://www.infoarena.ro/arhiva',
  'edu': 'https://www.infoarena.ro/arhiva-educationala',
  'monthly': 'https://www.infoarena.ro/arhiva-monthly',
  'acm': 'https://www.infoarena.ro/arhiva-acm',
  'varena': 'https://www.varena.ro'
}

async def generate(filename: str):
  """Generate a JSON file that contains infoarena problem data."""

  data = {}
  for archive_name, url in ARCHIVES.items():
    sys.stdout.write(f'=> Generating "{archive_name}" archive problem data (')

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as start_req:
        start_soup = BeautifulSoup(await start_req.read(), 'lxml')
        total = int(start_soup.find('span', class_='count').get_text().split('(')[1].split(' ')[0])
        total = int(total/250)+1
        for i in range(total):
          async with session.get(url+f'?display+entries=250&first_entry={250*i}') as req:
            soup = BeautifulSoup(await req.read(), 'lxml')
            tasks = soup.find_all('td', class_='task')
            for task in tasks:
              task = task.find('a')
              id = task['href'].split('/')[2]
              data[f'{archive_name}${id}'] = task.get_text()
          sys.stdout.write(f'{i+1}/{total})')
          sys.stdout.flush()
          sys.stdout.write('\b'*(len(str(i+1)) + len(str(total)) + 2))
    sys.stdout.write('\n')
  json.dump(data, open('output/infoarena.json', 'w'))
  print('Done!')

if __name__ == '__main__':
  filename = sys.argv[1] if len(sys.argv) > 1 else 'output/infoarena.json'
  asyncio.run(generate(filename))