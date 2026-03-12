from flask import Blueprint, jsonify, request

from app.utils.auth import admin_required
from app.controllers import medico_controller

medico_bp = Blueprint("medico", __name__)


@medico_bp.route("/", methods=["post"])
@admin_required
def create_medico():
    """
    Criar médico
    ---
    tags:
      - Médicos
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Dr João
            especialidade_id:
              type: integer
              example: 1
    responses:
      201:
        description: Médico criado
    """
    try:
        medico = medico_controller.create_medico(request.get_json() or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(medico.to_dict()), 201


@medico_bp.route("/", methods=["get"])
def list_medicos():
    medicos = medico_controller.list_medicos()
    return jsonify([medico.to_dict() for medico in medicos])


@medico_bp.route("/<int:medico_id>", methods=["get"])
def get_medico(medico_id: int):
    medico = medico_controller.get_medico_by_id(medico_id)
    return jsonify(medico.to_dict()), 200

@medico_bp.route("/<int:medico_id>", methods=["put"])
@admin_required
def update_medico(medico_id: int):
    try:
        medico = medico_controller.update_medico(medico_id, request.get_json() or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(medico.to_dict()) 

@medico_bp.route("/<int:medico_id>", methods=["delete"])
@admin_required
def delete_medico(medico_id: int):
    medico_controller.delete_medico(medico_id)
    return jsonify({"message": "Medico deletado com sucesso"})