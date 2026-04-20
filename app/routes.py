from flask import Blueprint, request, jsonify
from app import db
from app.models import Producto

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'servicio': 'inventario'}), 200

@inventario_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos]), 200

@inventario_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict()), 200

@inventario_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()

    if not data.get('nombre'):
        return jsonify({'error': 'El nombre es requerido'}), 400

    producto = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        cantidad=data.get('cantidad', 0),
        precio=data.get('precio', 0)
    )
    db.session.add(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto creado', 'producto': producto.to_dict()}), 201

@inventario_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()

    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.cantidad = data.get('cantidad', producto.cantidad)
    producto.precio = data.get('precio', producto.precio)

    db.session.commit()
    return jsonify({'mensaje': 'Producto actualizado', 'producto': producto.to_dict()}), 200

@inventario_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado'}), 200
