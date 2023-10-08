---
attachments: [Clipboard_2023-10-07-16-22-27.png, Clipboard_2023-10-07-16-41-37.png]
tags: [prog-avanzada]
title: Semana 9
created: '2023-10-07T16:20:56.021Z'
modified: '2023-10-08T12:33:53.250Z'
---

# Semana 9


## Conceptos Networking
- Cómo interactuamos con programas ejecutandose en otras maquinas?

### Como se comunican los computadores?
- Medio: Se refiere a como se transmite el mensaje, puede ser cable Ethernet, WifI o señales de telefonia.
- Destinatario: Maquina que se identifica con la **dirección IP**
- Protocolo de transmisión: Reglas para que el mensaje emitido sea recibido correctamente por el otro. Ej: TCP, UDP.
- Protocolo de aplicación: Reglas que todos los programas deben respetar para que la comunicación funciene entre ellos. Aquí se toma en cuenta: **formato, orden, y contenido** del los mensajes. Ej: HTTP, DNS, SMTP. Cada programa tendrá reglas especiales además.


### Identificacion de computadores en Internet
- Cada maquina es un *host*, que puede ejecutar programas que envian y reciben datos.

#### Dirección IP
- Esta permite identificar a un dispositivo o *host*. Definida por el ISP via un router.
- Versiones:
  - IPv4: 4 bytes (32 bits). Cada byte se separa por un punto. 2^32 direcciones. Ej: `255.255.255.255`
  - IPv6: 128 bits. 8 grupos de 16 bits (FFFF). Cada grupo de bits se escribe en hexa. 2^128 direcciones. Ej: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

#### DNS
- Los servidores DNS resuelven dominios como `google.com` a una dirección IP, permitiendo comunicarse usando dominios.

#### Puertos
- Permiten dirigir el tráfico de red a un programa específico dentro del mismo computador. Cada programa ocupa un puerto a la vez. El puerto es de 16 bits (Rango 2e6 0-65535).
- Puertos Comunes: FTP 21, SSH 22, SMTP 25, DNS 53, HTTP 80, HTTPS 443.
- Es decir: para comunicarse con un programa en otro host, necesitamos dirección y puerto./


### Protocolos de comunicación
- Los protocolos de transporte permiten que un mensaje del programa emisor sea recibido por el programa receptor.
- Los mensajes son **varios bytes serializados**. Estos no se pueden enviar de una si es demasiada información, además hay alta probabilidad de errores de transmisión.
- Los protocolos separan los mensajes en **paquetes**. Cada paquete tiene la dirección IP y el puerto del destinatario, y la **posición dentro del mensaje original**, para poder reconstruirlo.
- Aún así llegan paquetes alterados, o se pierden (*packet loss*), y los router los botan. Los protocolos actúan de distintas formas frente a esto.


#### TCP (*Transmission Control Protocol*)
- Permite enviar un *stream* (flujo) de *bytes serializados*. Es **confiable**: Todos los paquetes llegan de forma íntegra sin errores. Es decir: 
  - Verifica que cada paquete no haya sido alterado
  - Solicita que se confirme la llegada correcta de cada paquete
  - Retransmite los paquetes perdidos o dañados.
- Al recibirse correctamente todos los paquetes, declara que el mensaje se recibio correctamente.

- Al iniciar una transmisión TCP, primero se hace un **handshake**. En este el emisor y receptor se ponen de acuerdo en: Tiempo de espera, cantidad de paquetes simultaneos, memoria, etc. Esto quiere decir que es un protocolo **connection-oriented**.

- Este proceso significa garantizar la **fiabilidad** de la conexión, con un costo de cierta latencia, pero es necesario para aplicaciones que necesitan integridad.
- Algunos **protocolos de aplicación** que usan TCP: HTTP, SMTP, BitTorrent.



#### UDP (*User Datagram Protocol*)
- Permite enviar paquetes (*datagramas*), **sin garantías de integridad**. 
- UDP permite la pérdida de paquetes. Al recibir un paquete con errores, lo descarta y no pide su retransmisión. UDP hace *best-effort* para enviar mensajes, pero no entrega certezas.

- UDP es *connectionless*. Esto es ya que **no hay handshake**. Los paquetes llegan (o no).

- Es mas liviano que TCP y tiene menor latencia, pero puede tener pérdida de datos. Se usa en cosas como transmisión de audio y vídeo.
- No se ve en este curso.

