from flask import *
import json
from data.constantes import *
from algorithm.journey import *

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Its working</p>"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


@app.route("/cities")
def getCities():
    with open(CITIES_JSON_FILE, 'r') as file:
        cities = json.load(file)
        return jsonify(cities)


@app.route("/cities/filter")
def filterCities():
    filters = request.args.get('country').split(',')
    lower_filters = {f.lower() for f in filters}

    with open(CITIES_JSON_FILE, 'r') as file:
        cities = json.load(file)

    filtered_cities = [city for city in cities if city['country'].lower() in lower_filters]
    set_cityids = {f"{city['city']},{city['country']}".lower() for city in filtered_cities}

    with open(ROUTES_JSON_FILE, 'r') as file:
        routes = json.load(file)

    filtered_routes = [route for route in routes if route['from'].lower() in set_cityids or route['to'].lower() in set_cityids]

    return jsonify({
        "cities": filtered_cities,
        "routes": filtered_routes
    })


@app.route("/routes")
def getRoutes():
    with open(ROUTES_JSON_FILE, 'r') as file:
        routes = json.load(file)
        return jsonify(routes)
    

@app.route("/journey", methods=['POST'])
def getJourney():
    data = request.json
    journey = createJourney(data)    
    return  jsonify(journey)
