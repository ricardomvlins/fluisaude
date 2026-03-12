from flask import Blueprint, request, jsonify
from ..controllers.consulta_controller import ConsultaController

consulta_bp = Blueprint("consultas", __name__)

@consulta_bp.route("/", methods=["GET"])
def listar_consultas():
    return jsonify(ConsultaController.listar())

@consulta_bp.route("/", methods=["POST"])
def criar_consulta():
    """
    Criar consulta
    ---
    tags:
      - Consultas
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            paciente_id:
              type: integer
              example: 1
            medico_id:
              type: integer
              example: 2
            data:
              type: string
              example: 2026-03-15
    responses:
      201:
        description: Consulta criada
    """
    data = request.get_json()
    consulta = ConsultaController.criar(data)
    return jsonify(consulta), 201

@consulta_bp.route("/<int:id>", methods=["PUT"])
def atualizar_consulta(id):
    data = request.get_json()
    consulta = ConsultaController.atualizar(id, data)
    if not consulta:
        return jsonify({"error": "Consulta não encontrada"}), 404
    return jsonify(consulta)

@consulta_bp.route("/<int:id>", methods=["DELETE"])
def deletar_consulta(id):
    sucesso = ConsultaController.deletar(id)
    if not sucesso:
        return jsonify({"error": "Consulta não encontrada"}), 404
    return jsonify({"message": "Consulta excluída com sucesso"})
