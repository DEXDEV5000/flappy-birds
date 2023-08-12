import tkinter as tk 
import subprocess 
from PIL import Image, ImageTk
def iniciar_juego():
    try:
        subprocess.run(["python", "main.py"])  
    except FileNotFoundError:
        print("El archivo 'main.py' no se encontró.")
def abrir_configuracion():
    try:
        subprocess.run(["python", "configuracion.py"])  
    except FileNotFoundError:
        print("El archivo 'configuracion.py' no se encontró.")
def cerrar_y_abrir_1():
    ventana.destroy()
    iniciar_juego()
def cerrar_y_abrir_2():
    ventana.destroy()
    abrir_configuracion()
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Metal Men")
ventana.geometry("1080x1080")
# Cargar la imagen y redimensionarla
imagen_fondo = Image.open("imagenes/bg.png")
ancho, alto = ventana.winfo_screenwidth(), ventana.winfo_screenheight()  # Tamaño de la pantalla
imagen_redimensionada = imagen_fondo.resize((ancho, alto))
imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)

fondo_label = tk.Label(ventana, image=imagen_fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
# Etiqueta de título
titulo = tk.Label(ventana, text="Menú Principal", font=("Helvetica", 16))
titulo.pack(pady=20)

# Botones de Iniciar y Configuración
boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=cerrar_y_abrir_1)
boton_iniciar.pack(pady=20)

boton_configuracion = tk.Button(ventana, text="Configuración", command=cerrar_y_abrir_2)
boton_configuracion.pack(pady=20)


# Ejecutar el bucle de la interfaz gráfica
ventana.mainloop()
