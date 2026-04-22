class TestHealth:
    def test_health_retorna_ok(self, client):
        res = client.get('/health')
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'ok'
        assert data['servicio'] == 'inventario'


class TestListarProductos:
    def test_lista_vacia_al_inicio(self, client):
        res = client.get('/productos')
        assert res.status_code == 200
        assert res.get_json() == []

    def test_lista_productos_despues_de_crear(self, client, producto_id):
        res = client.get('/productos')
        assert res.status_code == 200
        productos = res.get_json()
        assert len(productos) == 1
        assert productos[0]['nombre'] == 'Monitor'


class TestCrearProducto:
    def test_crear_producto_completo(self, client):
        res = client.post('/productos', json={
            'nombre': 'Laptop',
            'descripcion': 'Laptop gaming',
            'cantidad': 5,
            'precio': 1500.0,
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data['producto']['nombre'] == 'Laptop'
        assert data['producto']['cantidad'] == 5
        assert data['producto']['precio'] == 1500.0

    def test_crear_producto_sin_nombre_retorna_400(self, client):
        res = client.post('/productos', json={'cantidad': 5, 'precio': 100.0})
        assert res.status_code == 400
        assert 'error' in res.get_json()

    def test_crear_producto_minimo(self, client):
        res = client.post('/productos', json={'nombre': 'Teclado'})
        assert res.status_code == 201
        data = res.get_json()
        assert data['producto']['nombre'] == 'Teclado'
        assert data['producto']['cantidad'] == 0


class TestObtenerProducto:
    def test_obtener_producto_existente(self, client, producto_id):
        res = client.get(f'/productos/{producto_id}')
        assert res.status_code == 200
        assert res.get_json()['nombre'] == 'Monitor'

    def test_obtener_producto_inexistente_retorna_404(self, client):
        res = client.get('/productos/9999')
        assert res.status_code == 404


class TestEditarProducto:
    def test_editar_cantidad(self, client, producto_id):
        res = client.put(f'/productos/{producto_id}', json={'cantidad': 20})
        assert res.status_code == 200
        assert res.get_json()['producto']['cantidad'] == 20

    def test_editar_nombre_y_precio(self, client, producto_id):
        res = client.put(f'/productos/{producto_id}', json={'nombre': 'Monitor Curvo', 'precio': 750.0})
        assert res.status_code == 200
        data = res.get_json()['producto']
        assert data['nombre'] == 'Monitor Curvo'
        assert data['precio'] == 750.0

    def test_editar_producto_inexistente_retorna_404(self, client):
        res = client.put('/productos/9999', json={'cantidad': 5})
        assert res.status_code == 404


class TestEliminarProducto:
    def test_eliminar_producto(self, client, producto_id):
        res = client.delete(f'/productos/{producto_id}')
        assert res.status_code == 200
        assert 'mensaje' in res.get_json()

    def test_producto_eliminado_no_existe(self, client, producto_id):
        client.delete(f'/productos/{producto_id}')
        res = client.get(f'/productos/{producto_id}')
        assert res.status_code == 404

    def test_eliminar_producto_inexistente_retorna_404(self, client):
        res = client.delete('/productos/9999')
        assert res.status_code == 404
