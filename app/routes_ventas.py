from flask import Blueprint, request, jsonify
from app import db
from app.models import Producto
from app.models_venta import Venta
from sqlalchemy import func

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas', methods=['GET'])
def listar_ventas():
    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()
    return jsonify([v.to_dict() for v in ventas]), 200

@ventas_bp.route('/ventas', methods=['POST'])
def registrar_venta():
    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad_vendida')

    if not producto_id or not cantidad:
        return jsonify({'error': 'producto_id y cantidad_vendida son requeridos'}), 400

    producto = Producto.query.get_or_404(producto_id)

    if producto.cantidad < cantidad:
        return jsonify({'error': f'Stock insuficiente. Disponible: {producto.cantidad}'}), 400

    venta = Venta(
        producto_id=producto.id,
        nombre_producto=producto.nombre,
        cantidad_vendida=cantidad,
        precio_unitario=producto.precio,
        total=float(producto.precio) * cantidad
    )

    producto.cantidad -= cantidad
    db.session.add(venta)
    db.session.commit()

    return jsonify({'mensaje': 'Venta registrada', 'venta': venta.to_dict()}), 201

@ventas_bp.route('/ventas/reporte', methods=['GET'])
def reporte_ventas():
    total_ventas = db.session.query(func.count(Venta.id)).scalar()
    total_ingresos = db.session.query(func.sum(Venta.total)).scalar() or 0
    total_productos_vendidos = db.session.query(func.sum(Venta.cantidad_vendida)).scalar() or 0

    top_productos = db.session.query(
        Venta.nombre_producto,
        func.sum(Venta.cantidad_vendida).label('total_vendido'),
        func.sum(Venta.total).label('total_ingresos')
    ).group_by(Venta.nombre_producto)\
     .order_by(func.sum(Venta.cantidad_vendida).desc())\
     .limit(5).all()

    return jsonify({
        'resumen': {
            'total_ventas': total_ventas,
            'total_ingresos': float(total_ingresos),
            'total_productos_vendidos': int(total_productos_vendidos)
        },
        'top_productos': [
            {
                'nombre': r.nombre_producto,
                'total_vendido': int(r.total_vendido),
                'total_ingresos': float(r.total_ingresos)
            } for r in top_productos
        ]
    }), 200
