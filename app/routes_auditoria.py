from flask import Blueprint, request, jsonify, session
from app import db
from app.models_auditoria import Auditoria

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/inv')


def _verificar_sesion():
    return request.headers.get("X-USER-ID") is not None


@auditoria_bp.route('/auditoria', methods=['GET'])
def listar_auditoria():
    if not _verificar_sesion():
        return jsonify({'error': 'No autenticado'}), 401

    query = Auditoria.query

    entidad  = request.args.get('entidad')
    accion   = request.args.get('accion')
    username = request.headers.get('X-USERNAME')
    limite   = min(int(request.args.get('limite', 100)), 500)

    if entidad:
        query = query.filter(Auditoria.entidad == entidad)
    if accion:
        query = query.filter(Auditoria.accion == accion.upper())
    if username:
        query = query.filter(Auditoria.username == username)

    registros = query.order_by(Auditoria.fecha.desc()).limit(limite).all()

    return jsonify([r.to_dict() for r in registros]), 200


@auditoria_bp.route('/auditoria/<int:id_auditoria>', methods=['GET'])
def obtener_auditoria(id_auditoria):
    if not _verificar_sesion():
        return jsonify({'error': 'No autenticado'}), 401

    registro = Auditoria.query.get_or_404(id_auditoria)
    return jsonify(registro.to_dict()), 200
