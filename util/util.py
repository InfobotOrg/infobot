import re


def prettifySoup(soup, id):
  div = soup.find('div', id=id)

  # Change format of tags
  for sub in div.find_all('sub'):
    sub.string = f'[{sub.get_text()}]'

  for var in div.find_all('var'):
    var.string = f'`{var.get_text()}`'
  for code in div.find_all('code'):
    code.string = f'`{code.get_text()}`'
  for jax in div.find_all('span', class_='MathJax'):
    jax.string = f'`{jax.get_text()}`'
  for li in div.find_all('li'):
    li.string = f'- {li.get_text()}'

def prettify(text: str, length=330) -> str:
  while '  ' in text:
    text = text.replace('  ', ' ')
  text = text.strip()
  if text == '':
    return None
  if text[-1] in ':;':
    text = text[:-1]
  return f'{text[:length]}...' if len(text) > length+3 else text

def text_find_next_until(el, end_t):
  text = ''

  sbs = el.find_next_siblings()
  for s in sbs:
    if s.name in end_t:
      break
    if s.name == 'p':
      text += '\n'
    text += s.get_text()

  return text