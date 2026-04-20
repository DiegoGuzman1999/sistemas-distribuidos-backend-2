from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY', 'clave-secreta-dev')

    db_url = (
        f"postgresql://{os.environ.get('DB_USER', 'admin')}:"
        f"{os.environ.get('DB_PASSWORD', 'admin123')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'inventario_db')}"
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import inventario_bp
    app.register_blueprint(inventario_bp)

    return app
