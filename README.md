# 🏍️ Ketoz Chain - Ecosistema Tecnológico End-to-End

Solución de software modular diseñada para la captura transaccional, persistencia relacional y analítica gerencial de la cadena de distribución de repuestos para motocicletas (B2B y e-commerce) de Ketoz Chain de Colombia. El sistema automatiza el ciclo de vida completo del dato.

## 🏗️ Arquitectura General del Sistema

El ecosistema opera bajo un diseño integrado estructurado en tres capas funcionales autónomas:

1. **Capa Backend (`Backend/database.py`):** Motor relacional desarrollado sobre SQLite3 bajo un **Esquema Estrella**. Está compuesto por una tabla de hechos central (`fact_envios`) y dos dimensiones (`dim_clientes` y `dim_repuestos`). Implementa *Data Seeding* automatizado inyectando 5 registros base al inicializar el sistema.
2. **Capa Frontend (`Frontend/app_envios.py`):** Interfaz gráfica construida en `Tkinter` que integra la identidad visual de la marca. Cuenta con controles CRUD 100% funcionales que interactúan en vivo con la base de datos, protegidos por manejo de excepciones (`try-except`) y ventanas de alerta para mitigar fallos de digitación humana.
3. **Capa Business Intelligence (`Ketoz_Dashboard.pbix`):** Panel analítico desarrollado en Power BI Desktop. Para garantizar una conexión irrompible y evitar fallos de rutas dinámicas en Windows, el Modelo Estrella se alimenta a través de un **Script nativo de Python (`pandas`, `sqlite3`)**. Incluye DAX avanzado, segmentación de tiempo (Calendario) y UI/UX corporativa (Rojo, Negro y Blanco).

## 👥 Equipo de Ingeniería
* **Matías Mondragón** (Líder de Arquitectura Backend y Orquestación)
* **Arianne** (Diseño de Interfaz Frontend & UX/UI)
* **Mariana Peña** (Ingeniería de Business Intelligence & Modelado DAX)

## 🚀 Instrucciones de Despliegue y Ejecución

### 1. Despliegue Transaccional
Asegúrese de contar con las librerías `Pillow` y `pandas` instaladas.
```bash
python main.py
