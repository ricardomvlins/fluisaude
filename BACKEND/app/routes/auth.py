from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "chave_super_secreta"


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login do usuário
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: 123456
    responses:
      200:
        description: Login realizado com sucesso
      401:
        description: Credenciais inválidas
    """

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "user": user.to_dict()
    })