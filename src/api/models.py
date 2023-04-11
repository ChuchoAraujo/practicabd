from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.is_active = True

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    # Define the relationship with the User and Character models
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    character = db.relationship('Character', backref=db.backref('favorited_by', lazy=True))

    def __init__(self, user, character):
        self.user = user
        self.character = character

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "character": self.character.serialize()
        }
    def serialize_with_user(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "character": self.character.serialize(),
        }