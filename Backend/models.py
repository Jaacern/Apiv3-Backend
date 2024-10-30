from fireo.models import Model
from fireo.fields import (
    IDField, TextField, NumberField, BooleanField,
    ReferenceField, ListField, datetime_field
)

# Usar DateTimeField desde FireO
DateTimeField = datetime_field.DateTimeField

import re

# Función de validación para el correo electrónico
def validate_email(value):
    email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if not email_pattern.match(value):
        raise ValueError('El correo electrónico no es válido.')

# Definición de constantes para los campos de elección (ENUM)
DEPARTAMENTO_TIPO = ['Propietario', 'Arriendo']
DEPARTAMENTO_ESTADO = ['Ocupado', 'Disponible', 'En Mantenimiento']
PERSONAL_CARGO = ['Mantenimiento', 'Conserje', 'Instalaciones', 'Atención']
GASTO_COMUN_TIPO = ['Agua', 'Gas', 'Luz', 'Internet', 'Remuneraciones', 'Insumos', 'Extraordinario', 'Servicio', 'Otro']
PAGO_ESTADO = ['Pagado', 'Pendiente', 'Atrasado']
MOROSIDAD_ESTADO = ['Activo', 'Cancelado']
NOTIFICACION_TIPO = ['Recordatorio', 'Penalización', 'Aviso de Mantención', 'Emergencia']
NOTIFICACION_ESTADO = ['Enviado', 'Leído', 'Fallido']
PENALIZACION_ESTADO = ['Aplicada', 'Revertida']
HISTORIAL_PAGO_ESTADO = ['Completado', 'Parcial', 'Fallido']
SOLICITUD_TIPO = ['Mantenimiento', 'Reparación', 'Servicio General', 'Otro']
SOLICITUD_ESTADO = ['Pendiente', 'En Proceso', 'Completada', 'Cancelada']
SOLICITUD_PRIORIDAD = ['Baja', 'Media', 'Alta']
QUEJA_ESTADO = ['Pendiente', 'En Revisión', 'Resuelta', 'Rechazada']
FEEDBACK_TIPO = ['Positivo', 'Negativo', 'Sugerencia']

# Función de validación para el RUT chileno
def validate_rut(value):
    rut_pattern = re.compile(r'^\d{7,8}-?[\dkK]$')
    if not rut_pattern.match(value):
        raise ValueError('El RUT no tiene un formato válido.')

# Entidad: Departamento
class Departamento(Model):
    id_departamento = IDField(primary_key=True)
    numero = TextField(required=True, unique=True)
    piso = NumberField(required=True)
    tipo = TextField(choices=DEPARTAMENTO_TIPO, required=True)
    superficie = NumberField(required=True)
    estado = TextField(choices=DEPARTAMENTO_ESTADO, required=True)

    def __str__(self):
        return f'Departamento {self.numero} - Piso {self.piso}'

# Entidad: Cuota
class Cuota(Model):
    id_cuota = IDField(primary_key=True)
    departamento = ReferenceField(Departamento, required=True, reverse_delete=True)
    monto = NumberField(required=True)
    periodo = TextField(required=True)
    fecha_vencimiento = DateTimeField(required=True)
    estado = TextField(choices=['Pagada', 'Pendiente', 'Atrasada'], required=True)

    def __str__(self):
        return f'Cuota {self.id_cuota} - Departamento {self.departamento.numero} - {self.periodo}'

# Entidad: Propietario
class Propietario(Model):
    id_propietario = IDField(primary_key=True)
    nombre = TextField(required=True)
    apepat = TextField(required=True)
    apemat = TextField(required=True)
    rut = TextField(required=True, unique=True, validators=[validate_rut])
    telefono = TextField(required=True)
    email = TextField(required=True, validators=[validate_email])
    direccion = TextField(required=True)

    def __str__(self):
        return f'{self.nombre} {self.apepat} {self.apemat}'

# Entidad: Residente
class Residente(Model):
    id_residente = IDField(primary_key=True)
    departamento = ReferenceField(Departamento, required=True, reverse_delete=True)
    nombre = TextField(required=True)
    rut = TextField(required=True, unique=True, validators=[validate_rut])
    apepat = TextField(required=True)
    apemat = TextField(required=True)
    telefono = TextField(required=True)
    email = TextField(required=True, validators=[validate_email])

    def __str__(self):
        return f'{self.nombre} {self.apepat} {self.apemat}'

# Entidad: Personal
class Personal(Model):
    id_personal = IDField(primary_key=True)
    nombre = TextField(required=True)
    apepat = TextField(required=True)
    apemat = TextField(required=True)
    cargo = TextField(choices=PERSONAL_CARGO, required=True)
    telefono = TextField(required=True)
    email = TextField(required=True, validators=[validate_email])
    fecha_contratacion = DateTimeField(required=True)

    def __str__(self):
        return f'{self.nombre} {self.apepat} {self.apemat} - {self.cargo}'

# Entidad: GastoComun
class GastoComun(Model):
    id_gasto = IDField(primary_key=True)
    tipo = TextField(choices=GASTO_COMUN_TIPO, required=True)
    descripcion = TextField(required=True)
    monto = NumberField(required=True)
    fecha = DateTimeField(required=True)
    estado = TextField(choices=['Pagado', 'Pendiente'], required=True)

    def __str__(self):
        return f'{self.tipo} - {self.descripcion} - {self.monto}'

