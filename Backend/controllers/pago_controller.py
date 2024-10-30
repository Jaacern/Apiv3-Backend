# backend/controllers/pago_controller.py

from flask import Blueprint, request, jsonify
from models import Pago, Departamento
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

pago_bp = Blueprint('pago_bp', __name__)

# Ruta: Obtener todos los pagos
@pago_bp.route('/', methods=['GET'])
def get_pagos():
    try:
        pagos = Pago.collection.all()
        pagos_list = [pago.to_dict() for pago in pagos]
        return jsonify({'status': 'success', 'data': pagos_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un pago por ID
@pago_bp.route('/<id_pago>/', methods=['GET'])
def get_pago(id_pago):
    try:
        pago = Pago.collection.get(id_pago)
        if pago:
            return jsonify({'status': 'success', 'data': pago.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo pago
@pago_bp.route('/', methods=['POST'])
def create_pago():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['departamento', 'monto', 'fecha_pago', 'periodo', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el departamento existe
        departamento = Departamento.collection.get(data['departamento'])
        if not departamento:
            return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Crear una instancia de Pago
        pago = Pago(
            departamento=data['departamento'],
            monto=data['monto'],
            fecha_pago=data['fecha_pago'],
            periodo=data['periodo'],
            estado=data['estado']
        )
        
        # Guardar en Firestore
        pago.save()
        
        return jsonify({'status': 'success', 'data': pago.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El pago ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un pago existente
@pago_bp.route('/<id_pago>/', methods=['PUT'])
def update_pago(id_pago):
    try:
        data = request.get_json()
        pago = Pago.collection.get(id_pago)
        if not pago:
            return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
        
        # Si se está actualizando el departamento, verificar que exista
        if 'departamento' in data:
            departamento = Departamento.collection.get(data['departamento'])
            if not departamento:
                return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(pago, key):
                setattr(pago, key, value)
        
        # Guardar cambios
        pago.save()
        
        return jsonify({'status': 'success', 'data': pago.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un pago
@pago_bp.route('/<id_pago>/', methods=['DELETE'])
def delete_pago(id_pago):
    try:
        pago = Pago.collection.get(id_pago)
        if not pago:
            return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
        
        # Eliminar el pago
        pago.delete()
        
        return jsonify({'status': 'success', 'message': 'Pago eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Pago no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
