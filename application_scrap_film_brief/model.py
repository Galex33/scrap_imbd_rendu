import urllib.request
from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests
import re
import sqlite3
from sqlite3 import connect



def connexion():


  conn = connect('/Users/hugofugeray/Desktop/formaIA/scrap/application_scrap_film_brief/film.db')
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
  titre TEXT,
  annee INTEGER,
  certificate TEXT,
  Duree INTEGER,
  genre TEXT,
  note REAL,
  avis INTEGER,
  directors TEXT,
  recette VARCHAR)'''
  );

  conn.commit()
  conn.close()




def scrapping(urls):

  conn, curs =connexion()

  for url in urls:
      response = requests.get(url)



      #Si reponse ok recuperation du html

      if response.ok:

          soup = BeautifulSoup(response.text,'html.parser')

      else:

          print(f'L\'erreur {reponse.status_code} s\'est produite')

      movies_html = soup.find_all('div', 'lister-item')
      movies_list = []

      for info in movies_html:



          title = info.find('h3', attrs={'class':'lister-item-header'})
          title1 = title.find('a')
          title2 = title1.text

          # movies_list.append(title.text)

          date = info.find('h3', attrs={'class':'lister-item-header'})
          date1 = date.find('span', attrs={'class':'lister-item-year'})
          date2=date1.text.replace('(', '').replace(')', '').replace('I ','')
          date2 = int(date2)


          # movies_list.append(date.text.replace('(','').replace(')',''))

          certificate = info.find('span',{"class": "certificate"})
          if certificate is not None:
              certificate = certificate.text

          # movies_list.append(certificate)

          time = info.find('span',{"class": "runtime"})
          time1=time.text.replace(' min', '')

          # movies_list.append(time.text.replace(' min', ''))

          genre = info.find('span',{"class": "genre"})
          genre1=genre.text.replace('\n', '')

          # movies_list.append(genre.text.replace('\n', '').replace(' ', ''))

          note = info.find('div', attrs={'class':'inline-block ratings-imdb-rating'})
          note1 = note.find('strong')
          note2=note1.text

          # movies_list.append(note.text)

          votes = info.find('p', class_='sort-num_votes-visible').contents[3].attrs['data-value']
          film_director = info.find('p', class_='').text
          direc = film_director.split(':')[1]
          direc1 = direc.split('|')[0].replace('\n', '')

          for gross in soup.find_all('p', class_='sort-num_votes-visible'):


              try:
                gross = info.find('p', class_='sort-num_votes-visible').contents[9].attrs['data-value'].replace(',','')
                gross = int(gross)
              except IndexError:
                gross = None

          curs.execute("INSERT INTO Film (titre, annee, certificate, Duree, genre, note, avis, directors, recette) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (title2, date2, certificate, time1, genre1, note2, votes, direc1, gross))
          conn.commit()


