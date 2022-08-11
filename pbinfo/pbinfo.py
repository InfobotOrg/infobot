import aiohttp
from bs4 import BeautifulSoup
import re
import util.util as util

async def get_problem(id: int):
  URL = f'https://www.pbinfo.ro/probleme/{str(id)}'
  
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as page:
      if page.status != 200:
        return {'error': page.status}

      soup = BeautifulSoup(await page.text(), 'html.parser')
      data = dict.fromkeys(['error', 'categories', 'name', 'author', 'solutions', 'statement', 'task', 'input', 'output', 'file_in', 'in_example', 'file_out', 'out_example', 'example'])
      data['id'] = id

      # Change format of code tags
      for code in soup.find_all('code'):
        code.string = f'`{code.string}`'

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
        data['name'] = name_header.find('a').get_text()
      author = soup.find('span', class_='pbi-widget-user pbi-widget-user-span')
      if author:
        data['author'] = (author.get_text(), author.find('img')['src'])
      data['solutions'] = soup.find('span', class_='badge').get_text()

      article = soup.find('article', id='enunt')
      if article:
        data['statement'] = util.text_find_next_until(article, 'h1')
      task_header = soup.find('h1', text=re.compile('Cerin.a'))
      if task_header:
        data['task'] = util.text_find_next_until(task_header, 'h1')

      input_header = soup.find('h1', text='Date de intrare')
      output_header = soup.find('h1', text=re.compile('Date de ie.ire'))
      if input_header:
        if not output_header: # some problems have typos (ex. https://www.pbinfo.ro/probleme/1436)
          output_header = input_header.find_next_sibling('h1')
        if output_header:
          data['input'] = util.text_find_next_until(input_header, ['h1'])
          data['output'] = util.text_find_next_until(output_header, ['h1'])

      example_header = soup.find('h1', text=re.compile('Exemplu+'))
      if example_header:
        editableIn = example_header.find_next_sibling('pre')
        if editableIn:
          editableOut = editableIn.find_next_sibling('pre')
          if editableOut:
            data['file_in'] = editableIn.find_previous('p').get_text()
            data['in_example'] = editableIn.get_text()
            data['file_out'] = editableOut.find_previous('p').get_text()
            data['out_example'] = editableOut.get_text()
        if not data['file_in']:
          example = example_header.find_next_sibling('p')
          if example:
            data['example'] = example.get_text()

      for k, v in data.items():
        if type(v) == tuple:
          data[k] = (util.prettify(v[0]), util.prettify(v[1]))
        elif isinstance(v, str):
          data[k] = util.prettify(v)
      return data

async def get_account(name: str):
  URL_DOC = f'https://www.pbinfo.ro/profil/{name}'
  URL_PB = 'https://www.pbinfo.ro/ajx-module/profil/json-jurnal.php'

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
      data['avatar'] = 'https://www.pbinfo.ro' + soup.find('div', class_='center padding18').find('img')['src']
      data['goal'] = 'https://www.pbinfo.ro' + soup.find('div', class_='panel-heading center').find('img')['src']
      data['success'] = soup.find('span', string='succes (%)').find_previous('span').get_text()
      
      async with session.get(URL_PB, params={'user': name}) as req:
        pbjson = await req.json(content_type='text/html')
        data['problems'] = pbjson['content']
        for k, v in data.items():
          if isinstance(v, str):
            data[k] = util.prettify(v)
        return data

def process_problems(problems: list):
  data = {}

  data['total'] = len(problems)
  data['total_solved'] = set()
  data['total_tried'] = set()
  data['solved'] = {'9': set(), '10': set(), '11': set()}
  data['tried'] = {'9': set(), '10': set(), '11': set()}

  for problem in problems:
    if (int(problem['scor']) == 100):
      data['solved'][problem['clasa']].add(problem['id'])
      data['total_solved'].add(problem['id'])
    else:
      data['tried'][problem['clasa']].add(problem['id'])
      data['total_tried'].add(problem['id'])
  
  for cls in range(9, 12):
    data['tried'][str(cls)] = data['tried'][str(cls)].difference(data['solved'][str(cls)])
  data['total_tried'] = data['total_tried'].difference(data['total_solved'])


  return data
