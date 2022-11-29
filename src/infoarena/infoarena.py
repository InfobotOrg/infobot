import aiohttp
from bs4 import BeautifulSoup
import re
import util.util as util

BASE = 'https://www.infoarena.ro'
VARENA_BASE = 'https://www.varena.ro'

async def get_problem(name: str, archive: str):
  """Return data about an infoarena problem.
  
  name -- the problem's name
  archive -- the archive to which the problem belongs
  """

  base = VARENA_BASE if archive == 'varena' else BASE
  URL = f'{base}/problema/{name}'
  
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as page:
      if page.status != 200:
        return {'error': page.status}

      soup = BeautifulSoup(await page.text(), 'lxml')
      data = dict.fromkeys(['error', 'time', 'memory', 'source', 'author', 'categories', 'name', 'poster'])
      data['categories'] = util.get_category(archive)
      
      main = soup.find('div', id='main')
      infotable = main.find('table')
      if infotable:
        data['source'] = util.prettify(infotable.find('tr').find('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').get_text())
        data['author'] = util.prettify(infotable.find('tr').find_next_sibling('tr').find('td').find_next_sibling('td').get_text())
        data['time'] = util.prettify(infotable.find('tr').find_next_sibling('tr').find_next_sibling('tr').find('td').find_next_sibling('td').get_text().split(' ')[0])
        data['memory'] = str(int(int(infotable.find('tr').find_next_sibling('tr').find_next_sibling('tr').find('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').get_text().split(' ')[0])/100)/10)
      
      util.prettifySoup(soup, 'main')

      name_header = soup.find('h1').find_next('h1')
      if name_header:
        data['name'] = util.prettify(name_header.get_text())
      poster = soup.find('span', class_='tiny-user')
      if poster:
        poster_username = soup.find('span', class_='username').get_text()
        data['poster'] = (f'{poster.find("a").get_text()} ({poster_username})', base+poster.find('img')['src'])

      data['headers'] = [('Enunț', util.prettify(util.text_find_next_until(name_header, 'h2')))]
      headers = main.find_all('h2')
      for header in headers:
        if header.get_text() == 'Exemplu':
          break
        data['headers'].append((header.get_text(), util.prettify(util.text_find_next_until(header, 'h2'))))

      return data

async def get_account(name: str, varena: bool):
  """Return data about an infoarena account.
  
  name -- the account's name
  varena -- whether the account is on varena"""

  base = VARENA_BASE if varena else BASE
  URL = f'{base}/utilizator/{name}?action=stats'

  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as page:
      if page.status != 200 or 'utilizator' not in str(page.url):
        return {'error': page.status}

      data = {'error': None}
      soup = BeautifulSoup(await page.text(), 'lxml')
      util.prettifySoup(soup, 'main')

      mainblock = soup.find('div', id='main')
      infotable = mainblock.find('div', class_='wiki_text_block').find('table')

      data['avatar'] = f'{base}/avatar/full/{name}'
      data['display_name'] = infotable.find('tr').find('td').find_next_sibling('td').get_text()
      data['rating'] = infotable.find('tr').find_next_sibling('tr').find_next_sibling('tr').find('td').get_text()
      data['statut'] = infotable.find('tr').find_next_sibling('tr').find_next_sibling('tr').find_next_sibling('tr').find('td').get_text()
      
      data['solved'] = mainblock.find('span', class_='task_enum').get_text().split('Total: ')[1].split(' ')[0]
      data['unsolved'] = mainblock.find('h3', text='Probleme incercate').find_next('span', class_='task_enum').get_text().split('Total: ')[1].split(' ')[0]

      return data
  
async def get_monitor(user: str, task: str, varena: bool):
  """Return data about the infoarena monitor
  
  user -- a specific user
  task -- a specific problem's name
  varena -- whether the monitor is varena's"""

  base = VARENA_BASE if varena else BASE
  URL = f'{base}/monitor?only_table=1&first_entry=0&display_entries=15&user={user}&task={task}'

  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as page:
      if page.status != 200:
        return {'error': page.status}
      
      data = {'error': None, 'evals': []}
      soup = BeautifulSoup(await page.text(), 'lxml')

      table = soup.find('table', class_='monitor')
      if not table:
        return {'error': 404}
      monitor = table.find('tbody')
      rows = monitor.find_all('tr')

      for row in rows:
        curr = {}

        user = row.find('td').find_next_sibling('td').find('span', class_='tiny-user')
        task = row.find('td').find_next_sibling('td').find_next_sibling('td')
        curr['id'] = row.find('td').get_text().split('#')[1]
        curr['display_name'] = user.find('a').get_text()
        curr['username'] = user.find('span').get_text()
        curr['task'] = util.prettify(task.get_text(), 20)
        curr['task_link'] = task.find('a')['href'].lower().split('/problema/')[1]
        curr['points'] = row.find('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').get_text()
        if ':' not in curr['points']:
          curr['points'] = '???'
        else:
          curr['points'] = curr['points'].split(': ')[1].split(' ')[0]

        data['evals'].append(curr)
      
      return data