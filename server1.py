import socket
import threading

host = '127.0.0.1'
port = 9099

#El servidor está en modo escucha.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host,port))
server.listen()

print(f"servidor corriendo en {host}:{port}")

#compartimos mensaje con el resto de los conectados al servidor
clientes = []
usuarios = []

def compartir_msg(mensaje,_cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)

def control_msg(cliente):
    
    while True:
      try:
        mensaje = cliente.recv(1024)
        compartir_msg(mensaje,cliente)
      except:
         index = clientes.index(cliente) #si el cliente se desconecta.
         usuario = usuarios[index]
         mensaje=(f"chat:{usuario} desconectado". encode('utf-8'))
         compartir_msg(mensaje,cliente)
         print(f"{usuario} se desconecto") 
         clientes.remove(cliente)
         usuarios.remove(usuario)
         cliente.close()
         break
                       
# Coneccion con los clientes.

def recibir_coneccion():
    contador = 0
    while True:
        contador += 1
        print(f"usuarios conectados:{contador}")
        cliente,addres = server.accept()
        cliente.send("user". encode("utf-8"))
        usuario = cliente.recv(1024). decode ("utf-8")
        # Se agregan al servidor el usuario
        clientes.append(cliente)
        usuarios.append(usuario)
        print(f"{usuario} esta conectado con {str(addres)}") 
          # Informamos al resto de los usuario quien se conecto.
        mensaje = f"chat: {usuario} se conecto!". encode("utf-8")
        compartir_msg(mensaje,cliente)
        cliente.send ("conectado al servidor ".encode("utf-8"))
        
        thread = threading.Thread(target =control_msg,
                                  args = (cliente,)
                                  )
        thread.start()
recibir_coneccion()

