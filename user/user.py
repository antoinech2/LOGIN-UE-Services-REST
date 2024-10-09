from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

def getUser(userid):
   for user in users:
      if user["id"] == userid:
         return user
   return None

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
   return make_response(jsonify(users), 200)

@app.route("/users/<userid>", methods=['GET'])
def get_user_by_userid(userid):
   user = getUser(userid)
   if user:
      return make_response(jsonify(user), 200)
   return make_response(jsonify({"error":"User not found"}), 404)


# Display movies that are available for booking on a specific date
@app.route("/available_bookings", methods=['GET'])
def get_available_bookings():
   # check if there is a date in the request
   if not "date" in request.args or not request.args["date"]:
      return make_response(jsonify({"error":"No date provided"}), 400)

   date = request.args["date"]

   # ask showtimes service a list of movies for the date
   slots = requests.get(f"http://127.0.0.1:3202/showtimes/{date}")

   # check if there is an error using the response code
   if not slots.ok:
      if slots.status_code == 404:
         return make_response(jsonify({"error":"No showtimes available for this date"}), 404)
      return make_response(jsonify({"error":"Error in showtimes service"}), 500)
   
   service_request = slots.json()
   movies_id = service_request["movies"]

   # get the name of the movies
   movies_name = []
   for movie in movies_id:
      movie_name = requests.get(f"http://127.0.0.1:3200/movies/{movie}/title")
      if not movie_name.ok:
         return make_response(jsonify({"error":"Error in movies service or unknown movie"}), 500)
      movies_name.append(movie_name.text)

   return make_response(jsonify(movies_name), 200)

@app.route("/movie_info", methods=['GET'])
def get_movie_info():
   if not "title" in request.args or not request.args["title"]:
      return make_response(jsonify({"error":"No title provided"}), 400)

   title = request.args["title"]

   # ask movie service for the movie info
   movie_request = requests.get(f"http://127.0.0.1:3200/moviesbytitle?title={title}")

   # check if there is an error using the response code
   if not movie_request.ok:
      if movie_request.status_code == 404:
         return make_response(jsonify({"error":"No movie found"}), 404)
      return make_response(jsonify({"error":"Error in movie service"}), 500)
   
   # We provide info to end-users (not the interal movie id)
   movie = movie_request.json()
   result = {
      "title": movie["title"],
      "director": movie["director"],
      "rating": movie["rating"]
   }

   return make_response(jsonify(result), 200)

# Add a booking for a movie
@app.route("/bookings/<userid>", methods=['POST'])
def create_booking_by_userid(userid):
   req = request.get_json()
   
   if not getUser(userid):
      return make_response(jsonify({"error":"User not found"}), 404)

   #Post request to booking service
   service = requests.post(f"http://127.0.0.1:3201/bookings/{userid}",json = req)
   if service.ok:
      return make_response(jsonify(service.json()), 200)
   else:
      if service.status_code < 500: #return error message from booking service
         return make_response(jsonify(service.json()), service.status_code)
      return make_response(jsonify({"error":"Error in booking service"}), 500)

# Get bookings of a user
@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_by_userid(userid):
   service = requests.get(f"http://127.0.0.1:3201/bookings/{userid}")
   if service.ok:
      return make_response(jsonify(service.json()), 200)
   else:
      if service.status_code == 404:
         return make_response(jsonify(service.json()), 404)
      return make_response(jsonify({"error":"Error in booking service"}), 500)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
