import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ketoz_logistica.db")

class KetozDB:
    @staticmethod
    def inicializar():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # 1. ESQUEMA ESTRELLA (1 Hecho, 2 Dimensiones)
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_clientes (
                                id_cliente INTEGER PRIMARY KEY,
                                empresa TEXT, ciudad TEXT)''')
                                
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_repuestos (
                                id_repuesto INTEGER PRIMARY KEY,
                                articulo TEXT, categoria TEXT)''')
                                
            cursor.execute('''CREATE TABLE IF NOT EXISTS fact_envios (
                                id_envio INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_cliente INTEGER,
                                id_repuesto INTEGER,
                                peso_kg REAL,
                                costo_flete REAL,
                                fecha TEXT,
                                FOREIGN KEY(id_cliente) REFERENCES dim_clientes(id_cliente),
                                FOREIGN KEY(id_repuesto) REFERENCES dim_repuestos(id_repuesto))''')
            
            # 2. SEEDING (Autogeneración de mínimo 5 registros)
            cursor.execute("SELECT COUNT(*) FROM dim_repuestos")
            if cursor.fetchone()[0] == 0:
                print("🌱 Inicializando datos base de Ketoz Chain...")
                
                clientes = [(1, "Distribuidora B2B Sur", "Cali"), (2, "Taller Motos Pro", "Medellín"), 
                            (3, "Central Repuestos", "Bogotá"), (4, "Motos del Caribe", "Barranquilla"), 
                            (5, "Servicio Técnico XYZ", "Bucaramanga")]
                cursor.executemany("INSERT INTO dim_clientes VALUES (?, ?, ?)", clientes)
                
                repuestos = [(101, "Disco de Freno Delantero", "Frenos"), (102, "Pastillas de Freno", "Frenos"),
                             (103, "Cadena Reforzada 520", "Transmisión"), (104, "Kit de Arrastre", "Transmisión"),
                             (105, "Batería 12V", "Eléctrico")]
                cursor.executemany("INSERT INTO dim_repuestos VALUES (?, ?, ?)", repuestos)
                
                envios = [(1, 101, 15.5, 45000, "2026-05-01"), (2, 103, 8.2, 25000, "2026-05-03"),
                          (3, 104, 25.0, 75000, "2026-05-10"), (4, 102, 2.5, 12000, "2026-05-15"),
                          (5, 105, 10.0, 30000, "2026-05-20")]
                cursor.executemany("INSERT INTO fact_envios (id_cliente, id_repuesto, peso_kg, costo_flete, fecha) VALUES (?, ?, ?, ?, ?)", envios)
                
            conn.commit()