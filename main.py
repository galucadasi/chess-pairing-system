"""
batatinha quando nasce
esparalhama pelo chão 
menino quando dorme 
bota a mão no coração
o:
"""

import re
from PyPDF2 import PdfFileReader

REGEX_TABLE = r'(?P<table>\d+) (?P<player1>[\w ]+) (\d+\.\d) (?P<result>1-0|0-1|0.5-0.5) (\d+\.\d) (?P<player2>[\w ]+)'

def extract_information(pdf_path):
    file_content = ''
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)

        for i in range(pdf.numPages):
            current_page = pdf.getPage(i)
            file_content += current_page.extractText()
    return file_content

def get_results(pdf_text):
  games = {}

  for pdf_line in pdf_text.split('\n'):
    match = re.match(REGEX_TABLE, pdf_line)

    if match is None:
      continue

    player1= match.group('player1')
    player2= match.group('player2')
    result = match.group('result')
    player1_res, player2_res = result.split('-')
    player1_res, player2_res = float(player1_res), float(player2_res)

    if player1 not in games:
      games[player1] = []

    games[player1].append({
      "opponent": player2,
      "result": player1_res
    })

    if player2 not in games:
      games[player2] = []

    games[player2].append({
      "opponent": player1,
      "result": player2_res
    })

  return games

def get_inputs(games):
  ratings = {}

  for name in games:
    rating = int(input(f"Diga me o rating do jogador {name}"))

    ratings[player1] = rating

  return ratings

def main(path):
  pdf_text = extract_information(path)

  print(pdf_text)
  
  games = get_results(pdf_text)

  ratings = get_inputs(games)

if __name__ == '__main__':
  main('./axs30.pdf')
