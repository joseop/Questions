import socket

#Importamos la libreria Socket y definimos el metodo iniciar
#Este metodo sirve para instancia un objeto cliente y realizar la coneccion con el servidor
#Asignamos el host y puerto del servidor y procedemos a hacer la coneccion
host = '192.168.30.16'
port = 8000
def iniciar():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

#Con este metodo procedemos a hacer la transferencia de datos entre el cliente y el servidor
def solicitud(client_socket, request):
    client_socket.send(request.encode())
    data = client_socket.recv(1024)
    return (data.decode())

#Este metodo sirve para cerrar el cliente conectado al servidor
def cerrar(client_socket):
    client_socket.close()
