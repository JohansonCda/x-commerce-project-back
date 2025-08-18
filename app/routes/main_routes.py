from flask import Blueprint, jsonify
from ..orm.schemas import UserCreate
from ..orm.controllers.user_controller import UserController

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    user_controller = UserController()
    user1 = user_controller.get_by_email("johndoe@example.com")
    user2 = user_controller.get_by_register_date("2023-01-01", "2026-12-31")
    print(user2)
    return jsonify({"message": "API corriendo..."})


