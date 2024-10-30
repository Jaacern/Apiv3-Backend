from flask import Blueprint, request, jsonify
from models import Cuota

cuota_bp = Blueprint('cuota_bp', __name__)

@cuota_bp.route('/', methods=['GET'])
def get_cuotas():
    try:
        cuotas = Cuota.get_all()
        return jsonify({'status': 'success', 'data': cuotas}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cuota_bp.route('/<cuota_id>/', methods=['GET'])
def get_cuota(cuota_id):
    try:
        cuota = Cuota.get_by_id(cuota_id)
        if cuota:
            return jsonify({'status': 'success', 'data': cuota}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Cuota no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cuota_bp.route('/', methods=['POST'])
def create_cuota():
    try:
        data = request.get_json()
        Cuota.create(data)
        return jsonify({'status': 'success', 'message': 'Cuota creada con éxito.'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cuota_bp.route('/<cuota_id>/', methods=['PUT'])
def update_cuota(cuota_id):
    try:
        data = request.get_json()
        Cuota.update(cuota_id, data)
        return jsonify({'status': 'success', 'message': 'Cuota actualizada con éxito.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cuota_bp.route('/<cuota_id>/', methods=['DELETE'])
def delete_cuota(cuota_id):
    try:
        Cuota.delete(cuota_id)
        return jsonify({'status': 'success', 'message': 'Cuota eliminada con éxito.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
