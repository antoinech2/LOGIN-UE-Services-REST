from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

dirname = os.path.dirname(__file__)

with open('{}/databases/bookings.json'.format(dirname), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

# Get all bookings
@app.route("/bookings", methods=['GET'])
def get_bookings():
   res = make_response(jsonify(bookings), 200)
   return res

# Get bookings for one user by user id
@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_byid(userid):
   user_bookings = None
   for booking in bookings:
      if booking["userid"] == userid:
         return make_response(jsonify(booking["dates"]), 200)
   return make_response(jsonify({"error":"No bookings for this user"}), 404)

# Add a booking for a user by user id, using the service showtimes to check the validity of the booking   
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
   req = request.get_json()
   req_date = req["date"]
   movieid = req["movieid"]

   if not req_date or not movieid:
      return make_response(jsonify({"error":"Missing date or movieid"}), 400)

   req_new_date = {"date": req_date, "movies": [movieid]}

   # check if user already has this booking
   for booking in bookings:
      if booking["userid"] == userid:
         for shedule in booking["dates"]:
            if shedule["date"] == req_date and shedule["movies"] == movieid:
               return make_response(jsonify({"error":"Booking already exists for this user"}), 409)

   # ask showtimes service a list of movies for the date
   service_request = requests.get(f"http://127.0.0.1:3202/showtimes/{req_date}")

   # check if there is an error using the response code
   if not service_request.ok:
      if service_request.status_code == 404:
         return make_response(jsonify({"error":"No showtimes available for this date"}), 404)
      return make_response(jsonify({"error":"Error in showtimes service"}), 500)
   
   service_request = service_request.json()
   movies = service_request["movies"]

   # check if the movie is in the list
   if movieid not in movies:
      res = make_response(jsonify({"error":"Movie not available for the selected date"}), 404)
   else :
      # add the booking for the specific user
      for booking in bookings:
         if booking["userid"] == userid:
            #check if the date already exists
            find = False
            for date in booking["dates"]:
               if date["date"] == req_date:
                  #check if the movie already exists
                  for movie in date["movies"]:
                     if movie == movieid:
                        return make_response(jsonify({"error":"Booking already exists for this user"}), 409)
                  date["movies"].append(movieid) #the movie is not used we append the movie
                  find = True #the date is already used we append the movie
                  print("date found in booking for user")
                  break
            if not find:
               booking["dates"].append(req_new_date) #the date is not used we add the date and the movie
               print("date not found in booking for user") 
      write(bookings)
      res = make_response(jsonify({"message":"Booking added"}), 200)
   return res

def write(bookings):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        json.dump({"bookings": bookings}, f, indent=4)



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
