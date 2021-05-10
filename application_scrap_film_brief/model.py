import urllib.request
from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests
import re
import sqlite3
from sqlite3 import connect

def connexion():
  conn = connect('/Users/hugofugeray/Desktop/formaIA/scrap/scrap_imbd_rendu/application_scrap_film_brief/film.db')
  curs = conn.cursor()
  return conn, curs

def create_table():
  conn,curs = connexion()
  try:
    curs.execute('''DROP TABLE Film;''')
    print('DROP TABLE --> OK')
  except :
    print('DROP TABLE --> ERROR')

  curs.execute('''CREATE TABLE IF NOT EXISTS Film (
  id  INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  year INTEGER,
  certificate TEXT,
  duration INTEGER,
  genre TEXT,
  score REAL,
  rate INTEGER,
  directors TEXT,
  recette VARCHAR)'''
  );

  conn.commit()
  conn.close()

def scrapping(urls):
  conn, curs =connexion()
  for url in urls:
      response = requests.get(url)
      if response.ok:
          soup = BeautifulSoup(response.text,'html.parser')
      else:
          print(f'L\'erreur {reponse.status_code} s\'est produite')
      movies_html = soup.find_all('div', 'lister-item')
      movies_list = []
      for info in movies_html:
          title = info.find('h3', attrs={'class':'lister-item-header'})
          title_1 = title.find('a')
          title_2 = title_1.text
          year = info.find('h3', attrs={'class':'lister-item-header'})
          year_1 = year.find('span', attrs={'class':'lister-item-year'})
          year_2 = year_1.text.replace('(', '').replace(')', '').replace('I ','')
          year_2 = int(year_2)
          certificate = info.find('span',{"class": "certificate"})
          if certificate is not None:
              certificate = certificate.text
          duration = info.find('span',{"class": "runtime"})
          duration_1 = duration.text.replace(' min', '')
          genre = info.find('span',{"class": "genre"})
          genre_1 =genre.text.replace('\n', '')
          score = info.find('div', attrs={'class':'inline-block ratings-imdb-rating'})
          score_1 = score.find('strong')
          score_2 = score_1.text
          rate = info.find('p', class_='sort-num_votes-visible').contents[3].attrs['data-value']
          film_director = info.find('p', class_='').text
          directors = film_director.split(':')[1]
          directors_1 = directors.split('|')[0].replace('\n', '')
          for recette in soup.find_all('p', class_='sort-num_votes-visible'):
              try:
                recette = info.find('p', class_='sort-num_votes-visible').contents[9].attrs['data-value'].replace(',','')
                recette = int(recette)
              except IndexError:
                recette = None
          curs.execute("INSERT INTO Film (title, year, certificate, duration, genre, score, rate, directors, recette) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (title_2, year_2, certificate, duration_1, genre_1, score_2, rate, directors, recette))
          conn.commit()