# Entidad: Pago
class Pago(Model):
    id_pago = IDField(primary_key=True)
    departamento = ReferenceField(Departamento, required=True, reverse_delete=True)
    monto = NumberField(required=True)
    fecha_pago = DateTimeField(required=True)
    periodo = TextField(required=True)
    estado = TextField(choices=PAGO_ESTADO, required=True)

    def __str__(self):
        return f'Pago {self.id_pago} - Departamento {self.departamento.numero} - {self.monto}'

# Entidad: Mantenimiento
class Mantenimiento(Model):
    id_mantenimiento = IDField(primary_key=True)
    tipo = TextField(required=True)
    descripcion = TextField(required=True)
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField(required=True)
    costo = NumberField(required=True)
    personal = ReferenceField(Personal, required=False, reverse_delete=True)
    estado = TextField(choices=['Pendiente', 'En Proceso', 'Completado'], required=True)

    def __str__(self):
        return f'Mantenimiento {self.id_mantenimiento} - {self.tipo} - {self.estado}'

# Entidad: Transaccion
class Transaccion(Model):
    id_transaccion = IDField(primary_key=True)
    tipo = TextField(choices=['Ingreso', 'Egreso'], required=True)
    descripcion = TextField(required=True)
    monto = NumberField(required=True)
    fecha = DateTimeField(required=True)
    departamento = ReferenceField(Departamento, required=False, reverse_delete=True)

    def __str__(self):
        return f'Transacción {self.id_transaccion} - {self.tipo} - {self.monto}'

# Entidad: Morosidad
class Morosidad(Model):
    id_morosidad = IDField(primary_key=True)
    pago = ReferenceField(Pago, required=True, reverse_delete=True)
    monto_atrasado = NumberField(required=True)
    fecha_retraso = DateTimeField(required=True)
    intereses = NumberField(required=True)
    estado = TextField(choices=MOROSIDAD_ESTADO, required=True)
    fecha_cancelacion = DateTimeField(required=False)

    def __str__(self):
        return f'Morosidad {self.id_morosidad} - Pago {self.pago.id_pago} - {self.monto_atrasado}'

# Entidad: Notificacion
class Notificacion(Model):
    id_notificacion = IDField(primary_key=True)
    residente = ReferenceField(Residente, required=True, reverse_delete=True)
    tipo = TextField(choices=NOTIFICACION_TIPO, required=True)
    mensaje = TextField(required=True)
    fecha_envio = DateTimeField(required=True)
    estado = TextField(choices=NOTIFICACION_ESTADO, required=True)

    def __str__(self):
        return f'Notificación {self.id_notificacion} - Residente {self.residente.id_residente} - {self.tipo}'

# Entidad: Penalizacion
class Penalizacion(Model):
    id_penalizacion = IDField(primary_key=True)
    morosidad = ReferenceField(Morosidad, required=True, reverse_delete=True)
    monto = NumberField(required=True)
    descripcion = TextField(required=True)
    fecha_aplicacion = DateTimeField(required=True)
    estado = TextField(choices=PENALIZACION_ESTADO, required=True)

    def __str__(self):
        return f'Penalización {self.id_penalizacion} - Morosidad {self.morosidad.id_morosidad} - {self.monto}'

# Entidad: HistorialPago
class HistorialPago(Model):
    id_historial_pago = IDField(primary_key=True)
    pago = ReferenceField(Pago, required=True, reverse_delete=True)
    fecha_pago = DateTimeField(required=True)
    monto_pagado = NumberField(required=True)
    metodo_pago = TextField(choices=['Transferencia', 'Tarjeta', 'Efectivo', 'Otro'], required=True)
    referencia_pago = TextField(required=False)
    estado = TextField(choices=HISTORIAL_PAGO_ESTADO, required=True)

    def __str__(self):
        return f'HistorialPago {self.id_historial_pago} - Pago {self.pago.id_pago} - {self.monto_pagado}'

# Entidad: Solicitud
class Solicitud(Model):
    id_solicitud = IDField(primary_key=True)
    residente = ReferenceField(Residente, required=True, reverse_delete=True)
    tipo = TextField(choices=SOLICITUD_TIPO, required=True)
    descripcion = TextField(required=True)
    fecha_creacion = DateTimeField(required=True)
    estado = TextField(choices=SOLICITUD_ESTADO, required=True)
    prioridad = TextField(choices=SOLICITUD_PRIORIDAD, required=True)
    personal = ReferenceField(Personal, required=False, reverse_delete=True)

    def __str__(self):
        return f'Solicitud {self.id_solicitud} - Residente {self.residente.id_residente} - {self.tipo}'

# Entidad: Queja
class Queja(Model):
    id_queja = IDField(primary_key=True)
    residente = ReferenceField(Residente, required=True, reverse_delete=True)
    descripcion = TextField(required=True)
    fecha_creacion = DateTimeField(required=True)
    estado = TextField(choices=QUEJA_ESTADO, required=True)
    fecha_resolucion = DateTimeField(required=False)
    personal = ReferenceField(Personal, required=False, reverse_delete=True)

    def __str__(self):
        return f'Queja {self.id_queja} - Residente {self.residente.id_residente} - {self.estado}'

# Entidad: Feedback
class Feedback(Model):
    id_feedback = IDField(primary_key=True)
    residente = ReferenceField(Residente, required=True, reverse_delete=True)
    tipo = TextField(choices=FEEDBACK_TIPO, required=True)
    comentarios = TextField(required=True)
    fecha_creacion = DateTimeField(required=True)
    estado = TextField(choices=['Nuevo', 'En Revisión', 'Atendido'], required=True)

    def __str__(self):
        return f'Feedback {self.id_feedback} - Residente {self.residente.id_residente} - {self.tipo}'
