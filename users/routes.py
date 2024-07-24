from flask import Blueprint, request, jsonify
from .models import User
from app import db
from .services import create_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "mobile_no": user.mobile_no, "email": user.email} for user in users])



@users_bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()
    user = create_user(data)
    return jsonify(user), 201

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.name = data['name']
    user.mobile_no = data['mobile_no']
    user.email = data['email']
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    users = User.query.filter(User.name.ilike(f'%{name}%')).all()
    return jsonify([{"id": user.id, "name": user.name, "mobile_no": user.mobile_no, "email": user.email} for user in users])