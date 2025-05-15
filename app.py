from flask import Flask, request, render_template, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = 'clave-secreta-compartida'  # Debe coincidir con la del servicio de auth

# Simulación de base de datos de productos
PRODUCTOS = [
    {'id': 1, 'nombre': 'Lápiz', 'precio': 1.5},
    {'id': 2, 'nombre': 'Cuaderno', 'precio': 3.0},
    {'id': 3, 'nombre': 'Mochila', 'precio': 20.0}
]

# Interfaz web
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

# API protegida
@app.route('/api/productos')
def productos_api():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Falta token'}), 401
    try:
        jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=['HS256'])
        return jsonify(PRODUCTOS)
    except jwt.exceptions.InvalidTokenError:
        return jsonify({'error': 'Token inválido'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