### Encapsulamiento
- Es la modelación de la comunicación entre 2 dispositivos o procesos. Se separa en capas, cada capa tiene una responsabilidad, y confía en el funcionamiento de las anteriores.
- Hay 2 modelos:
![](@attachment/Clipboard_2023-10-07-16-22-27.png)
- Nuestros programas operan en la capa de aplicación y ocupan un protocolo de transporte como TCP, provisto por el SO.


## Python TCP: Networking con Python

### Arquitectura cliente-servidor
- Una arquitectura se refiere a una forma de conectar o construir *hardware o software* para cumplir estándares.
- En la arquitectura cliente-servidor, el servidor ofrece serivcios al cliente quien los consume.
- El cliente es quien inicia y establece la conexión de acuerdo a algún protocolo.
- El servidor se dedica a esperar y escuchar conexiones entrantes. Al recibir una solicitud de conexión, decide aceptar o no, y envía una respuesta al cliente según protocolo.
![](@attachment/Clipboard_2023-10-07-16-41-37.png)

### Sockets
- Es un objeto del sistema operativo que permite que un programa transmita y reciba datos desde un programa de otra máquina, o en la misma máquina pero otro puerto. (Podría ser similar a un archivo del SO, con lectura y escritura.
- Para obtener un socket, especificamos la IP a usar, y el protocolo de transporte.
- En Python, usar módulo `socket`. Se crea una instancia usando `socket.socket(family, type)`. family es el tipo de dirección IP, y type es el protocolo de transporte.
- Tipos permitidos y ejemplo:
```py
import socket

# family socket.AF_INET IPv4 socket.AF_INET6 IPv6
# type socket.SOCK_STREAM TCP socket.SOCK_DGRAM UDP
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

```
### Ejemplo cliente-servidor

#### Cliente TCP
- Se establece la conexión con el destinatario usando el método `connect((host, port))` de un `socket`. Es una tupla, con IP (string) y puerto (int) (la IP puede ser una direccion DNS).
- Ej 1 (conexion):
```python
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

my_socket.connect(('146.155.123.21', 80)) # con IP
my_socket.connect(('canvas.uc.cl', 80)) # con DNS addr.
```

- **Envio de bytes**: Se deben enviar mensajes codificados, se ocupan los siguientes métodos:
  - `send(bytes)`: Trata de enviar el mensaje pasado. Si el envio resulta en error o no se envia completamente, no vuelve a enviar. **Retorna cantidad de bytes enviados correctamente**, uno maneja que se hace con esa información, para enviar el mensaje completo.
  - `sendall(bytes)`: Se asegura de enviar **todos los bytes**. Usa `send()` hasta que el mensaje se envié completamente. En el caso de fallar, simplemente retorna un error, y no la cantidad de bytes que no se enviaron.

- Ej 1 (envio):
```python
request_txt = 'GET HTTP/1.1\n\n\n'  # text to be sent

encoded = request_txt.encode('utf-8')  # encodes text in utf-8 BYTES

my_socket.sendall(encoded) # sends all bytes

```

- **Recepción de bytes**: Para recibir la respuesta del servidor, ocupamos `recv(buffer)`, que retorna un objeto `bytes`. El parametro es el **maximo** de bytes a ser leidos. Se recomienda usar potencias de 2 pequeñas.
  - Si al momento de hacer recv() se han enviado menos bytes, solo esos bytes se recibiran.
- Finalmente se cierra la conexion con `my_socket.close()`.

- Ej 1 (recibir datos):
```python
recieved_data = my_socket.recv(4096)  # recieves max 4096 bytes at this moment.

print(recieved_data.decode('utf-8'))  # decodes the recieved bytes into text.
```

- Ej 1 completo:
```python
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

my_socket.connect(('canvas.uc.cl', 80))

request_txt = 'GET HTTP/1.1\n\n\n'  # text to be sent

encoded = request_txt.encode('utf-8')  # encodes text in utf-8 text

my_socket.sendall(encoded)

recieved_data = my_socket.recv(4096)  # recieves max 4096 bytes at this moment.

print(recieved_data.decode('utf-8'))  # decodes the recieved bytes into text.

my_socket.close()

```

- Ejemplo 2 (con manejo de errores):
  - Nota: `ConnectionError` es exception base de errores de sockets.
```python
import socket

# create IPv4 TCP socket
my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = "iic2333.ing.puc.cl"
port = 80

try:
    my_sock.connect((addr, port))  # connect to the specified server
    msg = 'GET / HTTP/1.1\nHost: iic2333.ing.puc.cl\n\n'  # standard HTTP
    my_sock.sendall(msg.encode('utf-8'))  # send bytes

    data = my_sock.recv(4096)  # recieve data.
    print(data.decode('utf-8'))

except ConnectionError as e:
    print('Error')
    print(e)
finally:  # always executed
    my_sock.close()

```
- El ejemplo anterior se conectaba al puerto 80 (HTTP) de `iic2233.ing.puc.cl`, tiene texto plano, no HTTPS.


#### Servidor TCP
- https://docs.python.org/3/howto/sockets.html
- El servidor debe escuchar conexiones en un puerto específico. Para asociar el socket, usamos el metodo `bind((host, port))` `(host,port)` (tuple) del socket.
- Se llama a `listen()` para empezar a escuchar
- Se llama a `accept()` para aceptar conexion, que retorna un socket para conectarse a un cliente y la direccion y puerto del cliente. **este metodo espera a una conexion entrante** (usar en thread para no congelar programa)
- Ej 3 (escuchar en puerto y enviar paquete)
```py
import socket

my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = socket.gethostname() # returns the machine ip
port = 9999

# bind socket to addr, port

my_sock.bind((addr, port))  # connect also binds automatically to random port.

my_sock.listen()

while True:
    # accept() opens socket connected with the client
    client_socket, addr_port = my_sock.accept()  # accept connection, use client socket and ip info
    print(f'Accepted connection from: {addr}')
    msg = 'Conectado!\n'
    my_sock.sendall(msg.encode('utf-8'))
    my_sock.close()

# never reached, example
my_sock.close()  # stops waiting for more connection attempts

```

#### Ej cliente y servidor simple
- Ej 4 (cliente y servidor)
- Servidor
```py
import socket

my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = socket.gethostname()  # returns the machine ip
port = 9999

# bind socket to addr, port

my_sock.bind((addr, port))  # connect also binds automatically to random port.

my_sock.listen()

ct = 0
while ct < 5:
    try:
        # accept() opens socket connected with the client
        client_socket, addr_port = my_sock.accept()  # accept connection, use client socket and ip info
        print(f'Accepted connection from: {addr}')
        msg = 'Conectado!\n'
        client_socket.sendall(msg.encode('utf-8'))
        client_socket.close()
        ct += 1
    except ConnectionError as e:
        print("Error:", e)

print("Finishing..")
# reached after 5
my_sock.close()  # stops waiting for more connection attempts

```
- Cliente
```py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()  # the current computer
port = 9999

try:
    sock.connect((host, port))
    # sock.sendall() # no need to send anything
    stream = sock.recv(4096)
    print(stream.decode('utf-8'))  # it should print Conectado!\n
except ConnectionError as e:
    print("Error", e)
finally:
    sock.close()

```

## Ejemplos

### Envío de JSON
- Ejemplo de *echo server*, recibe datos y los envia de vuelta al cliente
- Servidor:
```py
import socket

# only an echo server

# addr = socket.gethostname()
addr = ''  # this means localhost
port = 9998

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((addr, port))  # start listening
print(f'Listening for clients in {addr}:{port}..')
sock.listen()

client_sock, (client_addr, client_port) = sock.accept()
print(f'Accepted connection from {client_addr}:{client_port}.')

# The server only accepts 1 connection, and after that it stops everything.
while True:
    data = client_sock.recv(4096)
    print(f'Recieved bytes: {data}, sending back...')
    if not data:  # recieved empty byte: b'', it means end connection
        break  # stop listening
    client_sock.sendall(data)  # send data back


client_sock.close()  # stop listening for specific client
sock.close()  # stop listening for clients
```
- Cliente:
```py
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = ''
port = 9998


sock.connect((addr, port))

json_dict_sample = {1: "hola", 2: "aaaaaa"}
json_dict_sample = json.dumps(json_dict_sample)  # dict -> JSON string

# now we send the message (encoded in utf 8 bytes)


sock.sendall(json_dict_sample.encode('utf-8'))  # json str -> bytes


# recieve the echoed message and decode.

recieved = sock.recv(4096).decode('utf-8')  # bytes -> JSON str
deserialized_rec = json.loads(recieved)  # JSON str -> dict

print("Recieved:")
print(type(deserialized_rec))  # type dict
print(deserialized_rec)  # dictionary
# print(json_dict_sample)  # see if it is the same

input("press any key to end the program...")
sock.close()

```
### Envío de datos usando *pickle*
- Ejemplo enviando datos serializados con `pickle`. Ocupa mismo echo server que reevnia los bytes. El cliente recibe los datos de nuevo, los deserializa y los devuelve a su estado original.
- Servidor:
```py
import socket

# only an echo server

# addr = socket.gethostname()
addr = ''  # this means localhost
port = 9998

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((addr, port))  # start listening
print(f'Listening for clients in {addr}:{port}..')
sock.listen()

client_sock, (client_addr, client_port) = sock.accept()
print(f'Accepted connection from {client_addr}:{client_port}.')

# The server only accepts 1 connection, and after that it stops everything.
while True:
    data = client_sock.recv(4096)
    print(f'Recieved bytes: {data}, sending back...')
    if not data:  # recieved empty byte: b'', it means end connection
        break  # stop listening
    client_sock.sendall(data)  # send data back


client_sock.close()  # stop listening for specific client
sock.close()  # stop listening for clients
```
- Cliente:
```py
import socket
import pickle

host = ''
port = 9998


class Animal:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type


# serialize obj
monkey_obj = Animal("aaa", "monkey")

obj_serialized = pickle.dumps(monkey_obj)

# send serialized obj

sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_out.connect((host, port))
sock_out.sendall(obj_serialized)

# recieve the echoed message
recieved = sock_out.recv(4096)
recieved_deserialized = pickle.loads(recieved)

print(f"Recieved back obj with type {type(recieved_deserialized)}")
print(recieved_deserialized.name)
print(recieved_deserialized.type)

sock_out.close()

```
- ...

### Envío de muchos datos a un archivo (e7)
- La idea es transmitir un archivo grande entre 2 computadores. El receptor es el servidor y quien envia el archivo es cliente.
- Problema: como saber cuantos bytes recibir? (recv()).
- Solucion: se envian 4 bytes con el tamaño del archivo, luego se recibe por chunks el archivo hasta alcanzar los bytes requeridos.
- Servidor:
```py
import socket

# Server that recieves a file acc to protocol.

addr = ''  # this means localhost
port = 9997

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((addr, port))  # start listening
print(f'Listening for clients in {addr}:{port}..')
sock.listen()

client_sock, (client_addr, client_port) = sock.accept()
print(f'Accepted connection from {client_addr}:{client_port}.')

# The server only accepts 1 connection, and after that it stops everything.

# get bytes to recieve according to our protocol
bytes_to_recieve = client_sock.recv(4)
bytes_to_recieve_int = int.from_bytes(bytes_to_recieve, 'big')

print(f'Trying to recieve a file of {bytes_to_recieve_int} bytes.')

data_recieved = bytearray()
bytes_recieved = 0

while bytes_recieved < bytes_to_recieve_int:
    chunk = client_sock.recv(min(4096, bytes_to_recieve_int - bytes_recieved))  # send a chunk of 4096 or the amount of bytes pending
    bytes_recieved += len(chunk)
    data_recieved.extend(chunk) # add the data to the bytearray
    print(f'Recieved {bytes_recieved}/{bytes_to_recieve_int} bytes')

print(f'File successfully recieved!')
client_sock.sendall('finished'.encode('utf-8'))

client_sock.close()  # stop listening for specific client
sock.close()  # stop listening for clients

# write to file
with open('../files/recieved.bin', 'wb') as f:
    f.write(data_recieved)
    f.close()

```
- Cliente:
```py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ''
sv_port = 9997

sock.connect((sv_addr, sv_port))
# connected to server

with open('../files/enviar.bin', 'rb') as f:
    data_from_file = f.read()  # in bytes
    f.close()
    bytes_to_send = len(data_from_file)
    sock.sendall(bytes_to_send.to_bytes(4, 'big'))  # send 4 bytes of the file length
    sent_bytes = 0
    print(f"Trying to send {bytes_to_send} bytes...")
    while sent_bytes < bytes_to_send:
        chunk = data_from_file[sent_bytes:]  # raro
        # it sends part of the message by default.
        sent_bytes += sock.send(chunk)  # send returns the bytes successfully sent, add them


print('File sent, closing connection...')
print(f'Response: {sock.recv(4096).decode("utf-8")}')
sock.close()

```

### Ej completo: Servidor con manejo de multiples clientes (concurrente)
- Para poder manejar múltiples clientes se usan *threads*. 
- Al ejecutar `socket.accept()` el thread se bloquea hasta aceptar una nueva conexión
- Al ejecutar `socket.recv()` el thread se bloquea hasta recibir datos
- Modelo: Se crea un thread encargado de:
  - Aceptar nuevos clientes
  - Al aceptar un cliente, crear un thread nuevo que escuche y envie datos al nuevo cliente.

- Servidor:
```python

```

- Cliente:
```python


```



### Ej completo: Servidor backend + Cliente con GUI PyQt
- Pendiente

## Bonus: Python UDP
- Pendiente
