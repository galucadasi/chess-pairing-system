"""
batatinha quando nasce
esparalhama pelo chão 
menino quando dorme 
bota a mão no coração
o:
"""

import re
from PyPDF2 import PdfFileReader

#declaring variáveis 
k=40
#diff is change
list_diff1 = []
list_diff2 = []
#Ganbiarra 
rating1 = 1500
rating2 = 1500

#Lists
player_list_rating = []
list_players = []
list_player1_res = []
list_player2_res = []

#regex config:
REGEX_TABLE = r'(?P<table>\d+) (?P<player1>[\w ]+) (\d+\.\d) (?P<result>1-0|0-1|0.5-0.5) (\d+\.\d) (?P<player2>[\w ]+)'
 
#Interacao com o usuario
def main_menu():
  #recolhe o numero de usuarios
  num_players = int(input('Número de jogadores:'))
  # rating = int(input(''))
  return num_players

#Recolhe o rating does jogadores
def get_rating_player(num_players,player_list_rating, list_players):
  count_num_players = num_players
  while count_num_players > 0:
    player_rating = input('Digite o rating do jogador:', list_players[count_num_players])
    player_list_rating.append(player_rating )
    count_num_players -= 1
  
  print(player_list_rating)
  return player_list_rating
#Pegar texto do pdf 
def extract_information(pdf_path):
    file_content = ''
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)

        for i in range(pdf.numPages):
            current_page = pdf.getPage(i)
            file_content += current_page.extractText()
    return file_content

#Pega os resultados de todas as mesas de uma rodada
def get_results(pdf_text, num_players):
  pdf_lines = pdf_text.split('\n')
  lines=0

  #Adicionar o sistema que compreende o que é uma linha valida
  pdf_lines_1char = pdf_lines[num_players].split()
  print (pdf_lines_1char)
  """
  if isinstance(pdf_lines_1char, int):
    print('Is integer')
  """
  while lines < num_players:
#add an if to check if it is the first round to get the players
    match = re.match(REGEX_TABLE, pdf_lines[7])
    
    player1= match.group('player1')
    player2= match.group('player2')
    result = match.group('result')
    if result == '1-0':
      player1_res = 1
      player2_res = 0
    elif result == '0-1':
      player1_res = 0
      player2_res = 1
    elif result == '0.5-0.5':
      player1_res = 0.5
      player2_res = 0.5
    else:
      player1_res = 10
      player2_res = 10
      print('Not found result')
      lines =+1
    list_player1_res.append(player1_res)
    list_player2_res.append(player2_res)    

#list_players.append(player1,player2)
    return list_player1_res, list_player2_res, list_players

#Recebe o resultado e os ratings é devolve a variação 
"""
def calc_rating(rating1, rating2, player1_res, player2_res):
  player1_diff = k*(player1_res[0]-(rating1/(rating1+rating2)))
  player2_diff = k*(player2_res[0]-(rating2/(rating1+rating2)))
  print(player1_diff, player2_diff)
  return player1_diff, player2_diff
"""
# Função principal
def main():
  #diz o caminho do arquivo / automatizar isso dps
  path = './axs30.pdf'
  #Chama a função que extrai o texto do pdf
  pdf_text = extract_information(path)
  #print(pdf_text)
  
  #Chama a função que recebe as informações base do usuario
  num_players = main_menu()
  #Isso realmente converte para uma int?
  num_players = int(num_players)
  #Chama a função que pega o resultado da rodada 
  list_player1_res, list_player2_res, list_players  = get_results(pdf_text,num_players)
  
#Chama a função que recolhe o rating dos jogadores
  get_rating_player(num_players,player_list_rating, list_players)

#Chama a função que calcula o diff
#player1_diff, player2_diff = calc_rating(rating1, rating2, list_player1_res, list_player2_res)

""""
def get_rating_player(num_players,player_list_rating):
  player1_diff, player2_diff= calc_rating(rating1, rating2, player1_res, player2_res)
  list_diff1.append(player1_diff)
  list_diff2.append(player2_diff)
  print(list_diff1, list_diff2)
"""

if __name__ == '__main__':
  main()
