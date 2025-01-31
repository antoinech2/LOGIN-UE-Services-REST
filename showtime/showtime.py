from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
import os

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

dirname = os.path.dirname(__file__)

with open('{}/databases/times.json'.format(dirname), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

# Main endpoint
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def showtimes():
   return make_response(jsonify(schedule), 200)

# Show available bookings for a specific date
@app.route("/showtimes/<date>", methods=['GET'])
def get_movies_by_date(date):
    for day in schedule:
        if day["date"] == date:
            return make_response(jsonify(day), 200)
    return make_response(jsonify({"error": "no data found for given date"}), 404)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
