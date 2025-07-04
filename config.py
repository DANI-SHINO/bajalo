import os

class Config:
    # Clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-super-segura'

    # URL de conexión (sin ?ssl-mode=REQUIRED)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Opciones de SQLAlchemy (usa SSL de forma correcta)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {
                'ca': '/etc/ssl/certs/ca-certificates.crt'
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo (ajusta si la usas)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
