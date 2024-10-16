import json
import os

dirname = os.path.dirname(__file__)

def get_movie(movies, movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return movie
    return None

def write_movies(movies):
    with open('{}/databases/movies.json'.format(dirname), 'w') as f:
        json.dump({"movies": movies}, f, indent=4)
