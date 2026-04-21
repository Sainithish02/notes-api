from flask import Blueprint,jsonify,request
from models.user_model import get_users, get_user , create_user , update_user,delete_user
users_bp = Blueprint("users", __name__)
@users_bp.route("/users", methods=["GET"])
def get_users_route():
    users = get_users()
    return jsonify(users)

@users_bp.route("/users/<int:user_id>",methods=["GET"])
def get_user_route(user_id):
    user = get_user(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user),200

@users_bp.route("/users", methods = ["POST"])
def create_user_route():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Invalid input"}), 400

    create_user(username, email)
    return jsonify({"message":"user created"}), 201

@users_bp.route("/users/<int:user_id>",methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Invalid input"}), 400

    result = update_user(user_id, username, email)

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "user updated"}), 200

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    result = delete_user(user_id)

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"}), 200