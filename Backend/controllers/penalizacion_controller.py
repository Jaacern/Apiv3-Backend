# backend/controllers/penalizacion_controller.py

from flask import Blueprint, request, jsonify
from models import Penalizacion, Residente, Cuota
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

penalizacion_bp = Blueprint('penalizacion_bp', __name__)

# Ruta: Obtener todas las penalizaciones
@penalizacion_bp.route('/', methods=['GET'])
def get_penalizaciones():
    try:
        penalizaciones = Penalizacion.collection.all()
        penalizaciones_list = [pen.to_dict() for pen in penalizaciones]
        return jsonify({'status': 'success', 'data': penalizaciones_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una penalización por ID
@penalizacion_bp.route('/<id_penalizacion>/', methods=['GET'])
def get_penalizacion(id_penalizacion):
    try:
        penalizacion = Penalizacion.collection.get(id_penalizacion)
        if penalizacion:
            return jsonify({'status': 'success', 'data': penalizacion.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva penalización
@penalizacion_bp.route('/', methods=['POST'])
def create_penalizacion():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['residente', 'cuota', 'monto', 'fecha', 'descripcion']
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
        
        # Verificar que la cuota existe
        try:
            cuota = Cuota.collection.get(data['cuota'])
            if not cuota:
                return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
        except DoesNotExist:
            return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
        
        # Crear una instancia de Penalizacion
        penalizacion = Penalizacion(
            residente=data['residente'],
            cuota=data['cuota'],
            monto=data['monto'],
            fecha=data['fecha'],
            descripcion=data['descripcion']
        )
        
        # Guardar en Firestore
        penalizacion.save()
        
        return jsonify({'status': 'success', 'data': penalizacion.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La penalización ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una penalización existente
@penalizacion_bp.route('/<id_penalizacion>/', methods=['PUT'])
def update_penalizacion(id_penalizacion):
    try:
        data = request.get_json()
        penalizacion = Penalizacion.collection.get(id_penalizacion)
        if not penalizacion:
            return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
        
        # Si se está actualizando el residente, verificar que exista
        if 'residente' in data:
            try:
                residente = Residente.collection.get(data['residente'])
                if not residente:
                    return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Si se está actualizando la cuota, verificar que exista
        if 'cuota' in data:
            try:
                cuota = Cuota.collection.get(data['cuota'])
                if not cuota:
                    return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
        
        # Actualizar los campos proporcionados
        updatable_fields = ['residente', 'cuota', 'monto', 'fecha', 'descripcion']
        for key, value in data.items():
            if key in updatable_fields and hasattr(penalizacion, key):
                setattr(penalizacion, key, value)
        
        # Guardar cambios
        penalizacion.save()
        
        return jsonify({'status': 'success', 'data': penalizacion.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una penalización
@penalizacion_bp.route('/<id_penalizacion>/', methods=['DELETE'])
def delete_penalizacion(id_penalizacion):
    try:
        penalizacion = Penalizacion.collection.get(id_penalizacion)
        if not penalizacion:
            return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
        
        # Eliminar la penalización
        penalizacion.delete()
        
        return jsonify({'status': 'success', 'message': 'Penalización eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Penalización no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
