from flask import Flask
from controllers.cuota_controller import cuota_bp
from controllers.departamento_controller import departamento_bp
from controllers.feedback_controller import feedback_bp
from controllers.gastocomun_controller import gastocomun_bp
from controllers.historialpago_controller import historialpago_bp
from controllers.mantenimiento_controller import mantenimiento_bp
from controllers.morosidad_controller import morosidad_bp
from controllers.notificacion_controller import notificacion_bp
from controllers.pago_controller import pago_bp
from controllers.penalizacion_controller import penalizacion_bp
from controllers.personal_controller import personal_bp
from controllers.propietario_controller import propietario_bp
from controllers.queja_controller import queja_bp
from controllers.residente_controller import residente_bp
from controllers.solicitud_controller import solicitud_bp
from controllers.transaccion_controller import transaccion_bp

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración opcional
app.config['DEBUG'] = True  # Activa el modo de depuración

# Registro de los controladores
app.register_blueprint(cuota_bp, url_prefix='/api/cuota')
app.register_blueprint(departamento_bp, url_prefix='/api/departamento')
app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
app.register_blueprint(gastocomun_bp, url_prefix='/api/gastocomun')
app.register_blueprint(historialpago_bp, url_prefix='/api/historialpago')
app.register_blueprint(mantenimiento_bp, url_prefix='/api/mantenimiento')
app.register_blueprint(morosidad_bp, url_prefix='/api/morosidad')
app.register_blueprint(notificacion_bp, url_prefix='/api/notificacion')
app.register_blueprint(pago_bp, url_prefix='/api/pago')
app.register_blueprint(penalizacion_bp, url_prefix='/api/penalizacion')
app.register_blueprint(personal_bp, url_prefix='/api/personal')
app.register_blueprint(propietario_bp, url_prefix='/api/propietario')
app.register_blueprint(queja_bp, url_prefix='/api/queja')
app.register_blueprint(residente_bp, url_prefix='/api/residente')
app.register_blueprint(solicitud_bp, url_prefix='/api/solicitud')
app.register_blueprint(transaccion_bp, url_prefix='/api/transaccion')

# Ruta de prueba para verificar que el servidor esté en funcionamiento
@app.route('/')
def home():
    return "API de gestión funcionando correctamente!"

# Lanza la aplicación si el archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
