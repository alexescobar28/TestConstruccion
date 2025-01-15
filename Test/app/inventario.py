from typing import Tuple, Union

# Simulación de una base de datos de productos
db_productos = {
    1: {"nombre": "Laptop", "stock": 10},
    2: {"nombre": "Monitor", "stock": 15},
    3: {"nombre": "Teclado", "stock": 20}
}


def consultar_producto(id_producto: int) -> Union[Tuple[str, int], str]:
    """
    Consulta un producto por su ID y devuelve su nombre y cantidad en stock.

    Args:
        id_producto: ID del producto a consultar

    Returns:
        Tupla con el nombre y stock del producto si es exitoso,
        o un mensaje de error si falla la validación
    """
    # Validar que el ID sea un número entero
    if not isinstance(id_producto, int):
        return "Error: El ID del producto debe ser un número entero"

    # Validar que el ID sea positivo
    if id_producto <= 0:
        return "Error: El ID del producto debe ser un número positivo"

    # Verificar si el producto existe en la base de datos
    if id_producto not in db_productos:
        return f"Error: No existe un producto con el ID {id_producto}"

    producto = db_productos[id_producto]
    return producto["nombre"], producto["stock"]


def agregar_producto(id_producto: int, cantidad: int) -> str:
    """
    Agrega una cantidad específica al stock de un producto.

    Args:
        id_producto: ID del producto a actualizar
        cantidad: Cantidad a agregar al stock

    Returns:
        Mensaje indicando el resultado de la operación
    """
    # Validar que el ID sea un número entero
    if not isinstance(id_producto, int):
        return "Error: El ID del producto debe ser un número entero"

    # Validar que el ID sea positivo
    if id_producto <= 0:
        return "Error: El ID del producto debe ser un número positivo"

    # Validar que la cantidad sea un número entero
    if not isinstance(cantidad, int):
        return "Error: La cantidad debe ser un número entero"

    # Validar que la cantidad sea positiva
    if cantidad <= 0:
        return "Error: La cantidad debe ser un número positivo"

    # Verificar si el producto existe
    if id_producto not in db_productos:
        return f"Error: No existe un producto con el ID {id_producto}"

    # Actualizar el stock
    db_productos[id_producto]["stock"] += cantidad
    return f"Stock actualizado correctamente. Nuevo stock: {db_productos[id_producto]['stock']}"


def actualizar_stock(id_producto: int, nueva_cantidad: int) -> str:
    """
    Actualiza el stock de un producto a una nueva cantidad específica.

    Args:
        id_producto: ID del producto a actualizar (debe ser entero positivo)
        nueva_cantidad: Nueva cantidad de stock (debe ser entero no negativo)

    Returns:
        Mensaje indicando el resultado de la operación

    Raises:
        AssertionError: Si no se cumplen las condiciones del contrato
    """
    try:
        # Verificar que id_producto sea un entero
        assert isinstance(id_producto, int), "El ID del producto debe ser un número entero"

        # Verificar que id_producto sea positivo
        assert id_producto > 0, "El ID del producto debe ser un número positivo"

        # Verificar que nueva_cantidad sea un entero
        assert isinstance(nueva_cantidad, int), "La nueva cantidad debe ser un número entero"

        # Verificar que nueva_cantidad no sea negativa
        assert nueva_cantidad >= 0, "La nueva cantidad no puede ser negativa"

        # Verificar que el producto exista
        assert id_producto in db_productos, f"No existe un producto con el ID {id_producto}"

        # Actualizar el stock
        db_productos[id_producto]["stock"] = nueva_cantidad
        return f"Stock actualizado correctamente. Nuevo stock: {nueva_cantidad}"

    except AssertionError as e:
        return f"Error de validación: {str(e)}"