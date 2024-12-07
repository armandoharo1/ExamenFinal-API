from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'alumnos.db'

# Función para conectar a la base de datos
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Método GET - Lista de estudiantes
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alumnos")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Método GET <id> - Estudiante por ID
@app.route('/estudiantes/<int:id>', methods=['GET'])
def get_estudiante(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alumnos WHERE id = ?", (id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({"error": "Estudiante no encontrado"}), 404

# Método POST - Crear estudiante
@app.route('/estudiantes', methods=['POST'])
def create_estudiante():
    data = request.get_json()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES (?, ?, ?, ?, ?)",
        (data['nombre'], data['apellido'], data['aprobado'], data['nota'], data['fecha'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Estudiante creado con éxito"}), 201

# Método PUT <id> - Actualizar estudiante
@app.route('/estudiantes/<int:id>', methods=['PUT'])
def update_estudiante(id):
    data = request.get_json()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alumnos SET nombre = ?, apellido = ?, aprobado = ?, nota = ?, fecha = ? WHERE id = ?",
        (data['nombre'], data['apellido'], data['aprobado'], data['nota'], data['fecha'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Estudiante actualizado con éxito"})

# Método DELETE <id> - Eliminar estudiante
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def delete_estudiante(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM alumnos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Estudiante eliminado con éxito"})

if __name__ == '__main__':
    app.run(debug=True)
