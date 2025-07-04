class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-super-segura'

    # Aquí la URL va directa, SIN os.environ.get()
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://avnadmin:AVNS_xlj5WYOprcR-tFN6xX1@mysql-1b6c1203-mirandadiazjesusdaniel-8cf4.k.aivencloud.com:21093/defaultdb'

    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {
                'ca': '/etc/ssl/certs/ca-certificates.crt'
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
