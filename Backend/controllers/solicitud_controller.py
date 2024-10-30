# backend/controllers/solicitud_controller.py

from flask import Blueprint, request, jsonify
from models import Solicitud, Residente, Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

solicitud_bp = Blueprint('solicitud_bp', __name__)

# Ruta: Obtener todas las solicitudes
@solicitud_bp.route('/', methods=['GET'])
def get_solicitudes():
    try:
        solicitudes = Solicitud.collection.all()
        solicitudes_list = [sol.to_dict() for sol in solicitudes]
        return jsonify({'status': 'success', 'data': solicitudes_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una solicitud por ID
@solicitud_bp.route('/<id_solicitud>/', methods=['GET'])
def get_solicitud(id_solicitud):
    try:
        solicitud = Solicitud.collection.get(id_solicitud)
        if solicitud:
            return jsonify({'status': 'success', 'data': solicitud.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva solicitud
@solicitud_bp.route('/', methods=['POST'])
def create_solicitud():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['residente', 'tipo', 'descripcion', 'fecha', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el residente existe
        try:
            residente = Residente.collection.get(data['residente'])
            if not residente:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        except DoesNotExist:
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
        
        # Crear una instancia de Solicitud
        solicitud = Solicitud(
            residente=data['residente'],
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            fecha=data['fecha'],
            estado=data['estado'],
            personal_asignado=data.get('personal_asignado')  # Puede ser None
        )
        
        # Guardar en Firestore
        solicitud.save()
        
        return jsonify({'status': 'success', 'data': solicitud.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La solicitud ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una solicitud existente
@solicitud_bp.route('/<id_solicitud>/', methods=['PUT'])
def update_solicitud(id_solicitud):
    try:
        data = request.get_json()
        solicitud = Solicitud.collection.get(id_solicitud)
        if not solicitud:
            return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
        
        # Si se está actualizando el residente, verificar que exista
        if 'residente' in data:
            try:
                residente = Residente.collection.get(data['residente'])
                if not residente:
                    return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Si se está actualizando el personal asignado, verificar que exista
        if 'personal_asignado' in data and data['personal_asignado']:
            try:
                personal = Personal.collection.get(data['personal_asignado'])
                if not personal:
                    return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal asignado no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        updatable_fields = ['residente', 'tipo', 'descripcion', 'fecha', 'estado', 'personal_asignado']
        for key, value in data.items():
            if key in updatable_fields and hasattr(solicitud, key):
                setattr(solicitud, key, value)
        
        # Guardar cambios
        solicitud.save()
        
        return jsonify({'status': 'success', 'data': solicitud.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una solicitud
@solicitud_bp.route('/<id_solicitud>/', methods=['DELETE'])
def delete_solicitud(id_solicitud):
    try:
        solicitud = Solicitud.collection.get(id_solicitud)
        if not solicitud:
            return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
        
        # Eliminar la solicitud
        solicitud.delete()
        
        return jsonify({'status': 'success', 'message': 'Solicitud eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Solicitud no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
