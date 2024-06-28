import socket
import threading

# Es para solicitar nombre de usuario
usuario = input("ingrese su usuario: ")

host = '127.0.0.1'
port = 9099

# Coneccion del cliente al servidor.
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host,port))


def mensaje_recibido():
    while True:
        try:
            mensaje = cliente.recv(1024). decode("utf-8")
            if mensaje =="user":
                cliente.send(usuario.encode("utf8"))
        
            else:
                print(mensaje)

        except:
            print("ocurrio un error")
            cliente.close()
            break

def write_menssages():
    while True:
        message = f"{usuario}:{input('')}"
        cliente.send(message.encode('utf-8'))

receive_thread = threading.Thread(target= mensaje_recibido)
receive_thread.start() 

write_thread = threading.Thread(target= write_menssages)
write_thread.start()


