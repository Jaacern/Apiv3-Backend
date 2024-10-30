# backend/controllers/historialpago_controller.py

from flask import Blueprint, request, jsonify
from models import HistorialPago, Pago, Residente
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

historialpago_bp = Blueprint('historialpago_bp', __name__)

# Ruta: Obtener todos los historiales de pagos
@historialpago_bp.route('/', methods=['GET'])
def get_historiales_pagos():
    try:
        historiales = HistorialPago.collection.all()
        historiales_list = [hist.to_dict() for hist in historiales]
        return jsonify({'status': 'success', 'data': historiales_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un historial de pago por ID
@historialpago_bp.route('/<id_historial>/', methods=['GET'])
def get_historial_pago(id_historial):
    try:
        historial = HistorialPago.collection.get(id_historial)
        if historial:
            return jsonify({'status': 'success', 'data': historial.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo historial de pago
@historialpago_bp.route('/', methods=['POST'])
def create_historial_pago():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['pago', 'residente', 'fecha', 'descripcion']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el pago existe
        try:
            pago = Pago.collection.get(data['pago'])
            if not pago:
                return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404
        except DoesNotExist:
            return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404
        
        # Verificar que el residente existe
        try:
            residente = Residente.collection.get(data['residente'])
            if not residente:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        except DoesNotExist:
            return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Crear una instancia de HistorialPago
        historial_pago = HistorialPago(
            pago=data['pago'],
            residente=data['residente'],
            fecha=data['fecha'],
            descripcion=data['descripcion']
        )
        
        # Guardar en Firestore
        historial_pago.save()
        
        return jsonify({'status': 'success', 'data': historial_pago.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El historial de pago ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un historial de pago existente
@historialpago_bp.route('/<id_historial>/', methods=['PUT'])
def update_historial_pago(id_historial):
    try:
        data = request.get_json()
        historial = HistorialPago.collection.get(id_historial)
        if not historial:
            return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
        
        # Si se está actualizando el pago, verificar que exista
        if 'pago' in data:
            try:
                pago = Pago.collection.get(data['pago'])
                if not pago:
                    return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404
        
        # Si se está actualizando el residente, verificar que exista
        if 'residente' in data:
            try:
                residente = Residente.collection.get(data['residente'])
                if not residente:
                    return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
            except DoesNotExist:
                return jsonify({'status': 'error', 'message': 'Residente relacionado no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        updatable_fields = ['pago', 'residente', 'fecha', 'descripcion']
        for key, value in data.items():
            if key in updatable_fields and hasattr(historial, key):
                setattr(historial, key, value)
        
        # Guardar cambios
        historial.save()
        
        return jsonify({'status': 'success', 'data': historial.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un historial de pago
@historialpago_bp.route('/<id_historial>/', methods=['DELETE'])
def delete_historial_pago(id_historial):
    try:
        historial = HistorialPago.collection.get(id_historial)
        if not historial:
            return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
        
        # Eliminar el historial de pago
        historial.delete()
        
        return jsonify({'status': 'success', 'message': 'Historial de pago eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Historial de pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
