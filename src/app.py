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
from models import db, User, Character, Planet # se importa toodo lo  que se cree en models
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

#--------------------------------------------------------character---------------------------------------------

@app.route('/character', methods=['GET'])
def get_character():
    all_character = Character.query.all()
    results = []
    for character in all_character:
        results.append(character.serialize())

   

    return jsonify(results), 200

@app.route('/character/<int:character_id>', methods=['GET']) # busca un solo autor
def get_characterId(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify(), 404
    
    return jsonify(character.serialize()), 200

#---------------------------------------------planet--------------------------------------------------

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()
    results = []
    for planet in all_planet:
        results.append(planet.serialize())

   

    return jsonify(results), 200

@app.route('/planet/<int:planet_id>', methods=['GET']) # busca un solo autor
def get_planetId(character_id):
    planet = Planet.query.get(character_id)
    if planet is None:
        return jsonify(), 404
    
    return jsonify(planet.serialize()), 200
  

"""@app.route('/autores/<int:autor_id>/libros', methods=['POST']) # crear un libro
def create_libro(autor_id):
    body = request.get_json()

    libro = Libro()
    libro.ISBN = body['ISBN'] # body.get('ISBN')
    #se agrega todo lo que este en models/libtos los atributos
    if body.get('titulo') is None:
        libro.titulo = "Sin titulo"
    else:
        libro.titulo = body.get = "Sin titulo" # poder dejar poner algo sin tener que ser obligatorio

    db.session.add(libro)
    db.session.commit()

    return jsonify("libro creado"), 200"""





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
