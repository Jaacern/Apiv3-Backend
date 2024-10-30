# controllers/departamento_controller.py

from flask import Blueprint, request, jsonify
from models import Departamento
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

departamento_bp = Blueprint('departamento_bp', __name__)

# Ruta: Obtener todos los departamentos
@departamento_bp.route('/', methods=['GET'])
def get_departamentos():
    try:
        departamentos = Departamento.collection.all()
        departamentos_list = [dept.to_dict() for dept in departamentos]
        return jsonify({'status': 'success', 'data': departamentos_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un departamento por ID
@departamento_bp.route('/<id_departamento>/', methods=['GET'])
def get_departamento(id_departamento):
    try:
        departamento = Departamento.collection.get(id_departamento)
        if departamento:
            return jsonify({'status': 'success', 'data': departamento.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo departamento
@departamento_bp.route('/', methods=['POST'])
def create_departamento():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['numero', 'piso', 'tipo', 'superficie', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Crear una instancia de Departamento
        departamento = Departamento(
            numero=data['numero'],
            piso=data['piso'],
            tipo=data['tipo'],
            superficie=data['superficie'],
            estado=data['estado']
        )
        
        # Guardar en Firestore
        departamento.save()
        
        return jsonify({'status': 'success', 'data': departamento.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El número de departamento ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un departamento existente
@departamento_bp.route('/<id_departamento>/', methods=['PUT'])
def update_departamento(id_departamento):
    try:
        data = request.get_json()
        departamento = Departamento.collection.get(id_departamento)
        if not departamento:
            return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(departamento, key):
                setattr(departamento, key, value)
        
        # Guardar cambios
        departamento.save()
        
        return jsonify({'status': 'success', 'data': departamento.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un departamento
@departamento_bp.route('/<id_departamento>/', methods=['DELETE'])
def delete_departamento(id_departamento):
    try:
        departamento = Departamento.collection.get(id_departamento)
        if not departamento:
            return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Eliminar el departamento
        departamento.delete()
        
        return jsonify({'status': 'success', 'message': 'Departamento eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
