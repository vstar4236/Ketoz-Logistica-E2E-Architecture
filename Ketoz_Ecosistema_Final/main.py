import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from Backend.database import KetozDB
from Frontend.app_envios import AppKetoz

if __name__ == '__main__':
    # Inicializa el Esquema Estrella y siembra los datos
    KetozDB.inicializar()
    
    # Arranca la Interfaz Gráfica
    root = tk.Tk()
    app = AppKetoz(root)
    root.mainloop()