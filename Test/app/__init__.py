from flask import Flask
from app.db import DatabaseHandler
import os

app = Flask(__name__)

# Configurar la ruta del archivo JSON
json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'productos.json')
db = DatabaseHandler(json_file)

# Importar las rutas después de crear la app
from app import api