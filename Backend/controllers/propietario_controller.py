# backend/controllers/propietario_controller.py

from flask import Blueprint, request, jsonify
from models import Propietario
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

propietario_bp = Blueprint('propietario_bp', __name__)

# Ruta: Obtener todos los propietarios
@propietario_bp.route('/', methods=['GET'])
def get_propietarios():
    try:
        propietarios = Propietario.collection.all()
        propietarios_list = [prop.to_dict() for prop in propietarios]
        return jsonify({'status': 'success', 'data': propietarios_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un propietario por ID
@propietario_bp.route('/<id_propietario>/', methods=['GET'])
def get_propietario(id_propietario):
    try:
        propietario = Propietario.collection.get(id_propietario)
        if propietario:
            return jsonify({'status': 'success', 'data': propietario.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo propietario
@propietario_bp.route('/', methods=['POST'])
def create_propietario():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['nombre', 'apepat', 'apemat', 'rut', 'telefono', 'email', 'direccion']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Crear una instancia de Propietario
        propietario = Propietario(
            nombre=data['nombre'],
            apepat=data['apepat'],
            apemat=data['apemat'],
            rut=data['rut'],
            telefono=data['telefono'],
            email=data['email'],
            direccion=data['direccion']
        )
        
        # Guardar en Firestore
        propietario.save()
        
        return jsonify({'status': 'success', 'data': propietario.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El RUT del propietario ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un propietario existente
@propietario_bp.route('/<id_propietario>/', methods=['PUT'])
def update_propietario(id_propietario):
    try:
        data = request.get_json()
        propietario = Propietario.collection.get(id_propietario)
        if not propietario:
            return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(propietario, key):
                setattr(propietario, key, value)
        
        # Guardar cambios
        propietario.save()
        
        return jsonify({'status': 'success', 'data': propietario.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un propietario
@propietario_bp.route('/<id_propietario>/', methods=['DELETE'])
def delete_propietario(id_propietario):
    try:
        propietario = Propietario.collection.get(id_propietario)
        if not propietario:
            return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
        
        # Eliminar el propietario
        propietario.delete()
        
        return jsonify({'status': 'success', 'message': 'Propietario eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Propietario no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
