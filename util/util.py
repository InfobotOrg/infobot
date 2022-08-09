def prettify(text: str, length=300) -> str:
  while '  ' in text:
    text = text.replace('  ', ' ')
  text = text.strip()
  return f'{text[:length]}...' if len(text) > length+3 else text
