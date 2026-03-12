from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "chave_super_secreta"


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = auth_header.split(" ")[1]

        if not auth_header:
            return jsonify({"error": "Token não enviado"}), 401

        try:
            token = auth_header.replace("Bearer ", "")
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if data["role"] != "admin":
                return jsonify({"error": "Acesso negado"}), 403

        except:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated