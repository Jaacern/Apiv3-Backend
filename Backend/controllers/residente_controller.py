# backend/controllers/residente_controller.py

from flask import Blueprint, request, jsonify
from models import Residente, Departamento
from fireo.errors import DoesNotExist, Duplicate, NotFound
from fireo.query import Q

residente_bp = Blueprint('residente_bp', __name__)

# Ruta: Obtener todos los residentes
@residente_bp.route('/', methods=['GET'])
def get_residentes():
    try:
        residentes = Residente.collection.all()
        residentes_list = [res.to_dict() for res in residentes]
        return jsonify({'status': 'success', 'data': residentes_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Obtener un residente por ID
@residente_bp.route('/<id_residente>/', methods=['GET'])
def get_residente(id_residente):
    try:
        residente = Residente.collection.get(id_residente)
        if residente:
            return jsonify({'status': 'success', 'data': residente.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Crear un nuevo residente
@residente_bp.route('/', methods=['POST'])
def create_residente():
    try:
        data = request.get_json()
        
        # Validación básica de los campos requeridos
        required_fields = ['departamento', 'nombre', 'apepat', 'apemat', 'rut', 'telefono', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido.'}), 400
        
        # Verificar que el departamento existe
        departamento = Departamento.collection.get(data['departamento'])
        if not departamento:
            return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Crear una instancia de Residente
        residente = Residente(
            departamento=data['departamento'],
            nombre=data['nombre'],
            apepat=data['apepat'],
            apemat=data['apemat'],
            rut=data['rut'],
            telefono=data['telefono'],
            email=data['email']
        )
        
        # Guardar en Firestore
        residente.save()
        
        return jsonify({'status': 'success', 'data': residente.to_dict()}), 201
    except Duplicate:
        return jsonify({'status': 'error', 'message': 'El RUT del residente ya existe.'}), 409
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Actualizar un residente existente
@residente_bp.route('/<id_residente>/', methods=['PUT'])
def update_residente(id_residente):
    try:
        data = request.get_json()
        residente = Residente.collection.get(id_residente)
        if not residente:
            return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
        
        # Si se está actualizando el departamento, verificar que exista
        if 'departamento' in data:
            departamento = Departamento.collection.get(data['departamento'])
            if not departamento:
                return jsonify({'status': 'error', 'message': 'Departamento no encontrado.'}), 404
        
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if hasattr(residente, key):
                setattr(residente, key, value)
        
        # Guardar cambios
        residente.save()
        
        return jsonify({'status': 'success', 'data': residente.to_dict()}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta: Eliminar un residente
@residente_bp.route('/<id_residente>/', methods=['DELETE'])
def delete_residente(id_residente):
    try:
        residente = Residente.collection.get(id_residente)
        if not residente:
            return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
        
        # Eliminar el residente
        residente.delete()
        
        return jsonify({'status': 'success', 'message': 'Residente eliminado correctamente.'}), 200
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'Residente no encontrado.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
