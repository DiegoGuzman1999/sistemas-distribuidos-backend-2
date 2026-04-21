from app import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    cantidad_vendida = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_venta = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'nombre_producto': self.nombre_producto,
            'cantidad_vendida': self.cantidad_vendida,
            'precio_unitario': float(self.precio_unitario),
            'total': float(self.total),
            'fecha_venta': str(self.fecha_venta)
        }
