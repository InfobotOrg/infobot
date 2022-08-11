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