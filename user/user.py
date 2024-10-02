from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
   return make_response(jsonify(users), 200)

@app.route("/users/<userid>", methods=['GET'])
def get_user_by_userid(userid):
   for user in users:
      if user["id"] == userid:
         return make_response(jsonify(user), 200)
   return make_response(jsonify({"error":"User not found"}), 404)

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

@app.route("/create_booking/<userid>", methods=['POST'])
def  create_booking_by_userid (userid):
   req = request.get_json()

   #Post request to booking service
   service = requests.post(f"http://127.0.0.1:3201//bookings/{userid}",json = req)
   if service.ok:
      return make_response(jsonify(service.json()), 200)
   else:
      return make_response(jsonify({"error":"Bad request"}), 400)

@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_by_userid (userid):
   service = requests.get(f"http://127.0.0.1:3201/bookings/{userid}")
   if service.ok:
      return make_response(jsonify(service.json()), 200)
   else:
      return make_response(jsonify({"error":"Bad request"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
