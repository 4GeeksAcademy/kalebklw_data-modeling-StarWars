"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Characters, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#   Code For GET Methods
@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users_list = [item.serialize() for item in users]
    response_body = {
        "msg": "Hello, this is your GET /users response ",
        "users": users_list
    }
    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def added_characters():
    characters = Characters.query.all()
    characters_list = [item.serialize() for item in characters]
    response_body = {
        "msg": "Hello, this is your GET /characters response ",
        "characters": characters_list
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def characters_info(character_id):
    # data = request.get_json()
    # characters = Characters.query.all()
    # character_list = [item.serialize() for item in characters]
    # character_id = data['character']
    character = db.session.get(Characters, character_id)
    response_body = {
        "msg": "This characters information",
        "character": character.serialize()
    }
    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def added_vehicles():
    vehicles = Vehicles.query.all()
    vehicles_list = [item.serialize() for item in vehicles]
    response_body = {
        "msg": "Here is a list of the vehicles!",
        "vehicles": vehicles_list
    }
    return jsonify(response_body), 200


#   Code For POST Methods
@app.route('/users/favorites/planet', methods=['POST'])
def fav_planets():
    data = request.get_json()
    user_id = data['user']
    planet_id = data['planet']
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    user.favorite_planet.append(planet)
    db.session.commit()

    return jsonify(user.serialize()), 200 


@app.route('/users/favorites/characters', methods=['POST'])
def fav_characters():
    data = request.get_json()
    user_id = data['user']
    character_id = data['characters']
    user = db.session.get(User, user_id)
    characters = db.session.get(Characters, character_id)

    user.favorite_characters.append(characters)
    db.session.commit()

    return jsonify(user.serialize()), 200


@app.route('/users/favorites/vehicles', methods=['POST'])
def fav_vehicles():
    data = request.get_json()
    user_id = data['user']
    vehicles_id = data['vehicles']
    user = db.session.get(User, user_id)
    vehicles = db.session.get(Vehicles, vehicles_id)

    user.favorite_vehicles.append(vehicles)
    db.session.commit()

    return jsonify(user.serialize()), 200


#  Code For DELETE Methods
@app.route('/users/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_fav_char():
    data = request.get_json()
    character_id = data['character_id']
    rec = User.query.filter_by(character_id)
    db.session.commit()

    return jsonify(rec), 200

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
