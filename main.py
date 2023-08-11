from tkinter import *
Ventana=Tk()
Ventana.title("Metal Men")
Ventana.geometry("650x650")

imagen_de_fondo=PhotoImage(file="imagenes\Kevin.png")
background_label = Label(image=imagen_de_fondo)
background_label.pack()  
label3 = Label(Ventana,text="¡Hola Mundo!",bg="yellow")
label3.config(height=1,width=18)
label3.pack()
Ventana.mainloop()
