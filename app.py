from flask import Flask, render_template, url_for 
import sqlite3

app = Flask(__name__)

DB_PATH = "hotel.db"

def obtener_habitaciones():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, tipo, numero, precio, imagen_url FROM habitaciones")
    filas = cur.fetchall()
    conn.close()
    return filas

def obtener_reservas():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, r.nombre, r.dni, r.fecha, r.habitaciones,
               h.tipo AS tipo_hab, h.numero AS numero_hab, h.imagen_url AS imagen_hab
        FROM reserva r
        LEFT JOIN habitaciones h ON h.id = r.habitaciones
        ORDER BY r.fecha DESC
    """)
    filas = cur.fetchall()
    conn.close()
    return filas

@app.route("/")
def index():
    habitaciones = obtener_habitaciones()
    reservas = obtener_reservas()
    return render_template("index.html", habitaciones=habitaciones, reservas=reservas)

if __name__ == "__main__":
    app.run(debug=True)
