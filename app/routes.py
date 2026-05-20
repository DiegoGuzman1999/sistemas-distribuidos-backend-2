from flask import Blueprint, request, jsonify
from app import db
from app.models import Producto
from app.auditoria_service import registrar_auditoria

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inv')


@inventario_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'servicio': 'inventario'}), 200


@inventario_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()

    registrar_auditoria(
        db_session  = db.session,
        accion      = 'READ',
        entidad     = 'productos',
        descripcion = f'Listado de productos consultado ({len(productos)} registros)',
    )
    db.session.commit()

    return jsonify([p.to_dict() for p in productos]), 200


@inventario_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)

    registrar_auditoria(
        db_session  = db.session,
        accion      = 'READ',
        entidad     = 'productos',
        entidad_id  = producto.id,
        descripcion = f'Consulta individual: {producto.nombre}',
    )
    db.session.commit()

    return jsonify(producto.to_dict()), 200


@inventario_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()

    if not data.get('nombre'):
        return jsonify({'error': 'El nombre es requerido'}), 400

    producto = Producto(
        nombre      = data['nombre'],
        descripcion = data.get('descripcion', ''),
        cantidad    = data.get('cantidad', 0),
        precio      = data.get('precio', 0),
    )
    db.session.add(producto)
    db.session.flush()

    registrar_auditoria(
        db_session  = db.session,
        accion      = 'CREATE',
        entidad     = 'productos',
        entidad_id  = producto.id,
        descripcion = f'Producto creado: {producto.nombre} | '
                      f'cantidad={producto.cantidad}, precio={producto.precio}',
    )
    db.session.commit()

    return jsonify({'mensaje': 'Producto creado', 'producto': producto.to_dict()}), 201


@inventario_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()

    cambios = []
    if 'nombre' in data and data['nombre'] != producto.nombre:
        cambios.append(f'nombre: {producto.nombre} → {data["nombre"]}')
    if 'cantidad' in data and data['cantidad'] != producto.cantidad:
        cambios.append(f'cantidad: {producto.cantidad} → {data["cantidad"]}')
    if 'precio' in data and str(data['precio']) != str(producto.precio):
        cambios.append(f'precio: {producto.precio} → {data["precio"]}')

    producto.nombre      = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.cantidad    = data.get('cantidad', producto.cantidad)
    producto.precio      = data.get('precio', producto.precio)

    registrar_auditoria(
        db_session  = db.session,
        accion      = 'UPDATE',
        entidad     = 'productos',
        entidad_id  = producto.id,
        descripcion = f'Producto actualizado: {producto.nombre}' +
                      (f' | Cambios: {"; ".join(cambios)}' if cambios else ''),
    )
    db.session.commit()

    return jsonify({'mensaje': 'Producto actualizado', 'producto': producto.to_dict()}), 200


@inventario_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    nombre_guardado = producto.nombre

    registrar_auditoria(
        db_session  = db.session,
        accion      = 'DELETE',
        entidad     = 'productos',
        entidad_id  = id,
        descripcion = f'Producto eliminado: {nombre_guardado}',
    )

    db.session.delete(producto)
    db.session.commit()

    return jsonify({'mensaje': 'Producto eliminado'}), 200
