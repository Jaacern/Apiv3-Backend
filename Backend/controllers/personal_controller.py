# backend/controllers/personal_controller.py

from flask import Blueprint, request, jsonify
from models import Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

personal_bp = Blueprint('personal_bp', __name__)

# Ruta: Obtener todos los personal
@personal_bp.route('/', methods=['GET'])
def get_personal():
    try:
        personal = Personal.collection.all()
        personal_list = [persona.to_dict() for persona in personal]
        return jsonify({'status': 'success', 'data': personal_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un personal por ID
@personal_bp.route('/<id_personal>/', methods=['GET'])
def get_personal_by_id(id_personal):
    try:
        persona = Personal.collection.get(id_personal)
        if persona:
            return jsonify({'status': 'success', 'data': persona.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo personal
@personal_bp.route('/', methods=['POST'])
def create_personal():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['nombre', 'apepat', 'apemat', 'cargo', 'telefono', 'email', 'fecha_contratacion']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Crear una instancia de Personal
        persona = Personal(
            nombre=data['nombre'],
            apepat=data['apepat'],
            apemat=data['apemat'],
            cargo=data['cargo'],
            telefono=data['telefono'],
            email=data['email'],
            fecha_contratacion=data['fecha_contratacion']
        )
        
        # Guardar en Firestore
        persona.save()
        
        return jsonify({'status': 'success', 'data': persona.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El correo electrónico del personal ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un personal existente
@personal_bp.route('/<id_personal>/', methods=['PUT'])
def update_personal(id_personal):
    try:
        data = request.get_json()
        persona = Personal.collection.get(id_personal)
        if not persona:
            return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(persona, key):
                setattr(persona, key, value)
        
        # Guardar cambios
        persona.save()
        
        return jsonify({'status': 'success', 'data': persona.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un personal
@personal_bp.route('/<id_personal>/', methods=['DELETE'])
def delete_personal(id_personal):
    try:
        persona = Personal.collection.get(id_personal)
        if not persona:
            return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
        
        # Eliminar el personal
        persona.delete()
        
        return jsonify({'status': 'success', 'message': 'Personal eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Personal no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
