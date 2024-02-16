from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#-------------------------------------------------------------User--------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos = db.relationship('Favorito', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.email # si tocas funciones no hace falta hacer migrar y upgradear todo otra vez

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favoritos": [favorito.serialize() for favorito in self.favoritos]
            # do not serialize the password, its a security breach
        }
    
#------------------------------------------------------Character Model----------------------------------------------------
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False )
    genero = db.Column(db.Enum('masculino','femenino', name='Genero'), nullable=False)
    hair_color = db.Column(db.Enum('negro','rubio', name='HairColor'), nullable=False)
    eye_color = db.Column(db.Enum('verdes','azules', name='EyeColor'), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.nombre

    def serialize(self): #aca va todos lo que este en class libro
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
            # do not serialize the password, its a security breach
        }
    
#---------------------------------------------------------Planet Model---------------------------------------------------------
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True) # nombre agregar
    nombre = db.Column(db.String(50),)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<Planet %r>' % self.nombre

    def serialize(self): #aca va todos lo que este en class libro
        return {
            "id": self.id,
            "nombre": self.nombre,
            "population": self.population,
            "terrain": self.terrain
            
            # do not serialize the password, its a security breach
        }
    
#---------------------------------------------Favorito-------------------------------------------------------------
    
class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planetId = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    characterId = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self): #aca va todos lo que este en class libro
        return {
            "id": self.id,
            "planetId": self.planetId,
            "userId": self.user_id
            
            
            # do not serialize the password, its a security breach
        }