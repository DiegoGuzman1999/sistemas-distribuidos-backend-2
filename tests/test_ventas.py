class TestListarVentas:
    def test_lista_vacia_al_inicio(self, client):
        res = client.get('/ventas')
        assert res.status_code == 200
        assert res.get_json() == []


class TestRegistrarVenta:
    def test_registrar_venta_exitosa(self, client, producto_id):
        res = client.post('/ventas', json={
            'producto_id': producto_id,
            'cantidad_vendida': 3,
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data['venta']['cantidad_vendida'] == 3
        assert data['venta']['total'] == 1500.0  # 3 * 500

    def test_venta_reduce_stock(self, client, producto_id):
        client.post('/ventas', json={'producto_id': producto_id, 'cantidad_vendida': 3})
        res = client.get(f'/productos/{producto_id}')
        assert res.get_json()['cantidad'] == 7  # 10 - 3

    def test_venta_stock_insuficiente_retorna_400(self, client, producto_id):
        res = client.post('/ventas', json={
            'producto_id': producto_id,
            'cantidad_vendida': 100,
        })
        assert res.status_code == 400
        assert 'Stock insuficiente' in res.get_json()['error']

    def test_venta_sin_producto_id_retorna_400(self, client):
        res = client.post('/ventas', json={'cantidad_vendida': 2})
        assert res.status_code == 400

    def test_venta_sin_cantidad_retorna_400(self, client, producto_id):
        res = client.post('/ventas', json={'producto_id': producto_id})
        assert res.status_code == 400

    def test_venta_cuerpo_vacio_retorna_400(self, client):
        res = client.post('/ventas', json={})
        assert res.status_code == 400

    def test_venta_producto_inexistente_retorna_404(self, client):
        res = client.post('/ventas', json={'producto_id': 9999, 'cantidad_vendida': 1})
        assert res.status_code == 404


class TestReporteVentas:
    def test_reporte_sin_ventas(self, client):
        res = client.get('/ventas/reporte')
        assert res.status_code == 200
        data = res.get_json()
        assert data['resumen']['total_ventas'] == 0
        assert data['resumen']['total_ingresos'] == 0
        assert data['resumen']['total_productos_vendidos'] == 0
        assert data['top_productos'] == []

    def test_reporte_con_ventas(self, client, producto_id):
        client.post('/ventas', json={'producto_id': producto_id, 'cantidad_vendida': 2})
        res = client.get('/ventas/reporte')
        assert res.status_code == 200
        data = res.get_json()
        assert data['resumen']['total_ventas'] == 1
        assert data['resumen']['total_productos_vendidos'] == 2
        assert data['resumen']['total_ingresos'] == 1000.0
        assert len(data['top_productos']) == 1
        assert data['top_productos'][0]['nombre'] == 'Monitor'
