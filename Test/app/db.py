import json
import os
from typing import Dict, Any, Tuple


class DatabaseHandler:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.ensure_json_file()

    def ensure_json_file(self):
        """Crea el archivo JSON si no existe"""
        if not os.path.exists(self.json_file):
            initial_data = {
                "productos": {
                    "1": {"nombre": "Laptop", "stock": 10},
                    "2": {"nombre": "Monitor", "stock": 15},
                    "3": {"nombre": "Teclado", "stock": 20}
                },
                "siguiente_id": 4
            }
            self.save_data(initial_data)

    def load_data(self) -> Dict[str, Any]:
        """Carga los datos del archivo JSON"""
        with open(self.json_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_data(self, data: Dict[str, Any]):
        """Guarda los datos en el archivo JSON"""
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_producto(self, id_producto: int) -> Tuple[Dict[str, Any], str]:
        """Obtiene un producto por su ID"""
        data = self.load_data()
        str_id = str(id_producto)
        if str_id in data["productos"]:
            return data["productos"][str_id], ""
        return {}, "Producto no encontrado"

    def agregar_producto(self, nombre: str, stock: int) -> Tuple[Dict[str, Any], str]:
        """Agrega un nuevo producto"""
        data = self.load_data()
        nuevo_id = str(data["siguiente_id"])

        data["productos"][nuevo_id] = {
            "nombre": nombre,
            "stock": stock
        }
        data["siguiente_id"] += 1

        self.save_data(data)
        return {"id": nuevo_id, "nombre": nombre, "stock": stock}, ""

    def actualizar_stock(self, id_producto: int, nuevo_stock: int) -> Tuple[Dict[str, Any], str]:
        """Actualiza el stock de un producto"""
        data = self.load_data()
        str_id = str(id_producto)

        if str_id not in data["productos"]:
            return {}, "Producto no encontrado"

        data["productos"][str_id]["stock"] = nuevo_stock
        self.save_data(data)

        return data["productos"][str_id], ""