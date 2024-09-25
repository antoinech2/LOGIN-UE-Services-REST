from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

from helper import get_movie, write_movies

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

# JSON file containing database
with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# Root endpoint
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

# Template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

# Raw JSON database
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

# Get all movie information
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    movie = get_movie(movies, movieid)
    if movie:
        return make_response(jsonify(movie),200)
    else:
        return make_response(jsonify({"error":"Movie ID not found"}),404)

# Get movie rating
@app.route("/movies/<movieid>/rating", methods=['GET'])
def get_movie_rating(movieid):
    movie = get_movie(movies, movieid)
    if movie:
        return make_response(str(movie["rating"]),200)
    else:
        return make_response(jsonify({"error":"Movie ID not found"}),404)
    
# Get movie title
@app.route("/movies/<movieid>/title", methods=['GET'])
def get_movie_title(movieid):
    movie = get_movie(movies, movieid)
    if movie:
        return make_response(movie["title"],200)
    else:
        return make_response(jsonify({"error":"Movie ID not found"}),404)
    
# Get movie director
@app.route("/movies/<movieid>/director", methods=['GET'])
def get_movie_director(movieid):
    movie = get_movie(movies, movieid)
    if movie:
        return make_response(movie["director"],200)
    else:
        return make_response(jsonify({"error":"Movie ID not found"}),400)

# Get movie by title
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie
    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

# Add movie
@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write_movies(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

# Update movie rating
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            write_movies(movies)
            res = make_response(jsonify(movie),200)
            return res
    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

# Delete movie
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            write_movies(movies)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

# Help message
@app.route("/help", methods=['GET'])
def help():
    return make_response(render_template('help.html'),200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
