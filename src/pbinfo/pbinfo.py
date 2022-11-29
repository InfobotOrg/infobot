import aiohttp
from bs4 import BeautifulSoup
import re
import util.util as util

BASE = 'https://www.pbinfo.ro'

async def get_problem(id: int) -> dict:
  """Return data about a pbinfo problem.
  
  id -- the problem's id
  """

  URL = f'{BASE}/probleme/{str(id)}'
  
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as page:
      if page.status != 200:
        return {'error': page.status}

      text = await page.text()
      soup = BeautifulSoup(text, 'lxml')
      data = dict.fromkeys(['error', 'time', 'memory', 'source', 'author', 'categories', 'name', 'poster', 'solutions'])
      data['id'] = id

      util.prettifySoup(soup, 'problema-wrapper')
      article = soup.find('article', id='enunt')

      infotable = soup.find('table', class_='table-bordered')
      if infotable:
        time = infotable.find('tr').find_next('tr').find('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')
        data['time'] = util.prettify(time.get_text().split(' ')[0])
        data['memory'] = util.prettify(time.find_next_sibling('td').get_text().split(' ')[0])+'.0'
        data['source'] = util.prettify(time.find_next_sibling('td').find_next_sibling('td').get_text())
        data['author'] = util.prettify(time.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').get_text())
        
        if data['source'] == '-':
          data['source'] = None
        if data['author'] == '-':
          data['author'] = None

      categories = soup.find('ol', class_='breadcrumb')
      if categories:
        categories_text = []
        for category in categories.find_all('li'):
          categories_text.append(util.prettify(category.get_text()))
        categories_text[-1] = f'*{categories_text[-1]}*'
        categories_text = '->'.join(categories_text)
        data['categories'] = categories_text

      name_header = soup.find('h1', class_='text-primary')
      if name_header:
        data['name'] = util.prettify(name_header.find('a').get_text())
      poster = soup.find('span', class_='pbi-widget-user pbi-widget-user-span')
      if poster:
        data['poster'] = (util.prettify(poster.get_text()), poster.find('img')['src'])
      data['solutions'] = soup.find('span', class_='badge').get_text()

      data['headers'] = [('Enunț', util.prettify(util.text_find_next_until(article.find(), 'h1')))]
      headers = article.find_all('h1')
      for header in headers:
        data['headers'].append((header.get_text(), util.prettify(util.text_find_next_until(header, 'h1'))))

      return data

async def get_account(name: str):
  """Return data about a pbinfo account.
  
  name -- the account's name
  """

  URL_DOC = f'{BASE}/profil/{name}'
  URL_PB = f'{BASE}/ajx-module/profil/json-jurnal.php'

  async with aiohttp.ClientSession() as session:
    async with session.get(URL_DOC) as page:
      if page.status != 200:
        return {'error': page.status}
      soup = BeautifulSoup(await page.text(), 'html.parser')
      data = {'error': None}

      last_name = soup.find('div', class_='well well-sm center').find('h2').find('span')
      data['last_name'] = last_name.get_text()
      data['first_name'] = last_name.find_next_sibling('span').get_text()
      data['display_name'] = f'{data["first_name"]} {data["last_name"]}'
      data['avatar'] = BASE + soup.find('div', class_='center padding18').find('img')['src']
      data['goal'] = BASE + soup.find('div', class_='panel-heading center').find('img')['src']
      data['success'] = soup.find('span', string='succes (%)').find_previous('span').get_text()
      
      async with session.get(URL_PB, params={'user': name}) as req:
        pbjson = await req.json(content_type='text/html')
        data['problems'] = pbjson['content']
        for k, v in data.items():
          if isinstance(v, str):
            data[k] = util.prettify(v)
        return data

def process_problems(problems: list) -> dict:
  """Calculate relevant data from a list of problems."""
  
  data = {'total_solved': [], 'total_tried': [], 'solved': {'9': [], '10': [], '11': []}, 'tried': {'9': [], '10': [], '11': []}}
  
  for problem in problems: # Solved problems
    problem.pop('data_upload') # We don't care about the date, and it messes up containment checks
    if int(problem['scor']) == 100:
      problem.pop('scor') # Same thing, don't need score after this point
      if problem not in data['total_solved']:
        data['solved'][problem['clasa']].append(problem)
        data['total_solved'].append(problem)
  
  for problem in problems: # Unsolved problems
    if 'scor' in problem:
      problem.pop('scor') # In the previous step only problems with 100 points got the score removed
    if problem not in data['total_solved'] and problem not in data['total_tried']:
      data['tried'][problem['clasa']].append(problem)
      data['total_tried'].append(problem)
  
  data['total_sub'] = len(problems)
  data['total'] = data['total_solved'] + data['total_tried']
  return data