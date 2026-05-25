import tkinter as tk
from tkinter import ttk, messagebox
import os


from PIL import Image, ImageTk
import os
import sqlite3

class AppKetoz:
    def __init__(self, root):
        self.root = root
        self.root.title("Ketoz Chain - Panel de Control Logístico")
        self.root.geometry("450x600")
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(False, False)
        
        # LOGO
        try:
            ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            img = Image.open(ruta_logo).convert("RGB").resize((130, 130), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.logo_img, bg="#f4f4f4").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="🏍️ KETOZ LOGÍSTICA", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)
        
        tk.Label(self.root, text="Gestión de Envíos B2B", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=5)
        
        # BOTONES CRUD FUNCIONALES
        frame_crud = tk.Frame(self.root, bg="#f4f4f4")
        frame_crud.pack(pady=10)
        
        tk.Button(frame_crud, text="➕ Crear Registro de Flete", bg="#2a9d8f", fg="white", width=25, font=("Arial", 11, "bold"), command=self.crear).pack(pady=5)
        tk.Button(frame_crud, text="📖 Leer / Consultar Envíos", bg="#e9c46a", fg="black", width=25, font=("Arial", 11, "bold"), command=self.leer).pack(pady=5)
        tk.Button(frame_crud, text="✏️ Actualizar Estado", bg="#f4a261", fg="white", width=25, font=("Arial", 11, "bold"), command=self.actualizar).pack(pady=5)
        tk.Button(frame_crud, text="🗑️ Eliminar Registro", bg="#e76f51", fg="white", width=25, font=("Arial", 11, "bold"), command=self.eliminar).pack(pady=5)
        
        # PUENTE A POWER BI
        tk.Label(self.root, text="Inteligencia de Negocios (Dashboard)", font=("Arial", 10, "italic"), bg="#f4f4f4").pack(pady=15)
        tk.Button(self.root, text="📊 ABRIR POWER BI", bg="#1d3557", fg="white", font=("Arial", 12, "bold"), width=25, cursor="hand2", command=self.abrir_pbi).pack(pady=5)

    def crear(self):
        # 1. Crear una ventana secundaria (Pop-up real de captura)
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Nuevo Envío B2B")
        ventana_nuevo.geometry("350x450")
        ventana_nuevo.configure(bg="#f4f4f4")
        ventana_nuevo.grab_set() # Bloquea la ventana principal hasta que se cierre esta
        ventana_nuevo.resizable(False, False)

        tk.Label(ventana_nuevo, text="Registrar Flete a Cliente", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=15)

        # 2. Campos de Formulario
        tk.Label(ventana_nuevo, text="ID Cliente (Ej: 1, 2, 3...):", bg="#f4f4f4").pack()
        entry_cliente = tk.Entry(ventana_nuevo, justify="center", font=("Arial", 11))
        entry_cliente.pack(pady=5)

        tk.Label(ventana_nuevo, text="ID Repuesto (Ej: 101, 102...):", bg="#f4f4f4").pack()
        entry_repuesto = tk.Entry(ventana_nuevo, justify="center", font=("Arial", 11))
        entry_repuesto.pack(pady=5)

        tk.Label(ventana_nuevo, text="Peso del paquete (Kg):", bg="#f4f4f4").pack()
        entry_peso = tk.Entry(ventana_nuevo, justify="center", font=("Arial", 11))
        entry_peso.pack(pady=5)

        tk.Label(ventana_nuevo, text="Costo del Flete ($):", bg="#f4f4f4").pack()
        entry_costo = tk.Entry(ventana_nuevo, justify="center", font=("Arial", 11))
        entry_costo.pack(pady=5)

        tk.Label(ventana_nuevo, text="Fecha (YYYY-MM-DD):", bg="#f4f4f4").pack()
        entry_fecha = tk.Entry(ventana_nuevo, justify="center", font=("Arial", 11))
        entry_fecha.pack(pady=5)

        # 3. Lógica de guardado en Base de Datos
        def guardar_db():
            try:
                # Validar y convertir los textos ingresados a números
                cli = int(entry_cliente.get())
                rep = int(entry_repuesto.get())
                peso = float(entry_peso.get())
                costo = float(entry_costo.get())
                fecha = entry_fecha.get()

                if not fecha:
                    raise ValueError("La fecha no puede estar vacía.")

                # Conectar a la base de datos Ketoz Logística
                ruta_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "ketoz_logistica.db")
                with sqlite3.connect(ruta_db) as conn:
                    cursor = conn.cursor()
                    # Inserción en la Tabla de Hechos
                    cursor.execute("INSERT INTO fact_envios (id_cliente, id_repuesto, peso_kg, costo_flete, fecha) VALUES (?, ?, ?, ?, ?)",
                                   (cli, rep, peso, costo, fecha))
                    conn.commit()

                messagebox.showinfo("Éxito", "Flete registrado y guardado en la base de datos operativa.", parent=ventana_nuevo)
                ventana_nuevo.destroy() # Cierra el formulario tras guardar exitosamente

            except ValueError as ve:
                messagebox.showwarning("Error de Formato", f"Verifique que los datos sean numéricos.\nDetalle: {ve}", parent=ventana_nuevo)
            except Exception as e:
                messagebox.showerror("Error Crítico", f"Fallo en el puente de datos:\n{e}", parent=ventana_nuevo)

        # Botón de ejecución
        tk.Button(ventana_nuevo, text="💾 Guardar en SQLite", bg="#2e7d32", fg="white", font=("Arial", 11, "bold"), cursor="hand2", command=guardar_db).pack(pady=20)

    def leer(self):
        # 1. Crear ventana secundaria para la tabla
        ventana_leer = tk.Toplevel(self.root)
        ventana_leer.title("Historial de Envíos B2B")
        ventana_leer.geometry("750x350")
        ventana_leer.configure(bg="#f4f4f4")
        ventana_leer.grab_set()

        tk.Label(ventana_leer, text="📋 Base de Datos: Fletes Registrados", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=10)

        # 2. Crear la tabla visual (Treeview)
        columnas = ("ID", "Cliente", "Repuesto", "Peso (Kg)", "Costo ($)", "Fecha")
        tabla = ttk.Treeview(ventana_leer, columns=columnas, show="headings", height=10)
        
        # Configurar anchos de columna
        tabla.column("ID", width=50, anchor="center")
        tabla.column("Cliente", width=180, anchor="w")
        tabla.column("Repuesto", width=180, anchor="w")
        tabla.column("Peso (Kg)", width=80, anchor="center")
        tabla.column("Costo ($)", width=100, anchor="center")
        tabla.column("Fecha", width=100, anchor="center")

        for col in columnas:
            tabla.heading(col, text=col)
        
        tabla.pack(pady=10, padx=10, fill="x")

        # 3. Lógica para extraer datos de SQLite (Uniendo las 3 tablas del Esquema Estrella)
        try:
            ruta_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "ketoz_logistica.db")
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT fact_envios.id_envio, dim_clientes.empresa, dim_repuestos.articulo, 
                           fact_envios.peso_kg, fact_envios.costo_flete, fact_envios.fecha 
                    FROM fact_envios
                    JOIN dim_clientes ON fact_envios.id_cliente = dim_clientes.id_cliente
                    JOIN dim_repuestos ON fact_envios.id_repuesto = dim_repuestos.id_repuesto
                ''')
                registros = cursor.fetchall()
                
                # Insertar los datos en la tabla visual
                for fila in registros:
                    tabla.insert("", tk.END, values=fila)

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo cargar el historial.\nDetalle: {e}", parent=ventana_leer)


    def actualizar(self):
        ventana_act = tk.Toplevel(self.root)
        ventana_act.title("Actualizar Flete")
        ventana_act.geometry("300x250")
        ventana_act.configure(bg="#f4f4f4")
        ventana_act.grab_set()

        tk.Label(ventana_act, text="Actualizar Costo de Envío", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=15)

        tk.Label(ventana_act, text="ID del Envío a modificar:", bg="#f4f4f4").pack()
        entry_id = tk.Entry(ventana_act, justify="center")
        entry_id.pack(pady=5)

        tk.Label(ventana_act, text="Nuevo Costo del Flete ($):", bg="#f4f4f4").pack()
        entry_costo = tk.Entry(ventana_act, justify="center")
        entry_costo.pack(pady=5)

        def ejecutar_actualizacion():
            try:
                id_envio = int(entry_id.get())
                nuevo_costo = float(entry_costo.get())

                ruta_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "ketoz_logistica.db")
                with sqlite3.connect(ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE fact_envios SET costo_flete = ? WHERE id_envio = ?", (nuevo_costo, id_envio))
                    
                    if cursor.rowcount == 0:
                        raise ValueError("No se encontró ningún envío con ese ID.")
                    
                    conn.commit()

                messagebox.showinfo("Éxito", f"El envío #{id_envio} ha sido actualizado a ${nuevo_costo}.", parent=ventana_act)
                ventana_act.destroy()

            except ValueError as ve:
                messagebox.showwarning("Dato Inválido", str(ve), parent=ventana_act)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=ventana_act)

        tk.Button(ventana_act, text="💾 Guardar Cambios", bg="#f4a261", fg="white", font=("Arial", 10, "bold"), command=ejecutar_actualizacion).pack(pady=15)


    def eliminar(self):
        ventana_elim = tk.Toplevel(self.root)
        ventana_elim.title("Eliminar Registro")
        ventana_elim.geometry("300x200")
        ventana_elim.configure(bg="#f4f4f4")
        ventana_elim.grab_set()

        tk.Label(ventana_elim, text="Borrar Registro Logístico", font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#d32f2f").pack(pady=15)

        tk.Label(ventana_elim, text="ID del Envío a ELIMINAR:", bg="#f4f4f4").pack()
        entry_id = tk.Entry(ventana_elim, justify="center")
        entry_id.pack(pady=5)

        def ejecutar_eliminacion():
            try:
                id_envio = int(entry_id.get())
                
                respuesta = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar el envío #{id_envio}?\nEsta acción es irreversible.", parent=ventana_elim)
                
                if respuesta:
                    ruta_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "ketoz_logistica.db")
                    with sqlite3.connect(ruta_db) as conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM fact_envios WHERE id_envio = ?", (id_envio,))
                        
                        if cursor.rowcount == 0:
                            raise ValueError("No existe un envío con ese ID para borrar.")
                        
                        conn.commit()
                        
                    messagebox.showinfo("Borrado", f"El envío #{id_envio} ha sido eliminado del sistema.", parent=ventana_elim)
                    ventana_elim.destroy()

            except ValueError as ve:
                messagebox.showwarning("Error", str(ve), parent=ventana_elim)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=ventana_elim)

        tk.Button(ventana_elim, text="🗑️ Eliminar Definitivamente", bg="#e76f51", fg="white", font=("Arial", 10, "bold"), command=ejecutar_eliminacion).pack(pady=15)

    def abrir_pbi(self):
        try:
            ruta_pbix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Ketoz_Dashboard.pbix")
            os.startfile(ruta_pbix)
        except Exception as e:
            messagebox.showerror("Archivo no encontrado", f"Asegúrate de que 'Ketoz_Dashboard.pbix' esté en la carpeta raíz.\nError: {e}")