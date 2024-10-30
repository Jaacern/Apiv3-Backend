# backend/controllers/morosidad_controller.py

from flask import Blueprint, request, jsonify
from models import Morosidad, Residente, Cuota
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

morosidad_bp = Blueprint('morosidad_bp', __name__)

# Ruta: Obtener todas las morosidades
@morosidad_bp.route('/', methods=['GET'])
def get_morosidades():
    try:
        morosidades = Morosidad.collection.all()
        morosidades_list = [mor.to_dict() for mor in morosidades]
        return jsonify({'status': 'success', 'data': morosidades_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una morosidad por ID
@morosidad_bp.route('/<id_morosidad>/', methods=['GET'])
def get_morosidad(id_morosidad):
    try:
        morosidad = Morosidad.collection.get(id_morosidad)
        if morosidad:
            return jsonify({'status': 'success', 'data': morosidad.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva morosidad
@morosidad_bp.route('/', methods=['POST'])
def create_morosidad():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['residente', 'cuota', 'monto', 'fecha_inicio', 'fecha_fin', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el residente existe
        residente = Residente.collection.get(data['residente'])
        if not residente:
            return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Verificar que la cuota existe
        cuota = Cuota.collection.get(data['cuota'])
        if not cuota:
            return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
        
        # Crear una instancia de Morosidad
        morosidad = Morosidad(
            residente=data['residente'],
            cuota=data['cuota'],
            monto=data['monto'],
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            estado=data['estado']
        )
        
        # Guardar en Firestore
        morosidad.save()
        
        return jsonify({'status': 'success', 'data': morosidad.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La morosidad ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una morosidad existente
@morosidad_bp.route('/<id_morosidad>/', methods=['PUT'])
def update_morosidad(id_morosidad):
    try:
        data = request.get_json()
        morosidad = Morosidad.collection.get(id_morosidad)
        if not morosidad:
            return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
        
        # Si se está actualizando el residente, verificar que exista
        if 'residente' in data:
            residente = Residente.collection.get(data['residente'])
            if not residente:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Si se está actualizando la cuota, verificar que exista
        if 'cuota' in data:
            cuota = Cuota.collection.get(data['cuota'])
            if not cuota:
                return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(morosidad, key):
                setattr(morosidad, key, value)
        
        # Guardar cambios
        morosidad.save()
        
        return jsonify({'status': 'success', 'data': morosidad.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una morosidad
@morosidad_bp.route('/<id_morosidad>/', methods=['DELETE'])
def delete_morosidad(id_morosidad):
    try:
        morosidad = Morosidad.collection.get(id_morosidad)
        if not morosidad:
            return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
        
        # Eliminar la morosidad
        morosidad.delete()
        
        return jsonify({'status': 'success', 'message': 'Morosidad eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Morosidad no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
