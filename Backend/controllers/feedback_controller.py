# backend/controllers/feedback_controller.py

from flask import Blueprint, request, jsonify
from models import Feedback, Residente, Personal
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

feedback_bp = Blueprint('feedback_bp', __name__)

# Ruta: Obtener todos los feedbacks
@feedback_bp.route('/', methods=['GET'])
def get_feedbacks():
    try:
        feedbacks = Feedback.collection.all()
        feedbacks_list = [fb.to_dict() for fb in feedbacks]
        return jsonify({'status': 'success', 'data': feedbacks_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un feedback por ID
@feedback_bp.route('/<id_feedback>/', methods=['GET'])
def get_feedback(id_feedback):
    try:
        feedback = Feedback.collection.get(id_feedback)
        if feedback:
            return jsonify({'status': 'success', 'data': feedback.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo feedback
@feedback_bp.route('/', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['residente', 'tipo', 'comentario', 'fecha']
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
        
        # Crear una instancia de Feedback
        feedback = Feedback(
            residente=data['residente'],
            tipo=data['tipo'],
            comentario=data['comentario'],
            fecha=data['fecha'],
            personal_asignado=data.get('personal_asignado')  # Puede ser None
        )
        
        # Guardar en Firestore
        feedback.save()
        
        return jsonify({'status': 'success', 'data': feedback.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El feedback ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un feedback existente
@feedback_bp.route('/<id_feedback>/', methods=['PUT'])
def update_feedback(id_feedback):
    try:
        data = request.get_json()
        feedback = Feedback.collection.get(id_feedback)
        if not feedback:
            return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
        
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
        updatable_fields = ['residente', 'tipo', 'comentario', 'fecha', 'personal_asignado']
        for key, value in data.items():
            if key in updatable_fields and hasattr(feedback, key):
                setattr(feedback, key, value)
        
        # Guardar cambios
        feedback.save()
        
        return jsonify({'status': 'success', 'data': feedback.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un feedback
@feedback_bp.route('/<id_feedback>/', methods=['DELETE'])
def delete_feedback(id_feedback):
    try:
        feedback = Feedback.collection.get(id_feedback)
        if not feedback:
            return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
        
        # Eliminar el feedback
        feedback.delete()
        
        return jsonify({'status': 'success', 'message': 'Feedback eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Feedback no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
