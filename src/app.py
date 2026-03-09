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
from models import db, User, Planet, Character, Film, Favorite
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

@app.route('/users', methods=['GET'])
def handle_user():

   all_users = User.query.all()
   results = [us.serialize() for us in all_users]

   return jsonify(results), 200

@app.route('/user/favorites', methods = ['GET'])
def handle_user_favorites():

    user_id = 1
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in user_favorites]), 200

@app.route('/character', methods = ['GET'])
def handle_character():
    
    all_character = Character.query.all()
    results = [char.serialize() for char in all_character]

    return jsonify(results), 200

@app.route ('/character/<int:character_id>', methods = ['GET'])
def handle_character_id(character_id):
    
    character = Character.query.get(character_id)

    return jsonify(character.serialize()), 200

@app.route('/planets', methods = ['GET'])
def handle_planets():
    all_planets = Planet.query.all()
    results = [char.serialize() for char in all_planets]

    return jsonify(results), 200

@app.route ('/planets/<int:planet_id>', methods = ['GET'])
def handle_planets_id(planets_id):

    planets = Planet.query.get(planets_id)

    return jsonify(planets.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def handle_favorite_planet(planet_id):
    user_id = 1

    new_favorite = Favorite (user_id = user_id, planet_id = planet_id)

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "planets added to favorites"}), 200
    
@app.route('/favorite/character/<int:character_id>', methods = ['POST'])
def handle_favorite_character(character_id):
    user_id = 1

    new_favorite = Favorite (user_id = user_id, character_id = character_id)

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "planets added to favorites"}), 200

@app.route('/favorite/character/<int:character_id>', methods = ['DELETE'])
def handle_favorite_character_DELETE(character_id):
    user_id = 1

    favorite = Favorite.query.filter_by(user_id = user_id, character_id = character_id).first()

    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg' : 'favorite delete'}), 200

@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def handle_favorite_planet_DELETE(planet_id):
    user_id = 1

    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()

    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg' : 'favorite delete'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
