# backend/controllers/transaccion_controller.py

from flask import Blueprint, request, jsonify
from models import Transaccion, Departamento, Pago, Cuota
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

transaccion_bp = Blueprint('transaccion_bp', __name__)

# Ruta: Obtener todas las transacciones
@transaccion_bp.route('/', methods=['GET'])
def get_transacciones():
    try:
        transacciones = Transaccion.collection.all()
        transacciones_list = [trans.to_dict() for trans in transacciones]
        return jsonify({'status': 'success', 'data': transacciones_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener una transacción por ID
@transaccion_bp.route('/<id_transaccion>/', methods=['GET'])
def get_transaccion(id_transaccion):
    try:
        transaccion = Transaccion.collection.get(id_transaccion)
        if transaccion:
            return jsonify({'status': 'success', 'data': transaccion.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear una nueva transacción
@transaccion_bp.route('/', methods=['POST'])
def create_transaccion():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['tipo', 'descripcion', 'monto', 'fecha']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Opcional: Validar referencias a otras entidades
        departamento = None
        pago = None
        cuota = None

        if 'departamento' in data and data['departamento']:
            departamento = Departamento.collection.get(data['departamento'])
            if not departamento:
                return jsonify({'status': 'error', 'message': 'Departamento relacionado no encontrado.'}), 404

        if 'pago' in data and data['pago']:
            pago = Pago.collection.get(data['pago'])
            if not pago:
                return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404

        if 'cuota' in data and data['cuota']:
            cuota = Cuota.collection.get(data['cuota'])
            if not cuota:
                return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404

        # Crear una instancia de Transaccion
        transaccion = Transaccion(
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            monto=data['monto'],
            fecha=data['fecha'],
            departamento=data.get('departamento'),  # Puede ser None
            pago=data.get('pago'),  # Puede ser None
            cuota=data.get('cuota')  # Puede ser None
        )
        
        # Guardar en Firestore
        transaccion.save()
        
        return jsonify({'status': 'success', 'data': transaccion.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'La transacción ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar una transacción existente
@transaccion_bp.route('/<id_transaccion>/', methods=['PUT'])
def update_transaccion(id_transaccion):
    try:
        data = request.get_json()
        transaccion = Transaccion.collection.get(id_transaccion)
        if not transaccion:
            return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
        
        # Validar y actualizar referencias a otras entidades si se proporcionan
        if 'departamento' in data and data['departamento']:
            departamento = Departamento.collection.get(data['departamento'])
            if not departamento:
                return jsonify({'status': 'error', 'message': 'Departamento relacionado no encontrado.'}), 404

        if 'pago' in data and data['pago']:
            pago = Pago.collection.get(data['pago'])
            if not pago:
                return jsonify({'status': 'error', 'message': 'Pago relacionado no encontrado.'}), 404

        if 'cuota' in data and data['cuota']:
            cuota = Cuota.collection.get(data['cuota'])
            if not cuota:
                return jsonify({'status': 'error', 'message': 'Cuota relacionada no encontrada.'}), 404

        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(transaccion, key):
                setattr(transaccion, key, value)
        
        # Guardar cambios
        transaccion.save()
        
        return jsonify({'status': 'success', 'data': transaccion.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar una transacción
@transaccion_bp.route('/<id_transaccion>/', methods=['DELETE'])
def delete_transaccion(id_transaccion):
    try:
        transaccion = Transaccion.collection.get(id_transaccion)
        if not transaccion:
            return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
        
        # Eliminar la transacción
        transaccion.delete()
        
        return jsonify({'status': 'success', 'message': 'Transacción eliminada correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Transacción no encontrada.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
