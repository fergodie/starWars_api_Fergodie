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
from models import db, User, Character, Planet, Favorito # se importa toodo lo  que se cree en models
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

@app.route('/planet/<int:planet_id>', methods=['GET']) # busca uno solo 
def get_planetId(character_id):
    planet = Planet.query.get(character_id)
    if planet is None:
        return jsonify(), 404
    
    return jsonify(planet.serialize()), 200

#---------------------------------------------------------Users---------------------------------------------------------------

@app.route('/user', methods=['GET'])
def get_user():
    all_user = User.query.all()
    results = []
    for user in all_user:
        results.append(user.serialize())

   

    return jsonify(results), 200

#-------------------------------------------------------favoritos User------------------------------------------------------

@app.route('/user/<int:user_id>/favoritos', methods=['GET'])
def get_user_favoritos(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    favoritos = Favorito.query.filter_by(user_id=user.id).all()

    return jsonify({'favoritos': [favorito.serialize() for favorito in favoritos]})


#-------------------------------------------------Add favoritos Planet----------------------------------------------------

@app.route('/user/<int:user_id>/favorito', methods=['POST'])
def add_user_favorito(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()

    if 'planetId' not in data:
        return jsonify({'message': 'El campo planetId es obligatorio'}), 200

    planet_id = data['planetId']
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'message': 'Planeta no encontrado'}), 404

#                        Verificar si el planeta ya es un favorito del usuario
    
    existing_favorito = Favorito.query.filter_by(user_id=user.id, planetId=planet.id).first()
    if existing_favorito:
        return jsonify({'message': 'Este planeta ya es un favorito del usuario'}), 200

#                        Crear un nuevo favorito y asociarlo al usuario actual
    
    new_favorito = Favorito(planetId=planet.id, user_id=user.id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify({'message': 'Planeta añadido a favoritos correctamente'})

#-------------------------------------------------Add favoritos Character----------------------------------------------------


@app.route('/user/<int:user_id>/favorito', methods=['POST'])
def add_user_favorito2(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()

    if 'characterId' not in data:
        return jsonify({'message': 'El campo characterId es obligatorio'}), 200

    character_id = data['characterId']
    character = Character.query.get(character_id)

    if not character:
        return jsonify({'message': 'Personaje no encontrado'}), 404

    #                             Verificar si el personaje ya es un favorito del usuario

    existing_favorito = Favorito.query.filter_by(user_id=user.id, characterId=character.id).first()
    if existing_favorito:
        return jsonify({'message': 'Este personaje ya es un favorito del usuario'}), 200

    #                             Crear un nuevo favorito y asociarlo al usuario actual
    
    new_favorito = Favorito(characterId=character.id, user_id=user.id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify({'message': 'Personaje añadido a favoritos correctamente'})

#-------------------------------------------------Delete Planet-------------------------------------------------------------

@app.route('/favorite/planet/<int:planetId>', methods=['DELETE'])
def delete_favorite_planet(planetId):
    # Obtener el favorito del planeta por su id
    favorito = Favorito.query.filter_by(planetId=planetId).first()

    if not favorito:
        return jsonify({'message': 'Planeta favorito no encontrado'}), 200

    # Eliminar el favorito del planeta
    db.session.delete(favorito)
    db.session.commit()

    return jsonify({'message': 'Planeta favorito eliminado correctamente'})

"""@app.route('/favorito/planet/<int:planetId>', methods=['POST']) # crear un libro
def create_planet(planetId):
    body = request.get_json()

    libro = Libro()
    libro.ISBN = body['ISBN'] # body.get('ISBN')
    #se agrega todo lo que este en models/libros los atributos
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
