from model import *
import seaborn as sns
import matplotlib.pyplot as plt



conn, curs = connexion()

df_film = pd.read_sql_query('SELECT * FROM Film', conn)


def clear():

  df_film.set_index('id', inplace = True)
  median = df_film['recette'].median()
  df_film['recette'].fillna(median, inplace=True)
  df_film['recette'] = df_film.recette.astype(int)

  df_film['certificate'].fillna('Tous publics', inplace=True)


def recette_year():

  recette_by_years = sns.lineplot(x="year", y="recette", data=df_film)

  plt.title("Evolution des recettes du box-offices")




def top_recent():

  df_movies_by_y = df_film.groupby('year').count()

  df3 = df_movies_by_y.rename_axis('year').reset_index()

  nb_years = sns.lineplot(x="year", y="title", data=df3)

  plt.title("Nombre de film par an")


def top_directors_boxoffice():

  df_best_directors=df_film.groupby('directors').sum('recette').sort_values(by= 'recette', ascending=False)
  df_best_directors
  df3 = df_best_directors.rename_axis('Réalisateur').reset_index()
  df4 = df3.head(5)
  top_5_directors = sns.catplot(x="Réalisateur", y="recette", data=df4, saturation=.5, kind="bar", ci=None, aspect=3)
  top_5_directors.fig.suptitle("Top 5 des réalisateurs ayant fait le plus de recette au box-office")

def top_directors_movies():

  df4 = pd.read_sql_query('SELECT directors, COUNT(*) as Nb_films from Film GROUP BY directors ORDER BY Nb_films DESC LIMIT 10;', conn)
  df5 = df4.head(20)
  top_10_directors = sns.catplot(x="directors", y="Nb_films", data=df5, saturation=.5, kind="bar", ci=None, aspect=3)
  top_10_directors.fig.suptitle("Top 10 des réalisateurs ayant eu le plus de films dans le top 250 ")


def annee_genre(annee):
  x = []
  z = 0
  new_df = pd.DataFrame(columns = ['genre_final', 'recette_final', 'annee'])

  for i in df_film.index:
      genre = (df_film['genre'][i]).replace('\n', '').replace(' ', '').split(',')
      for y in genre:
          recette_genre = (df_film['recette'][i])
          date_genre = (df_film['annee'][i])
          x = (y, recette_genre, date_genre)
          new_df.loc[z] = x
          z = z + 1

  df_dyn = new_df[new_df['annee']== annee].groupby('genre_final').sum()
  df_dyn1 = df_dyn.drop(['annee'], axis=1)

  labels = df_dyn1['genre_final']
  sizes = df_dyn['recette_final']

  fig1, ax1 = plt.subplots(figsize=(12,7))
  ax1.pie(sizes,  labels=labels, explode = explode, autopct='%1.1f%%',
          shadow=True)
  plt.show()

def category_genre():
  x = []
  z = 0
  new_df = pd.DataFrame(columns = ['genre_final', 'recette_final'])
  for i in df_film.index:
      genre = (df_film['genre'][i]).replace('\n', '').replace(' ', '').split(',')
      for y in genre:
          recette_genre = (df_film['recette'][i])

          x = (y, recette_genre)
          new_df.loc[z] = x
          z = z + 1
  df_genre = new_df.groupby('genre_final').sum('recette_final').sort_values(by= 'recette_final', ascending=False)
  return df_genre

create_table()

scrapping(['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt', 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt', 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=151&ref_=adv_nxt', 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=201&ref_=adv_nxt'])

clear()

