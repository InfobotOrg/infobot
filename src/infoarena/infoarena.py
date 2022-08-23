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
      data = dict.fromkeys(['error', 'categories', 'name', 'statement', 'author', 'task', 'input', 'output', 'file_in', 'in_example', 'file_out', 'out_example', 'example'])

      util.prettifySoup(soup, 'main')

      # Didn't use a match statement because it is only supported in Python 3.10+
      if archive == 'pb':
        data['categories'] = '*Arhiva de probleme*'
      elif archive == 'edu':
        data['categories'] = '*Arhiva educațională*'
      elif archive == 'monthly':
        data['categories'] = '*Arhiva monthly*'
      elif archive == 'acm':
        data['categories'] = '*Arhiva ACM*'
      elif archive == 'varena':
        data['categories'] = '*Arhiva de probleme varena'

      name_header = soup.find('h1').find_next('h1')
      if name_header:
        data['name'] = name_header.get_text()
        data['statement'] = util.text_find_next_until(name_header, ['h2'])
      author = soup.find('span', class_='tiny-user')
      if author:
        author_username = soup.find('span', class_='username').get_text()
        data['author'] = (f'{author.find("a").get_text()} ({author_username})', base+author.find('img')['src'])

      task_header = soup.find('h2', text=re.compile('Cerin.a'))
      if task_header:
        data['task'] = util.text_find_next_until(task_header, ['h2'])
        if data['statement'] == data['task']:
          data['statement'] = None

      input_header = soup.find('h2', text='Date de intrare')
      output_header = soup.find('h2', text=re.compile('Date de ie.ire'))
      if input_header and output_header:
        data['input'] = util.text_find_next_until(input_header, ['h2'])
        data['output'] = util.text_find_next_until(output_header, ['h2', 'table'])

      example_table = soup.find('table', class_='example')
      if example_table:
        file_in = example_table.find('tr').find('th')
        data['file_in'] = file_in.get_text()
        data['file_out'] = file_in.find_next_sibling('th').get_text()
        in_example = example_table.find('tr').find_next_sibling('tr').find('td')
        data['in_example'] = in_example.get_text()
        data['out_example'] = in_example.find_next_sibling('td').get_text()

      for k, v in data.items():
        if type(v) == tuple:
          data[k] = (util.prettify(v[0]), util.prettify(v[1]))
        elif v:
          data[k] = util.prettify(v)
      return data
