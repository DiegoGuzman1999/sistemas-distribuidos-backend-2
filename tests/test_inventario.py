import pytest



class TestHealth:
    def test_health_ok(self, client):
        res = client.get('/inv/health')
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'ok'
        assert data['servicio'] == 'inventario'



class TestListarProductos:
    def test_lista_vacia(self, client):
        res = client.get('/inv/productos')
        assert res.status_code == 200
        assert res.get_json() == []

    def test_lista_con_productos(self, client, producto_base):
        res = client.get('/inv/productos')
        assert res.status_code == 200
        assert len(res.get_json()) == 1



class TestObtenerProducto:
    def test_obtener_existente(self, client, producto_base):
        res = client.get(f'/inv/productos/{producto_base}')
        assert res.status_code == 200
        assert res.get_json()['nombre'] == 'Laptop'

    def test_obtener_inexistente(self, client):
        res = client.get('/inv/productos/9999')
        assert res.status_code == 404



class TestCrearProducto:
    def test_crear_ok(self, client):
        res = client.post('/inv/productos',
                          json={'nombre': 'Mouse', 'cantidad': 50, 'precio': 25.99})
        assert res.status_code == 201
        data = res.get_json()
        assert data['producto']['nombre'] == 'Mouse'
        assert data['producto']['cantidad'] == 50

    def test_crear_sin_nombre(self, client):
        res = client.post('/inv/productos', json={'cantidad': 10, 'precio': 5.0})
        assert res.status_code == 400
        assert 'error' in res.get_json()

    def test_crear_campos_opcionales_por_defecto(self, client):
        res = client.post('/inv/productos', json={'nombre': 'Teclado'})
        assert res.status_code == 201
        prod = res.get_json()['producto']
        assert prod['cantidad'] == 0



class TestEditarProducto:
    def test_editar_nombre(self, client, producto_base):
        res = client.put(f'/inv/productos/{producto_base}',
                         json={'nombre': 'Laptop Pro'})
        assert res.status_code == 200
        assert res.get_json()['producto']['nombre'] == 'Laptop Pro'

    def test_editar_cantidad(self, client, producto_base):
        res = client.put(f'/inv/productos/{producto_base}',
                         json={'cantidad': 99})
        assert res.status_code == 200
        assert res.get_json()['producto']['cantidad'] == 99

    def test_editar_inexistente(self, client):
        res = client.put('/inv/productos/9999', json={'nombre': 'X'})
        assert res.status_code == 404



class TestEliminarProducto:
    def test_eliminar_ok(self, client, producto_base):
        res = client.delete(f'/inv/productos/{producto_base}')
        assert res.status_code == 200
        # Verificar que ya no existe
        res2 = client.get(f'/inv/productos/{producto_base}')
        assert res2.status_code == 404

    def test_eliminar_inexistente(self, client):
        res = client.delete('/inv/productos/9999')
        assert res.status_code == 404



class TestVentas:
    def test_listar_ventas_vacio(self, client):
        res = client.get('/inv/ventas')
        assert res.status_code == 200
        assert res.get_json() == []

    def test_registrar_venta_ok(self, client, producto_base):
        res = client.post('/inv/ventas',
                          json={'producto_id': producto_base, 'cantidad_vendida': 3})
        assert res.status_code == 201
        venta = res.get_json()['venta']
        assert venta['cantidad_vendida'] == 3
        assert float(venta['total']) == pytest.approx(4500.00)

    def test_registrar_venta_stock_insuficiente(self, client, producto_base):
        res = client.post('/inv/ventas',
                          json={'producto_id': producto_base, 'cantidad_vendida': 999})
        assert res.status_code == 400
        assert 'Stock insuficiente' in res.get_json()['error']

    def test_registrar_venta_sin_campos(self, client):
        res = client.post('/inv/ventas', json={})
        assert res.status_code == 400

    def test_reporte_ventas(self, client, producto_base):
        client.post('/inv/ventas',
                    json={'producto_id': producto_base, 'cantidad_vendida': 2})
        res = client.get('/inv/ventas/reporte')
        assert res.status_code == 200
        resumen = res.get_json()['resumen']
        assert resumen['total_ventas'] >= 1
        assert resumen['total_ingresos'] > 0
