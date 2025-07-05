from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from models import User  # 👈 IMPORTANTE: tu modelo con UserMixin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from routes import main
        app.register_blueprint(main)

        db.create_all()

    return app

app = create_app()  # ✅ Esta línea es la clave

if __name__ == '__main__':
    app.run(debug=True)
