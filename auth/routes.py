from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    from auth.models import User
    from auth.services import create_user
    data = request.get_json()
    user = create_user(data)
    return jsonify(user), 201