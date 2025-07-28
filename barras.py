import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import subprocess
import sys
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="proyectofinal_aplicada"
    )

def obtener_valor_actual():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT humedad_porcentaje FROM humedad_datos ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else 0
    except:
        return 0

# --- CONFIGURACIÓN DE LA FIGURA ---
fig, ax = plt.subplots(figsize=(4, 6))
fig.subplots_adjust(bottom=0.2)  # Deja espacio para el botón
fig.patch.set_facecolor('#d0f0d0')
ax.set_facecolor('#e0ffe0')

ax.set_xlim(-0.5, 0.5)
ax.set_ylim(0, 100)
ax.set_xticks([])
ax.set_ylabel('Humedad (%)', fontsize=12)
ax.set_title('Medidor de Humedad', fontsize=14)
ax.axhline(y=30, color='red', linestyle='--', linewidth=2, label='Límite Crítico (30%)')
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.7)

bar = ax.bar(0, 0, width=0.4, color='#1f77b4', edgecolor='black')[0]
etiqueta_valor = ax.text(0, 102, '', ha='center', fontsize=12, fontweight='bold')

def actualizar(frame):
    valor = obtener_valor_actual()
    bar.set_height(valor)
    bar.set_color('#ff7f0e' if valor > 30 else '#1f77b4')
    etiqueta_valor.set_text(f'{valor:.1f}%')
    return [bar, etiqueta_valor]

ani = FuncAnimation(fig, actualizar, interval=2000)

# --- BOTÓN CON ICONO PARA VOLVER AL MENÚ (POSICIÓN INFERIOR IZQUIERDA) ---
def volver_al_menu(event):
    plt.close(fig)
    try:
        subprocess.Popen([sys.executable, "ventana_principal.py"])
    except Exception:
        subprocess.Popen(["python", "ventana_principal.py"])

# Cargar la imagen del botón
try:
    img = mpimg.imread('assets/devolver.png')
except FileNotFoundError:
    # Fallback a botón de texto si la imagen no existe (también movido a la izquierda)
    boton_ax = fig.add_axes([0.05, 0.05, 0.2, 0.075])  # Posición izquierda
    boton = Button(boton_ax, "Volver", color='#c4e6b7', hovercolor='#a0cc92')
    boton.on_clicked(volver_al_menu)
else:
    # Crear un botón con la imagen en posición inferior izquierda
    imagebox = OffsetImage(img, zoom=0.15)
    ab = AnnotationBbox(imagebox, (0, 0), 
                       xybox=(0.08, 0.05),  # Coordenadas ajustadas a la izquierda
                       xycoords='figure fraction',
                       boxcoords="figure fraction",
                       box_alignment=(0, 0),  # Alineado a la esquina inferior izquierda
                       pad=0,
                       frameon=False)
    ax.add_artist(ab)
    
    # Conectar el evento de clic
    def on_click(event):
        if ab.contains(event)[0]:
            volver_al_menu(event)
    
    fig.canvas.mpl_connect('button_press_event', on_click)

plt.tight_layout()
plt.show()