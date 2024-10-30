# backend/controllers/gastocomun_controller.py

from flask import Blueprint, request, jsonify
from models import GastoComun
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

gastocomun_bp = Blueprint('gastocomun_bp', __name__)

# Ruta: Obtener todos los gastos comunes
@gastocomun_bp.route('/', methods=['GET'])
def get_gastos_comunes():
    try:
        gastos = GastoComun.collection.all()
        gastos_list = [gasto.to_dict() for gasto in gastos]
        return jsonify({'status': 'success', 'data': gastos_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un gasto común por ID
@gastocomun_bp.route('/<id_gasto>/', methods=['GET'])
def get_gasto_comun(id_gasto):
    try:
        gasto = GastoComun.collection.get(id_gasto)
        if gasto:
            return jsonify({'status': 'success', 'data': gasto.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo gasto común
@gastocomun_bp.route('/', methods=['POST'])
def create_gasto_comun():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['tipo', 'descripcion', 'monto', 'fecha', 'estado']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Crear una instancia de GastoComun
        gasto = GastoComun(
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            monto=data['monto'],
            fecha=data['fecha'],
            estado=data['estado']
        )
        
        # Guardar en Firestore
        gasto.save()
        
        return jsonify({'status': 'success', 'data': gasto.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El gasto común ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un gasto común existente
@gastocomun_bp.route('/<id_gasto>/', methods=['PUT'])
def update_gasto_comun(id_gasto):
    try:
        data = request.get_json()
        gasto = GastoComun.collection.get(id_gasto)
        if not gasto:
            return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(gasto, key):
                setattr(gasto, key, value)
        
        # Guardar cambios
        gasto.save()
        
        return jsonify({'status': 'success', 'data': gasto.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un gasto común
@gastocomun_bp.route('/<id_gasto>/', methods=['DELETE'])
def delete_gasto_comun(id_gasto):
    try:
        gasto = GastoComun.collection.get(id_gasto)
        if not gasto:
            return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
        
        # Eliminar el gasto común
        gasto.delete()
        
        return jsonify({'status': 'success', 'message': 'Gasto común eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Gasto común no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
