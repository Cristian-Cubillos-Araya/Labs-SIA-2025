from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_del_laboratorio'

# Función para cargar los datos del inventario
def cargar_inventario():
    if os.path.exists('inventario.json'):
        with open('inventario.json', 'r') as archivo:
            return json.load(archivo)
    return []

# Función para guardar los datos del inventario
def guardar_inventario(inventario):
    with open('inventario.json', 'w') as archivo:
        json.dump(inventario, archivo, indent=4)

@app.route('/')
def index():
    inventario = cargar_inventario()
    return render_template('index.html', inventario=inventario)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = {
            'id': len(cargar_inventario()) + 1,
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio'])
        }
        
        inventario = cargar_inventario()
        inventario.append(producto)
        guardar_inventario(inventario)
        
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    inventario = cargar_inventario()
    producto = next((p for p in inventario if p['id'] == id), None)
    
    if producto is None:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['descripcion'] = request.form['descripcion']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        
        guardar_inventario(inventario)
        
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    inventario = cargar_inventario()
    inventario = [p for p in inventario if p['id'] != id]
    
    # Reordenar los IDs
    for i, producto in enumerate(inventario):
        producto['id'] = i + 1
    
    guardar_inventario(inventario)
    
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Crear el archivo de inventario si no existe
    if not os.path.exists('inventario.json'):
        guardar_inventario([])
    
    app.run(debug=True)