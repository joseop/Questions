import socket
import threading
import Datos
"""" 
Importamos las librerias requeridas y las clases que vamos a utilizar en la clase servidor
la siguiente linea de codigo crea un objeto de socket en Python para el servidor, que luego 
  se utiliza para establecer una conexión de red utilizando el protocolo de comunicación de red TCP/IP

Se asigna el host y puerto al servidor en el que vamos a trabajar

"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 8000
""""
Vinculamos el objeto de socket del servidor a una dirección IP y un número de puerto específicos
ponemos el socket del servidor en modo de escucha para aceptar conexiones entrantes de los clientes.
"""
server_socket.bind((host, port))
server_socket.listen()

""""
La función está diseñada para manejar la comunicación entre el servidor y un cliente específico.

el bucle while True que se ejecuta continuamente mientras el cliente esté conectado al servidor
"""
def handle_client(client_socket,address):
    while True:
        try:
            data = client_socket.recv(1024)  #Se reciben los datos del cliente
            if not data:                     #Se verifica si el cliente si no es nulo
                break
            if data.decode() == "En espera": #Se recibe un dato y se compara en caso de ser True
                pregunta_respuestas_puntajes = Datos.generar_pregunta()  #se genera la pregunta 
                client_socket.send('\n'.join(pregunta_respuestas_puntajes).encode()) #se envia la pregunta al cliente
            else:                              #En caso de ser false
                data = data.decode().split('\n')    #Se actualiza el puntaje y se envia al cliente
                nuevo_puntaje = (data[0], int(data[1]))
                Datos.actualizar_puntaje(nuevo_puntaje)
                pregunta_respuestas_puntajes = Datos.generar_pregunta()
                client_socket.send('\n'.join(pregunta_respuestas_puntajes).encode())
        except ConnectionResetError:
            break
    client_socket.close()  

#se ejecuta continuamente y espera a que un cliente se conecte al servidor
while True:
    print("Escuchando")
    client_socket, address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,address))
    client_thread.start()
