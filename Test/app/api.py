from flask import Flask, request, jsonify
from typing import Tuple, Dict, Union
import sqlite3
from functools import wraps
from dataclasses import dataclass

app = Flask(__name__)


# Clase para representar un producto
@dataclass
class Producto:
    id: int
    nombre: str
    cantidad: int


def init_db():
    """Inicializa la base de datos con una tabla de productos"""
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS productos
        (id INTEGER PRIMARY KEY, nombre TEXT, cantidad INTEGER)
    ''')
    conn.commit()
    conn.close()


def validar_id(func):
    """Decorador para validar IDs de producto"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            id_producto = kwargs.get('id_producto') or args[0]
            if not isinstance(id_producto, int) or id_producto <= 0:
                return jsonify({"error": "ID de producto debe ser un número entero positivo"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "ID de producto inválido"}), 400
        return func(*args, **kwargs)

    return wrapper


def validar_cantidad(func):
    """Decorador para validar cantidades"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            cantidad = kwargs.get('cantidad') or args[1]
            if not isinstance(cantidad, int) or cantidad < 0:
                return jsonify({"error": "La cantidad debe ser un número entero no negativo"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Cantidad inválida"}), 400
        return func(*args, **kwargs)

    return wrapper


def consultar_producto(id_producto: int) -> Tuple[Dict[str, Union[str, int]], int]:
    """
    Consulta un producto por su ID

    Args:
        id_producto: ID del producto a consultar

    Returns:
        Tuple con el diccionario del producto y el código HTTP
    """
    try:
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto = c.fetchone()
        conn.close()

        if producto:
            return {"id": producto[0], "nombre": producto[1], "cantidad": producto[2]}, 200
        return {"error": "Producto no encontrado"}, 404

    except Exception as e:
        return {"error": f"Error en la base de datos: {str(e)}"}, 500


def agregar_producto(id_producto: int, nombre: str, cantidad: int) -> Tuple[Dict[str, str], int]:
    """
    Agrega un nuevo producto al inventario

    Args:
        id_producto: ID del nuevo producto
        nombre: Nombre del producto
        cantidad: Cantidad inicial del producto

    Returns:
        Tuple con el mensaje de respuesta y el código HTTP
    """
    try:
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('INSERT INTO productos (id, nombre, cantidad) VALUES (?, ?, ?)',
                  (id_producto, nombre, cantidad))
        conn.commit()
        conn.close()
        return {"mensaje": "Producto agregado exitosamente"}, 201
    except sqlite3.IntegrityError:
        return {"error": "El producto ya existe"}, 409
    except Exception as e:
        return {"error": f"Error en la base de datos: {str(e)}"}, 500


def actualizar_stock(id_producto: int, nueva_cantidad: int) -> Tuple[Dict[str, str], int]:
    """
    Actualiza el stock de un producto

    Args:
        id_producto: ID del producto a actualizar
        nueva_cantidad: Nueva cantidad del producto

    Returns:
        Tuple con el mensaje de respuesta y el código HTTP
    """
    assert isinstance(id_producto, int) and id_producto > 0, "ID de producto debe ser un entero positivo"
    assert isinstance(nueva_cantidad, int) and nueva_cantidad >= 0, "Nueva cantidad debe ser un entero no negativo"

    try:
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('UPDATE productos SET cantidad = ? WHERE id = ?',
                  (nueva_cantidad, id_producto))
        if c.rowcount == 0:
            conn.close()
            return {"error": "Producto no encontrado"}, 404
        conn.commit()
        conn.close()
        return {"mensaje": "Stock actualizado exitosamente"}, 200
    except Exception as e:
        return {"error": f"Error en la base de datos: {str(e)}"}, 500


# Rutas de la API
@app.route('/producto/<int:id_producto>', methods=['GET'])
@validar_id
def get_producto(id_producto):
    """Endpoint para consultar un producto"""
    return consultar_producto(id_producto)


@app.route('/producto', methods=['POST'])
def post_producto():
    """Endpoint para agregar un nuevo producto"""
    data = request.get_json()

    if not all(k in data for k in ('id', 'nombre', 'cantidad')):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        id_producto = int(data['id'])
        cantidad = int(data['cantidad'])

        if id_producto <= 0:
            return jsonify({"error": "ID debe ser un número positivo"}), 400
        if cantidad < 0:
            return jsonify({"error": "Cantidad debe ser un número no negativo"}), 400

        return agregar_producto(id_producto, data['nombre'], cantidad)
    except ValueError:
        return jsonify({"error": "ID y cantidad deben ser números"}), 400


@app.route('/producto/<int:id_producto>', methods=['PUT'])
@validar_id
def put_producto(id_producto):
    """Endpoint para actualizar el stock de un producto"""
    data = request.get_json()

    if 'cantidad' not in data:
        return jsonify({"error": "Falta el campo cantidad"}), 400

    try:
        nueva_cantidad = int(data['cantidad'])
        return actualizar_stock(id_producto, nueva_cantidad)
    except ValueError:
        return jsonify({"error": "Cantidad debe ser un número"}), 400
    except AssertionError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    init_db()
    app.run(debug=True)