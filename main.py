"""
batatinha quando nasce
esparalhama pelo chão 
menino quando dorme 
bota a mão no coração
o:
"""

import re
from PyPDF2 import PdfFileReader
import math

REGEX_TABLE = r'(?P<table>\d+) (?P<player1>[\w ]+) (\d+\.\d) (?P<result>1-0|0-1|0.5-0.5) (\d+\.\d) (?P<player2>[\w ]+)'

K = 40

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
    rating = int(input(f"Diga me o rating do jogador {name}: "))

    ratings[name] = rating

  return ratings

def probability(rating1, rating2):
  if rating1 - rating2 > 400:
    return 0
  elif rating1 - rating2 < - 400:
    return 1

  return 1 / (1 + math.pow(10,(rating1 - rating2) / 400))
 
 
def calc_rating(games, ratings):
  rating_final = {}

  for name, games in games.items():
    rating1 = ratings[name]
    delta_rating = 0

    print('jogador:', name)

    for game in games:
      rating2 = ratings[game["opponent"]]
      result = game["result"]

      delta_rating += round((result - probability(rating2, rating1)) * K,  1)

    rating_final[name] = rating1 + delta_rating
  return rating_final

def main(path):
  pdf_text = extract_information(path)
  
  games = get_results(pdf_text)

  ratings = get_inputs(games)
  
  rating_final = calc_rating(games, ratings)
  print(rating_final)
if __name__ == '__main__':
  main('./axs31.pdf')
