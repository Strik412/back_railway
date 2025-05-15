from flask import Flask, request, render_template, jsonify
import jwt
import requests

app = Flask(__name__)
SECRET_KEY = 'clave-secreta-compartida'  # Debe ser la misma en todos los servicios

# URL del servicio de analítica (ajusta con tu dominio real de DigitalOcean)
ANALYTICS_URL = 'https://tu-digitalocean-app.com/api/evento'

# Simulación de base de datos de productos
PRODUCTOS = [
    {'id': 1, 'nombre': 'Lápiz', 'precio': 1.5},
    {'id': 2, 'nombre': 'Cuaderno', 'precio': 3.0},
    {'id': 3, 'nombre': 'Mochila', 'precio': 20.0}
]

# Función para enviar eventos al servicio de analítica
def enviar_evento(tipo, detalle, token):
    try:
        response = requests.post(ANALYTICS_URL, json={
            'tipo': tipo,
            'detalle': detalle
        }, headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
    except Exception as e:
        print("Error al enviar evento a analítica:", e)

# Interfaz web protegida por token (por URL)
@app.route('/productos')
def productos_web():
    token = request.args.get('token')
    if not token:
        return "Acceso denegado: falta token", 401
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return render_template('productos.html', productos=PRODUCTOS)
    except jwt.exceptions.InvalidTokenError:
        return "Token inválido", 401

# API protegida por token (en cabecera Authorization)
@app.route('/api/productos')
def productos_api():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Falta token'}), 401

    token = auth_header.replace("Bearer ", "")
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return jsonify({'error': 'Token inválido'}), 401

    # Enviar evento a analítica
    enviar_evento('consulta_productos', 'usuario consultó productos', token)

    return jsonify(PRODUCTOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
