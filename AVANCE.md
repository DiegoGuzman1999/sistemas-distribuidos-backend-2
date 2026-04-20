# AVANCE — sistemas-distribuidos-backend-2

## ¿Qué hace este repositorio?
Es el microservicio de **inventario**. Se encarga del CRUD completo de productos: listar, crear, editar y eliminar. El frontend consume este servicio para mostrar y gestionar el stock.

---

## ¿Por qué está separado del login?
Porque es un sistema distribuido con microservicios: cada servicio hace una sola cosa. Si el login falla, el inventario puede seguir funcionando de forma independiente.

---

## Estructura del repositorio

```
sistemas-distribuidos-backend-2/
├── app/
│   ├── __init__.py   ← Crea la app Flask y conecta la BD
│   ├── models.py     ← Define la tabla productos
│   └── routes.py     ← Endpoints CRUD de productos
├── run.py            ← Punto de entrada para correr el servidor
├── requirements.txt  ← Dependencias Python
├── Dockerfile        ← Imagen Docker del servicio
├── docker-compose.yml← Para correr solo este servicio
└── AVANCE.md         ← Este archivo
```

---

## Endpoints disponibles

| Método | Ruta              | Descripción                    |
|--------|-------------------|--------------------------------|
| GET    | /health           | Verifica que el servicio corre |
| GET    | /productos        | Lista todos los productos      |
| GET    | /productos/\<id\> | Obtiene un producto por ID     |
| POST   | /productos        | Crea un nuevo producto         |
| PUT    | /productos/\<id\> | Edita un producto existente    |
| DELETE | /productos/\<id\> | Elimina un producto            |

### Ejemplo de crear producto
**Request:**
```json
POST /productos
{
  "nombre": "Laptop",
  "descripcion": "Laptop gaming",
  "cantidad": 10,
  "precio": 1500.00
}
```
**Response:**
```json
{ "mensaje": "Producto creado", "producto": { "id": 1, "nombre": "Laptop", ... } }
```

---

## Puerto
Este servicio corre en el puerto **5001**.

---

## Historial de cambios

| Fecha      | Rama | Descripción                               |
|------------|------|-------------------------------------------|
| 2026-04-20 | dev  | Estructura inicial: API Flask de inventario (CRUD) |
