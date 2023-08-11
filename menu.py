import tkinter as tk 
import subprocess 
def iniciar_juego():
    try:
        subprocess.run(["python", "main.py"])  
    except FileNotFoundError:
        print("El archivo 'main.py' no se encontró.")

def abrir_configuracion():
    # Agrega aquí la lógica para la configuración del juego
    print("Configuración abierta")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Metal Men")
ventana.geometry("1080x1080")
# Etiqueta de título
titulo = tk.Label(ventana, text="Menú Principal", font=("Helvetica", 16))
titulo.pack(pady=20)

# Botones de Iniciar y Configuración
boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.pack(pady=20)

boton_configuracion = tk.Button(ventana, text="Configuración", command=abrir_configuracion)
boton_configuracion.pack(pady=20)

# Ejecutar el bucle de la interfaz gráfica
ventana.mainloop()
