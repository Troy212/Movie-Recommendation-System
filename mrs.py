# -*- coding: utf-8 -*-
"""MRS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1emalymbyn1NVeM9f9oM3y9DuLST-tAW_
"""

import numpy as np
import pandas as pd

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies.head()

credits.head()

movies.head(1)

credits.head(1)

credits.head(1)['cast'].values

credits.head(1)['crew'].values

movies = movies.merge(credits,on='title')

movies.head(1)

#genres
#id
#keywords
#titles
#overview
#caste
#crew

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies['original_language'].value_counts()

movies.info()

movies.head()

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

movies.iloc[0].genres

#[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
# ['Actions','Adventure','Fantasy','SciFi']

def convert(obj):
  L = []
  for i in ast.literal_eval(obj):
      L.append(i['name'])
  return L

movies['genres'] = movies['genres'].apply(convert)

movies.head()

movies['keywords'] = movies['keywords'].apply(convert)

movies.head()

movies['cast'][0]

def convert3(obj):
  L = []
  counter = 0
  for i in ast.literal_eval(obj):
    if counter != 3:
      L.append(i['name'])
      counter+=1
    else:
      break
  return L

movies['cast'] = movies['cast'].apply(convert3)

movies.head()

movies['crew'][0]

def fetch_director(obj):
  L = []
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      L.append(i['name'])
      break
  return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

new_df = movies[['movie_id','title','tags']]

new_df

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

movies.head()

new_df['tags'][0]

new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

new_df.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y = []

  for i in text.split():
      y.append(ps.stem(i))
  return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

new_df['tags'][0]

new_df['tags'][1]

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray().shape

vectors[0]

len(cv.get_feature_names_out())

cv.get_feature_names_out()

ps.stem('loving')

new_df['tags'][0]

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np # Import NumPy

vectors = np.asarray(vectors) # Convert vectors to NumPy array
vectors = vectors.reshape(1, -1)

simililarity = cosine_similarity(vectors)

cosine_similarity(vectors)

sorted(list(enumerate(simililarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = simililarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)
  return

recommend('Avatar')



vectors = cv.fit_transform(new_df['tags']).toarray()



simililarity = cosine_similarity(vectors)



from IPython import get_ipython
from IPython.display import display
import numpy as np
import pandas as pd
import ast

# ... (rest of your data loading and cleaning code)

# ... (functions like convert, convert3, fetch_director, stem)

# ... (creating new_df and preprocessing tags)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)
    return

recommend('Avatar')

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))

new_df.to_dict()

pickle.dump(new_df.to_dict(),open('movie_dict','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))
