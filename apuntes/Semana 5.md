---
attachments: [Clipboard_2023-09-11-21-40-42.png, Clipboard_2023-09-11-22-26-08.png, Clipboard_2023-09-11-22-35-41.png, Clipboard_2023-09-11-23-57-26.png, Clipboard_2023-09-11-23-57-47.png]
tags: [prog-avanzada]
title: Semana 5
created: '2023-09-11T23:24:13.167Z'
modified: '2023-09-12T03:01:18.959Z'
---

# Semana 5

## Threading
### Intro
- Los threads nos permiten tener **múltiples flujos de instrucciones** dentro del mismo código del programa.


### Procesos y núcleos
- Al ejecutarse múltiples programas o aplicaciones en paralelo, se crean varios **procesos** por el SO. Un proceso es un programa en ejecución ocupando un espacio de RAM y ejecutando instrucciones.
- Los sistemas modernos tienen multiples cores, los cuales pueden correr varios procesos en paralelo.
- Realmente cada core puede ejecutar un programa a la vez, pero el SO le da un espacio en cada segundo a cada programa para ejecutarse, haciendo parecer que hay paralelismo.


### Threading
- Un *thread* o hilo, es una unidad de ejecución de código dentro de un proceso.
- El proceso es el programa cargado en memoria con código y variables, y el thread tiene variables locales, código y una especie de program counter.
![](@attachment/Clipboard_2023-09-11-21-40-42.png)
- Todo proceso tiene un thread principal. Pero se pueden crear mas threads y tener paralelismo mediante el SO.


#### Usos de threads
- Algunos usos de threads:
  - Modelo **productor-consumidor**: Se opera sobre el mismo conjunto de datos pero realizando distintas operaciones al mismo tiempo. Ej: Un thread recibe input y lo coloca en cola por procesar, otro thread procesa linea a linea y los saca de la cola
  - Interfaces gráficas: Reciben input mediante entradas y botones, pero otros threads manejan la parte visual al mismo tiempo
  - Aplicaciones multiusuario: Servidores

#### Creación de threads
- Vienen en modulo threading `import threading`.
- La clase Thread representa un hilo. A cada hilo se le entrega un target, el cual sera la funcion a ejecutar.
- con `threading.Thread(target=funcion)` creamos un Thread que llame a la función funcion
- con `thread.start()` iniciamos un objeto Thread.
- Ej:
```py
import threading

# funcion generica
def count_monkeys():
  print('hola')
  for i in range(20):
    print(f'contando {i+1}')
  print("fin")

my_thread = threading.Thread(target=count_monkeys) # se pasa la funcion a ejecutar

my_thread.start() # se ejecuta el codigo del hilo.

my_thread.start() # NOTA: esto da error, un thread creado asi no puede iniciarse mas de 1 vez

```

- `threading.current_thread()` retorna referencia al thread que esta ejecutando el codigo actual
- Se puede acceder al `thread.name` para saber en cual estamos. El thread principal se llama `MainThread`

- Ej 2:
```py
import threading

def saludar():
  current_thread = threading.current_thread()
  print(f'Hola desde {current_thread.name}')

thread_1 = threading.Thread(name='Thread 1', target=saludar) # setear nombre
thread_2 = threading.Thread(name='Thread 2', target=saludar)

thread_1.start() # saludar via thread 1
thread_2.start() # saludar via thread 2

saludar() # llamando a saludar directamente, deberia decir MainThread

```
- Ej 3: (threads con sleep)
```py
import threading
import time


def trabajador_rapido():
    # Función rápida, que toma 2 segundos
    thread_actual = threading.current_thread()
    print(f"{thread_actual.name} partiendo...")
    # Pondremos a dormir el thread por 2 segundos simulando
    # que ocurre algun proceso dentro de la función
    time.sleep(2)
    print(f"{thread_actual.name} terminando...")


def trabajador_lento():
    # Función lenta, que toma 6 segundos
    thread_actual = threading.current_thread()
    print(f"{thread_actual.name} partiendo...")
    # Ponemos a dormir el thread por 6 segundos simulando
    # un proceso más largo que el anterior dentro de la función
    time.sleep(6)
    print(f"{thread_actual.name} terminando...")


# Creamos los threads usando la clase Thread
hilo_lento = threading.Thread(name="Hilo lento (6s)", target=trabajador_lento)
hilo_rapido_1 = threading.Thread(name="Hilo rápido (2s)", target=trabajador_rapido)
# Usa el nombre asignado por defecto
hilo_rapido_2 = threading.Thread(target=trabajador_rapido)
print("Thread principal: Fueron creados 3 threads")


##
print("Thread principal: Empezaré a iniciar los 3 threads")
hilo_rapido_1.start()  # Dormirá por 2 segundos
hilo_rapido_2.start()  # Dormirá por 2 segundos
hilo_lento.start()  # Dormirá por 6 segundos
print("Thread principal: Fueron iniciados 3 threads")
# Todas estas líneas que siguen serán ejecutadas mientras los threads
# se ejecutan independientemente del programa principal

print()
# El thread principal ejecutará lo que queda de código
# mientras los otros 3 threads hacen lo suyo

for i in range(10):
    print(f"Thread principal: Segundo actual: {i}")
    time.sleep(1)


```
- Ejecución:
  ![](@attachment/Clipboard_2023-09-11-22-26-08.png)
- Se ejecuta el código de MainThread en paralelo con el contador, los dos hilos rapidos y el lento empiezan al mismo tiempo. los hilos rapidos terminan a la vez en 2 segundos y el lento en 6.



- Problemas con print
  - El escribir un texto con print tiene el problema de que escribir un texto y un salto de linea son instrucciones distintas, y puede que no se ejecuten en el mismo ciclo del thread.

- Ej 4 (Pasar argumentos a thread):
  - Se hace via el atributo `args=` y `kwargs=` al crear un Thread.
```py
import threading
import time

def count_monkeys_until(max_monkeys):
  current_thread = threading.current_thread()
  print(f'current thread: {current_thread.name}')
  for i in range(max_monkeys):
    time.sleep(1)
    print(f'{current_thread.name}: count {i+1}')
  
  print(f'{current_thread.name} finished..')


## passes 10 as a positional argument
t1 = threading.Thread(name='Thread 1', target=count_monkeys_until, args=(10, ))

# passes time as a positional argument w with key "max_monkeys" 
t2 = threading.Thread(name='Thread 2', target=count_monkeys_until, kwargs={"max_monkeys": 10})


t1.start()
t2.start()

```

##### Objeto Thread OOP
- Se pueden crear clases que hereden de `threading.Thread`, donde habra que inicializar via init y modificar la funcion `run()`, la cual tendra el codigo que se ejecutara al iniciar el thread.
- Ej:

```py
class CountMonkeys(threading.Thread):
    def __init__(self, name, max_monkeys, *args, **kwargs) -> None:
        super().__init__(name=name, *args, **kwargs)
        self.max_count = max_monkeys

    def run(self):
        current_thread = threading.current_thread()
        print(f'current thread: {current_thread.name}')
        begin_time = time.time()
        for i in range(self.max_count):
            time.sleep(1)
            print(f'{current_thread.name}: count {i+1} monkeys')

        print(f'{current_thread.name} finished..')
        print(f'{current_thread.name} went to sleep after {time.time() - begin_time}..')


# snakes are faster in this world, and they dont stop every sec
class CountSnakes(threading.Thread):
    def __init__(self, name, max_snakes, *args, **kwargs) -> None:
        super().__init__(name=name, *args, **kwargs)
        self.max_count = max_snakes

    def run(self):
        current_thread = threading.current_thread()
        print(f'current thread: {current_thread.name}')
        begin_time = time.time()
        for i in range(self.max_count):
            if ((i+1) % 2) == 0:
                time.sleep(1)
            print(f'{current_thread.name}: count {i+1} snakes')

        print(f'{current_thread.name} finished..')
        print(f'{current_thread.name} went to sleep after {time.time() - begin_time}..')


t1 = CountMonkeys('Thread 1', 10)

t2 = CountSnakes('Thread 2', 10)
## snakes finish faster

t1.start()
t2.start()

```


#### join()
- Permite que un thread este pausado o **bloqueado** en espera de un resultado de otro thread. 
- El caller del thread no se sigue ejecutando hasta que termine el calleado o haya timeout
- Se hace via `join(timeout=None)` luego de haber iniciado thread via start()
- Ej visual:
  ![](@attachment/Clipboard_2023-09-11-22-35-41.png)

- Ej 1 (no me gusto xd, revisar):
```py
#.. codigo de clases e imports

# Usamos la definicion de los Thread declarados en el ejemplo anterior
# Se crean los threads usando la clase Thread.
hernan = CuentaOvejas("Hernán", 5)
daniela = CuentaOvejas("Daniela", 7)
fran = CuentaLiebres("Fran", 5)
joaquin = CuentaLiebres("Joaquín", 6)
paqui = CuentaLiebres("Paqui", 20)

# Se inicializan los threads creados
hernan.start()
daniela.start()
fran.start()
joaquin.start()
paqui.start()
print("Ayudantes: Los profes se fueron a dormir...")

# Aquí incorporamos el método join() para bloquear el programa principal
daniela.join()  # No especificamos timeout, esperará lo que sea necesario
print("Ayudantes: ¡DANIELA SE DURMIÓ!")
hernan.join() # No especificamos timeout, esperará lo que sea necesario
print("Ayudantes: ¡HERNÁN SE DURMIÓ!")
fran.join() # No especificamos timeout, esperará lo que sea necesario
print("Ayudantes: ¡FRAN SE DURMIÓ!")
joaquin.join() # No especificamos timeout, esperará lo que sea necesario
print("Ayudantes: ¡JOAQUÍN SE DURMIÓ!")
paqui.join(1)  # Esperaremos máximo 1 segundo después del último dormido, ya es muy tarde
print("Ayudantes: ¡(casi todos) los profes se durmieron! ¡A festejar!")

# En este punto, el programa ha esperado por los cuatro threads que creamos
# Estas líneas serán ejecutadas después de que los threads hayan terminado
for _ in range(6):
    print("Ayudantes: 🎵🎶🎵🎶🎵🎶🎵🎶🎵🎶🎵🎶🎵🎶🎵🎶")
    time.sleep(1)
print("Ayudantes: Ojalá no nos hayan escuchado...")
        
```
- Explicación: Termina en orden: Fran, Joaquin, Hernan, Daniela, pero se imprime primero daniela se durmio ya que esto se estaba esperando, luego se imprime hernan, luego fran y luego joaquin, por el orden de los join.
- Despues quedando 1 profesor se ejecuta el codigo de los emojis
- Se termina despues de esperar 1 segundo mas a paqui despues de todo el tiempo esperado.

- Ojo con el orden de los start y join. join siempre significa esperar antes de hacer cualquier cosa.

#### is_alive()
- La función `is_alive()` de un objeto thread permite saber si un thread sigue en ejecución.
- Un uso comun es ver si sigue despues de un .join() con timeout.

#### Daemons
- Los daemon threads son threads que aunque esten corriendo, **no impiden que el programa principal termine**.
- Cuando el programa termina, **son terminados inmediatamente**.
- El programa principal terminará cuando todos los threads no daemon terminen.
- se activa un thread como daemon via `daemon=True` como parametro.

- Ej 1:
```py
import threading
import time


def dormilon():
    print(f"{threading.current_thread().name} tiene sueño...")
    time.sleep(2)
    print(f"{threading.current_thread().name} se durmió.")

    
def con_insomnio():
    print(f"{threading.current_thread().name} tiene sueño...")
    time.sleep(10)
    print(f"{threading.current_thread().name} se durmió.")


# Forma 1 de hacer un thread daemon
dormilon = threading.Thread(name="Dormilón", target=dormilon, daemon=True)
# Forma 2 de hacer un thread daemon
con_insomnio = threading.Thread(name="Con insomnio", target=con_insomnio)
con_insomnio.daemon = True

# Se inicializan los threads
dormilon.start()
con_insomnio.start()

```
- Ej 1 (con daemon):
- Los threads se ven interrumpidos al ser daemon y el programa finalizando su ejecución inmediatamente, entonces su mensaje final no se imprime.
![](@attachment/Clipboard_2023-09-11-23-57-47.png)
- Ej 1 (sin daemon):
- Se ejecuta un thread completo y se espera, luego se ejecuta el siguiente.
![](@attachment/Clipboard_2023-09-11-23-57-26.png)

- TODO: revisar lo de aqui
- Ej 2 (se puede usar join() para esperar a un daemon):
```py
import threading
import time


def dormilon():
    print(f"{threading.current_thread().name} tiene sueño...")
    time.sleep(2)
    print(f"{threading.current_thread().name} se durmió.")

    
def con_insomnio():
    print(f"{threading.current_thread().name} tiene sueño...")
    time.sleep(10)
    print(f"{threading.current_thread().name} se durmió.")


# Forma 1 de hacer un thread daemon
dormilon = threading.Thread(name="Dormilón", target=dormilon, daemon=True)
# Forma 2 de hacer un thread daemon
con_insomnio = threading.Thread(name="Con insomnio", target=con_insomnio)
con_insomnio.daemon = True

# Se inicializan los threads
dormilon.start()
con_insomnio.start()

# Esperamos los threads.
# Lo esperamos por una cantidad indefinida de tiempo
dormilon.join()
# Esperamos sólo 5 segundos
con_insomnio.join(5)
```

- Ej 3 (Daemon tipo objeto):
```py
class Daemon(threading.Thread):
    
    def __init__(self):
        super().__init__()
        # Cuando inicializamos el thread lo declaramos como daemon
        self.daemon = True
    
    def run(self):
        print("Daemon thread: Empezando...")
        time.sleep(2)
        print("Daemon thread: Terminando...")

        
daemon = Daemon()
daemon.start()
daemon.join()
```

- Luego del start() no podemos cambiar un thread a daemon o viceversa


- revisar mejor: Si se interrumpen los threads inesperadamente, por ejemplo siendo daemon y sin tener mas instrucciones en el programa, se pueden producir errores raros al imprimir strings u otros.

#### Timers
- Es una subclase de la clase Thread y permite ejecutar un proceso luego de esperar determinado tiempo.
- segundos es float.
- Pide `(segundos, funcion_a_ejecutar, argumentos_via_args_o_kwargs=)`
- `cancel()` permite cancelar la ejecución antes de que se ejecute el timer.
- Ej 1:
```py
def mi_timer(ruta_archivo):
    with open(ruta_archivo) as archivo:
        for linea in archivo:
            print(linea.strip())

t1 = threading.Timer(4.0, mi_timer, args=("files/mensaje_01.txt",))
t2 = threading.Timer(1.0, mi_timer, kwargs={"ruta_archivo": "files/mensaje_02.txt"})

print("Activando timer 1 que comenzará luego de 4 segundos")
t1.start() # el thread t1 comenzará después de 4 seconds

print("Activando timer 2 que comenzará luego de 1 segundos")
t2.start() # el thread t2 comenzará después de 1 seconds

# se ejecuta primero el timer 2, y luego el 1.
```


## Concurrencia

### Sincronización

### Mecanismos de sincronización


### Deadlocks


## Ejemplos y aplicaciones

