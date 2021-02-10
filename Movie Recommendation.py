import requests
import json


def get_movies_from_tastedive(name):
    d = {}
    d['q'] = name
    d['type'] = 'movies'
    d['limit'] = 5
    page = requests.get("https://tastedive.com/api/similar", params=d)
    return page.json()


def extract_movie_titles(x):
    z = []
    for dt in x['Similar']['Results']:
        z.append(dt['Name'])
    #print(z)
    return z


def get_related_titles(y):
    m = []
    n = []
    for movie in y:
        if movie not in m:
            m.append(extract_movie_titles(get_movies_from_tastedive(movie)))
    for lst in m:
        for mov in lst:
            if mov not in n:
                n.append(mov)
    #print(n)
    return n


def get_movie_data(title):
    info = {}
    d = {}
    d['t'] = title
    d['r'] = 'json'
    p = requests.get("http://www.omdbapi.com/?&apikey=3a15ea1a", params=d)
    info = p.json()
    return info


def get_movie_rating(x):
    for dt in x['Ratings']:
        if dt['Source'] == 'Rotten Tomatoes':
            return int((dt['Value'][0:2]))
        else:
            continue
    return 0


def get_sorted_recommendations(lst):
    z = (get_related_titles(lst))
    x = {}
    for movie in z:
        x[movie] = str(get_movie_rating(get_movie_data(movie)))
    s = sorted(x, reverse=True, key=lambda key:(x[key], key))
    #print(x)
    return x

l = []
n = input('Enter Movie Name : ')
l.append(n)
r = (get_sorted_recommendations(l))

for movie in r:
    print('Movie - ', movie, end = '.')
    print(' Ratings = ', r[movie], '%')