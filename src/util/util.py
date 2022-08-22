import bs4

def prettifySoup(soup: bs4.BeautifulSoup, id: str):
  """Format page elements under a certain id so they look better on Discord.
  
  soup -- the BeautifulSoup
  id -- the id of the starting element
  """

  div = soup.find(id=id)

  # Change format of tags
  for em in div.find_all('em'):
    em.string = f'*{em.get_text()}*'
  for i in div.find_all('i'):
    i.string = f'*{i.get_text()}*'
  for sub in div.find_all('sub'):
    sub.string = f'[{sub.get_text()}]'
  for var in div.find_all('var'):
    var.string = f'`{var.get_text()}`'
  for code in div.find_all('code'):
    code.string = f'`{code.get_text()}`'
  #for jax in div.find_all('span', class_='MathJax'): # TODO https://github.com/RolandPetrean/infobot/issues/5
  #  jax.string = f'`{jax.get_text()}`'
  for li in div.find_all('li'):
    li.string = f'- {li.get_text()}'

def prettify(text: str, length: int = 350) -> str:
  """Format text.

  text -- the text to format
  length -- the maximum length of the resulting text (default 350)
  """

  while '  ' in text:
    text = text.replace('  ', ' ')
  text = text.strip()
  if text == '':
    return None
  if text[-1] in ':;':
    text = text[:-1]
  return f'{text[:length]}...' if len(text) > length+3 else text

def text_find_next_until(el: bs4.element.PageElement, end_t: str) -> str:
  """Return the concatenated text of all siblings of an element until a certain tag is found.

  el -- the starting BeautifulSoup element
  end_t -- the name of the final tag
  """

  text = ''

  sbs = el.find_next_siblings()
  for s in sbs:
    if s.name in end_t:
      break
    if s.name == 'p':
      text += '\n'
    text += s.get_text()

  return text