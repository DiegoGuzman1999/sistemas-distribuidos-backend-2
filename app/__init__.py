from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost", "http://127.0.0.1"])

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
    from app.routes_ventas import ventas_bp
    app.register_blueprint(inventario_bp)
    app.register_blueprint(ventas_bp)

    return app
