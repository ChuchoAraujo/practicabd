"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Favorite
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)
####################### GET ###############################

# Get all users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Get a user by ID
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.serialize()), 200

# Get all favorites for all users
@api.route('/favorites', methods=['GET'])
def get_all_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


# Get a user's favorite characters
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    favorites = user.favorites
    return jsonify([favorite.character.serialize() for favorite in favorites]), 200

# Get all characters
@api.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

# Get a character by ID
@api.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    return jsonify(character.serialize()), 200

@api.route('/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    favorites = user.favorites
    serialized_favorites = [f.serialize_with_user() for f in favorites]

    return jsonify(serialized_favorites), 200

# Add a favorite character for a user
@api.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite_character(user_id):
    data = request.get_json()
    character_id = data.get('character_id')
    
    # Ensure character exists
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    
    # Ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new favorite record
    favorite = Favorite(user=user, character=character)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'success': 'Character added to favorites'}), 200

