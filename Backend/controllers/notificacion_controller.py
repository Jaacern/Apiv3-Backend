# backend/controllers/notificacion_controller.py

from flask import Blueprint, request, jsonify
from models import Notificacion, Residente, Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

notificacion_bp = Blueprint('notificacion_bp', __name__)

# Ruta: Obtener todas las notificaciones
@notificacion_bp.route('/', methods=['GET'])
def get_notificaciones():
    try:
        notificaciones = Notificacion.collection.all()
        notificaciones_list = [notif.to_dict() for notif in notificaciones]
        return jsonify({'status': 'success', 'data': notificaciones_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una notificación por ID
@notificacion_bp.route('/<id_notificacion>/', methods=['GET'])
def get_notificacion(id_notificacion):
    try:
        notificacion = Notificacion.collection.get(id_notificacion)
        if notificacion:
            return jsonify({'status': 'success', 'data': notificacion.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva notificación
@notificacion_bp.route('/', methods=['POST'])
def create_notificacion():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['tipo', 'mensaje', 'fecha', 'destinatario']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el destinatario existe (puede ser Residente o Personal)
        destinatario = None
        if 'destinatario_residente' in data and data['destinatario_residente']:
            try:
                destinatario = Residente.collection.get(data['destinatario_residente'])
                if not destinatario:
                    return jsonify({'status': 'error', 'message': 'Residente destinatario no encontrado.'}), 404
                destinatario_tipo = 'Residente'
                destinatario_id = data['destinatario_residente']
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Residente destinatario no encontrado.'}), 404
        elif 'destinatario_personal' in data and data['destinatario_personal']:
            try:
                destinatario = Personal.collection.get(data['destinatario_personal'])
                if not destinatario:
                    return jsonify({'status': 'error', 'message': 'Personal destinatario no encontrado.'}), 404
                destinatario_tipo = 'Personal'
                destinatario_id = data['destinatario_personal']
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal destinatario no encontrado.'}), 404
        else:
            return jsonify({'status': 'error', 'message': 'Debe proporcionar un destinatario válido (residente o personal).'}), 400
        
        # Crear una instancia de Notificacion
        notificacion = Notificacion(
            tipo=data['tipo'],
            mensaje=data['mensaje'],
            fecha=data['fecha'],
            destinatario_tipo=destinatario_tipo,
            destinatario_id=destinatario_id
        )
        
        # Guardar en Firestore
        notificacion.save()
        
        return jsonify({'status': 'success', 'data': notificacion.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La notificación ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una notificación existente
@notificacion_bp.route('/<id_notificacion>/', methods=['PUT'])
def update_notificacion(id_notificacion):
    try:
        data = request.get_json()
        notificacion = Notificacion.collection.get(id_notificacion)
        if not notificacion:
            return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
        
        # Si se está actualizando el destinatario, verificar que exista
        if 'destinatario_residente' in data and data['destinatario_residente']:
            try:
                destinatario = Residente.collection.get(data['destinatario_residente'])
                if not destinatario:
                    return jsonify({'status': 'error', 'message': 'Residente destinatario no encontrado.'}), 404
                notificacion.destinatario_tipo = 'Residente'
                notificacion.destinatario_id = data['destinatario_residente']
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Residente destinatario no encontrado.'}), 404
        elif 'destinatario_personal' in data and data['destinatario_personal']:
            try:
                destinatario = Personal.collection.get(data['destinatario_personal'])
                if not destinatario:
                    return jsonify({'status': 'error', 'message': 'Personal destinatario no encontrado.'}), 404
                notificacion.destinatario_tipo = 'Personal'
                notificacion.destinatario_id = data['destinatario_personal']
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Personal destinatario no encontrado.'}), 404
        
        # Actualizar los campos proporcionados, excepto destinatario
        updatable_fields = ['tipo', 'mensaje', 'fecha']
        for key, value in data.items():
            if key in updatable_fields and hasattr(notificacion, key):
                setattr(notificacion, key, value)
        
        # Guardar cambios
        notificacion.save()
        
        return jsonify({'status': 'success', 'data': notificacion.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una notificación
@notificacion_bp.route('/<id_notificacion>/', methods=['DELETE'])
def delete_notificacion(id_notificacion):
    try:
        notificacion = Notificacion.collection.get(id_notificacion)
        if not notificacion:
            return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
        
        # Eliminar la notificación
        notificacion.delete()
        
        return jsonify({'status': 'success', 'message': 'Notificación eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Notificación no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
