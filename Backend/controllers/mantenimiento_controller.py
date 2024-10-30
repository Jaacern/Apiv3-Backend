# backend/controllers/mantenimiento_controller.py

from flask import Blueprint, request, jsonify
from models import Mantenimiento, Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

mantenimiento_bp = Blueprint('mantenimiento_bp', __name__)

# Ruta: Obtener todos los mantenimientos
@mantenimiento_bp.route('/', methods=['GET'])
def get_mantenimientos():
    try:
        mantenimientos = Mantenimiento.collection.all()
        mantenimientos_list = [m.to_dict() for m in mantenimientos]
        return jsonify({'status': 'success', 'data': mantenimientos_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un mantenimiento por ID
@mantenimiento_bp.route('/<id_mantenimiento>/', methods=['GET'])
def get_mantenimiento(id_mantenimiento):
    try:
        mantenimiento = Mantenimiento.collection.get(id_mantenimiento)
        if mantenimiento:
            return jsonify({'status': 'success', 'data': mantenimiento.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo mantenimiento
@mantenimiento_bp.route('/', methods=['POST'])
def create_mantenimiento():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['tipo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'costo', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Si se proporciona 'personal', verificar que exista
        personal = None
        if 'personal' in data and data['personal']:
            try:
                personal = Personal.collection.get(data['personal'])
                if not personal:
                    return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
        
        # Crear una instancia de Mantenimiento
        mantenimiento = Mantenimiento(
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            costo=data['costo'],
            estado=data['estado'],
            personal=data.get('personal')  # Puede ser None
        )
        
        # Guardar en Firestore
        mantenimiento.save()
        
        return jsonify({'status': 'success', 'data': mantenimiento.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El mantenimiento ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un mantenimiento existente
@mantenimiento_bp.route('/<id_mantenimiento>/', methods=['PUT'])
def update_mantenimiento(id_mantenimiento):
    try:
        data = request.get_json()
        mantenimiento = Mantenimiento.collection.get(id_mantenimiento)
        if not mantenimiento:
            return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
        
        # Si se está actualizando 'personal', verificar que exista
        if 'personal' in data and data['personal']:
            try:
                personal = Personal.collection.get(data['personal'])
                if not personal:
                    return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(mantenimiento, key):
                setattr(mantenimiento, key, value)
        
        # Guardar cambios
        mantenimiento.save()
        
        return jsonify({'status': 'success', 'data': mantenimiento.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un mantenimiento
@mantenimiento_bp.route('/<id_mantenimiento>/', methods=['DELETE'])
def delete_mantenimiento(id_mantenimiento):
    try:
        mantenimiento = Mantenimiento.collection.get(id_mantenimiento)
        if not mantenimiento:
            return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
        
        # Eliminar el mantenimiento
        mantenimiento.delete()
        
        return jsonify({'status': 'success', 'message': 'Mantenimiento eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Mantenimiento no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
