# firebase_config.py

import pyrebase

# Configuración de Firebase
firebaseConfig = {

}

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
