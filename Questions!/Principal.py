import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import Client
from PIL import ImageTk, Image
"""
Importamos las librerias y clases requeridas para el funcionamiento de instancias y funciones
creamos un puntaje
iniciamos la conexion cliente servidos
creamos una lista que sera asignada mediante una solicitud al servidor
"""
puntaje = 0
client_socket = Client.iniciar()
pregunta_respuestas_puntajes = Client.solicitud(client_socket, "En espera").split('\n')

"""
Cargamos los componentes para la vista 
y asignamos los textos requeridos a estos componentes
"""
def cargar(pregunta_respuestas_puntajes, texto_pregunta, texto_puntaje, btn1, btn2, btn3, btn4, punto, validar):
    
    #Nos permite incrementar el puntaje
    global puntaje
    if punto == 0:
        puntaje = 0
    else:
        puntaje += punto

    """
    Modificamos los componentes para una mejor visibilidad y uso de la interfaz
    Asignamos los textos a estos componentes
    """
    texto_pregunta.config(state="normal")
    texto_pregunta.delete(1.0, END)
    texto_pregunta.tag_configure("centered", justify="center")
    text = validar +  "\n \n" + pregunta_respuestas_puntajes[0]
    texto_pregunta.insert("1.0", text, "centered")
    texto_pregunta.config(state="disabled")

    texto_puntaje_actual.config(state="normal")
    texto_puntaje_actual.delete(1.0, END)
    texto_puntaje_actual.tag_configure("centered", justify="center")
    text2 =  "Tu puntaje: "+str(puntaje)
    texto_puntaje_actual.insert("1.0", text2, "centered")
    texto_puntaje_actual.config(state="disabled")

    texto_puntaje.config(state="normal")
    text = "\t             Puntajes \n \n"
    for i in range(1, 51):
        text = text + str(i) + ". " + pregunta_respuestas_puntajes[i+5+(i-1)] + "\t" + pregunta_respuestas_puntajes[i+6+(i-1)] + "\n"
    texto_puntaje.insert('1.0', text)
    texto_puntaje.config(state="disabled")
    texto_puntaje.config(yscrollcommand=None)

    # Agregamos el texto a los botones
    btn1.config(text="A:  "+pregunta_respuestas_puntajes[1])
    btn2.config(text="B:  "+pregunta_respuestas_puntajes[2])
    btn3.config(text="C:  "+pregunta_respuestas_puntajes[3])
    btn4.config(text="D:  "+pregunta_respuestas_puntajes[4])

    


"""
Creamos la ventana raiz y un cuadro de dialogo para el ingreso del nombre
le asignamos titulo a la ventana y el tamaño, le desabilidamos las modificaciones y centramos la ventana
"""
root = tk.Tk()
root.withdraw()
name = simpledialog.askstring("N", "Ingresa tu nombre",initialvalue="Nombre",)
root.deiconify()
root.title("Questions!")
root.geometry("1200x500")
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1200
window_height = 500
x_coord = (screen_width / 2) - (window_width / 2)
y_coord = (screen_height / 2) - (window_height / 2)
root.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_coord), int(y_coord)))

"""
Creamos un componente para los botones
"""
frame = tk.Frame(root, width=1200, height=500)
frame.pack()
frame.place(x=0, y=0)


"""
Creamos una instancia de una imagen para usarla como fondo de la aplicacion
"""
image = Image.open("assets/fondo.jpg")
photo = ImageTk.PhotoImage(image)
label = tk.Label(frame, image=photo)
label.image = photo
label.pack()


"""
Creamos los cuadros de textos para las preguntas, los puntajes y el puntaje del cliente
personalizamos la letra y el tamaño de los cuadros de texto
"""
texto_pregunta = tk.Text(frame, font=("Times New Roman", 16), width=69, height=9, bg='white')
texto_pregunta.pack()
texto_pregunta.place(x=14, y=13)

texto_puntaje = tk.Text(frame, font=("Times New Roman", 16), width=30, height=15, bg='white')
texto_puntaje.pack()
texto_puntaje.place(x=814, y=13)

texto_puntaje_actual = tk.Text(frame, font=("Times New Roman", 16), width=30, height=2, bg='white')
texto_puntaje_actual.pack()
texto_puntaje_actual.place(x=814, y=390)


"""
Este metodo nos permite validar la respuesta correcta 
si es correcta enviar otra pregunta, incrementar el puntaje y seguir con la ejecucion
de lo contrario bloquear la interfaz para asi guardar el puntaje obtenido
"""
def opciones(x):
    global pregunta_respuestas_puntajes
    respuesta=pregunta_respuestas_puntajes[5]
    if pregunta_respuestas_puntajes[5] == pregunta_respuestas_puntajes[x]:
        pregunta_respuestas_puntajes = Client.solicitud(client_socket, "En espera").split('\n')
        cargar(pregunta_respuestas_puntajes, texto_pregunta, texto_puntaje, btn1, btn2, btn3, btn4, 1, "¡CORRECTO!")
    else:
        Client.solicitud(client_socket, name + "\n"+str(puntaje)).split('\n')
        cargar(pregunta_respuestas_puntajes, texto_pregunta, texto_puntaje, btn1, btn2, btn3, btn4, 0, "Perdiste era: " + respuesta)
        btn5.configure(state="normal")
        btn1.configure(state="disabled")
        btn2.configure(state="disabled")
        btn3.configure(state="disabled")
        btn4.configure(state="disabled")

"""
Definir el metodo para los botones
"""
def btn1_click():
    opciones(1)

def btn2_click():
    opciones(2)

def btn3_click():
    opciones(3)

def btn4_click():
    opciones(4)

def btn5_click():
    root.destroy() #Con este metodo cerramos la interfaz 


"""
Personalizar los botones
"""
btn_config = {'font': ('Times New Roman', 16), 'width': 30, 'height': 2, 'fg': 'white', 'bg': 'black'}

btn1 = tk.Button(frame, command=btn1_click, **btn_config)
btn1.pack()
btn1.place(x=13, y=260)

btn2 = tk.Button(frame, command=btn2_click,**btn_config)
btn2.pack()
btn2.place(x=13, y=345)

btn3 = tk.Button(frame, command=btn3_click, **btn_config)
btn3.pack()
btn3.place(x=405, y=260)

btn4 = tk.Button(frame, command=btn4_click,**btn_config)
btn4.pack()
btn4.place(x=405, y=345)

btn5 = tk.Button(frame, font=("Times New Roman", 16), command=btn5_click,bg='red',fg='white')
btn5.pack()
btn5.place(x=270, y=430)
btn5.config(text="Salir")
btn5.config(width= 20, height= 1)
btn5.configure(state="disabled")

"""
Cargamos la pregunta inicial y abrimos la ventana root para inicar con el programa
"""
cargar(pregunta_respuestas_puntajes, texto_pregunta, texto_puntaje, btn1, btn2, btn3, btn4, 0, " ")

root.mainloop()
