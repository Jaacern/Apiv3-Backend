# backend/controllers/queja_controller.py

from flask import Blueprint, request, jsonify
from models import Queja, Residente, Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

queja_bp = Blueprint('queja_bp', __name__)

# Ruta: Obtener todas las quejas
@queja_bp.route('/', methods=['GET'])
def get_quejas():
    try:
        quejas = Queja.collection.all()
        quejas_list = [queja.to_dict() for queja in quejas]
        return jsonify({'status': 'success', 'data': quejas_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una queja por ID
@queja_bp.route('/<id_queja>/', methods=['GET'])
def get_queja(id_queja):
    try:
        queja = Queja.collection.get(id_queja)
        if queja:
            return jsonify({'status': 'success', 'data': queja.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva queja
@queja_bp.route('/', methods=['POST'])
def create_queja():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['residente', 'descripcion', 'fecha', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el residente existe
        residente = Queja.collection.get(data['residente'])
        if not residente:
            return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Opcional: Verificar que el personal existe si se asigna uno
        personal = None
        if 'personal_asignado' in data and data['personal_asignado']:
            try:
                personal = Personal.collection.get(data['personal_asignado'])
                if not personal:
                    return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
        
        # Crear una instancia de Queja
        queja = Queja(
            residente=data['residente'],
            descripcion=data['descripcion'],
            fecha=data['fecha'],
            estado=data['estado'],
            personal_asignado=data.get('personal_asignado')  # Puede ser None
        )
        
        # Guardar en Firestore
        queja.save()
        
        return jsonify({'status': 'success', 'data': queja.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La queja ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una queja existente
@queja_bp.route('/<id_queja>/', methods=['PUT'])
def update_queja(id_queja):
    try:
        data = request.get_json()
        queja = Queja.collection.get(id_queja)
        if not queja:
            return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
        
        # Si se está actualizando el residente, verificar que exista
        if 'residente' in data:
            residente = Residente.collection.get(data['residente'])
            if not residente:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Si se está actualizando el personal asignado, verificar que exista
        if 'personal_asignado' in data and data['personal_asignado']:
            personal = Personal.collection.get(data['personal_asignado'])
            if not personal:
                return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        updatable_fields = ['residente', 'descripcion', 'fecha', 'estado', 'personal_asignado']
        for key, value in data.items():
            if key in updatable_fields and hasattr(queja, key):
                setattr(queja, key, value)
        
        # Guardar cambios
        queja.save()
        
        return jsonify({'status': 'success', 'data': queja.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una queja
@queja_bp.route('/<id_queja>/', methods=['DELETE'])
def delete_queja(id_queja):
    try:
        queja = Queja.collection.get(id_queja)
        if not queja:
            return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
        
        # Eliminar la queja
        queja.delete()
        
        return jsonify({'status': 'success', 'message': 'Queja eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Queja no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
