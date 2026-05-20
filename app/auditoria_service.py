from flask import session as flask_session
from app.models_auditoria import Auditoria


def registrar_auditoria(db_session, accion: str, entidad: str,
                         entidad_id: int = None, descripcion: str = None):
    usuario_id = flask_session.get('usuario_id')
    username   = flask_session.get('username', 'desconocido')

    if usuario_id is None:
        return

    registro = Auditoria(
        usuario_id  = usuario_id,
        username    = username,
        accion      = accion.upper(),
        entidad     = entidad,
        entidad_id  = entidad_id,
        descripcion = descripcion,
    )
    db_session.add(registro)
