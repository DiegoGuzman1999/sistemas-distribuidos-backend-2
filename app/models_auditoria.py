from app import db


class Auditoria(db.Model):
    __tablename__ = 'auditoria'

    id_auditoria = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    accion = db.Column(db.String(20), nullable=False)
    entidad = db.Column(db.String(50), nullable=False)
    entidad_id = db.Column(db.Integer, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    fecha = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )