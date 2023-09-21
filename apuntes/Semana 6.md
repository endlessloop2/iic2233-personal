---
attachments: [Clipboard_2023-09-21-00-55-51.png]
tags: [prog-avanzada]
title: Semana 6
created: '2023-09-20T01:50:44.607Z'
modified: '2023-09-21T04:15:10.009Z'
---

# Semana 6

## QThreads

### Threads y PyQt
- Los threads son compatibles con PyQt, por lo tanto se pueden usar normalmente, aunque lo recomendable es usar QThread.

- Ejemplo 1 con qtsignals y Threads de Python:
```py
class MyThread(Thread):
    def __init__(self, signal: pyqtSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal

    # runs after thread.start() is called
    def run(self) -> None:
        for i in range(10):
            # send signal with text to windowa
            self.signal.emit(str(i))
            time.sleep(1)


class WindowA(QWidget):
    signal_from_thread = pyqtSignal(str)  # signal recibe texto a cambiar

    def __init__(self) -> None:
        super().__init__()
        self.thread_1 = None  # created empty
        self.init_gui()
        self.signal_from_thread.connect(self.update_text)  # run update_text when recieving signal

    def init_gui(self):
        self.setGeometry(20, 20, 250, 250)
        self.setWindowTitle('test')

        layout_1 = QVBoxLayout()

        self.label_1 = QLabel(text="Status: Thread no ejecutado")
        self.button_1 = QPushButton(text="Ejecutar Thread")
        layout_1.addStretch(1)
        layout_1.addWidget(self.label_1)
        layout_1.addStretch(2)
        layout_1.addWidget(self.button_1)
        layout_1.addStretch(10)
        self.setLayout(layout_1)

        self.button_1.clicked.connect(self.start_thread)

    def start_thread(self):
        self.button_1.setText("Status: Thread iniciado..")

        # if it was never started clicked, or if it finished, create new thread and run
        if self.thread_1 is None or not self.thread_1.is_alive():
            self.thread_1 = MyThread(self.signal_from_thread)
            self.thread_1.start()

    # process and recieve signal from thread
    def update_text(self, text):
        self.label_1.setText(text)

```


### QThread
- PyQt es la version PyQt de `Thread`. Viene en el modulo `PyQt6.QtCore`.
- Documentación: https://doc.qt.io/qt-6/qthread.html
- Docs Python: https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html 

- Ej 2 (Equivalente usando QThread):
- El único cambio fue usar `isRunning()` en vez de `is_alive()`. Es comun cambiar nombres de funciones pero son equivalentes.
```py
class MyThread(QThread):
    def __init__(self, signal: pyqtSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal

    # runs after thread.start() is called
    def run(self) -> None:
        for i in range(10):
            # send signal with text to windowa
            self.signal.emit(str(i))
            time.sleep(1)


class WindowA(QWidget):
    signal_from_thread = pyqtSignal(str)  # signal recibe texto a cambiar

    def __init__(self) -> None:
        super().__init__()
        self.thread_1 = None  # created empty
        self.init_gui()
        self.signal_from_thread.connect(self.update_text)  # run update_text when recieving signal

    def init_gui(self):
        self.setGeometry(20, 20, 250, 250)
        self.setWindowTitle('test')

        layout_1 = QVBoxLayout()

        self.label_1 = QLabel(text="Status: Thread no ejecutado")
        self.button_1 = QPushButton(text="Ejecutar Thread")
        layout_1.addStretch(1)
        layout_1.addWidget(self.label_1)
        layout_1.addStretch(2)
        layout_1.addWidget(self.button_1)
        layout_1.addStretch(10)
        self.setLayout(layout_1)

        self.button_1.clicked.connect(self.start_thread)

    def start_thread(self):
        self.button_1.setText("Status: Thread iniciado..")

        # if it was never started clicked, or if it finished, create new thread and run
        if self.thread_1 is None or not self.thread_1.isRunning():
            self.thread_1 = MyThread(self.signal_from_thread)
            self.thread_1.start()

    # process and recieve signal from thread
    def update_text(self, text):
        self.label_1.setText(text)

```

- Ej 3 (Múltiples QThreads)
```py
class MyThread(QThread):
    def __init__(self, signal: pyqtSignal, index, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.index = index

    # runs after thread.start() is called
    def run(self) -> None:
        for i in range(10):
            # send signal with text to windowa
            self.signal.emit(self.index, str(i))
            r = random.randint(1, 3)
            time.sleep(r)
        self.signal.emit(self.index, f"Thread #{self.index} terminado.")


class WindowA(QWidget):
    signal_from_thread = pyqtSignal(int, str)  # signal recibe texto a cambiar

    def __init__(self) -> None:
        super().__init__()
        self.threads = []
        self.thread_1 = None  # created empty
        self.init_gui()
        self.signal_from_thread.connect(self.update_text)  # run update_text when recieving signal

    def init_gui(self):
        self.setGeometry(20, 20, 250, 250)
        self.setWindowTitle('test')

        layout_1 = QVBoxLayout()

        self.labels = []
        layout_1.addStretch(1)
        for i in range(4):
            label_x = QLabel(text=f"Status: Thread #{i} no ejecutado")
            layout_1.addWidget(label_x)
            self.labels.append(label_x)

        self.button_1 = QPushButton(text="Ejecutar Threads")
        # layout_1.addWidget(self.label_1)
        layout_1.addStretch(2)
        layout_1.addWidget(self.button_1)
        layout_1.addStretch(10)
        self.setLayout(layout_1)

        self.button_1.clicked.connect(self.start_thread)

    def start_thread(self):
        self.button_1.setText("Status: Thread iniciado..")

        # previene iniciar varias veces los mismos threads, o crear otros.
        for thread in self.threads:
            #if (thread is not None) or thread.isRunning():
            if thread.isRunning():
                return  # if any of the threads is alive, do not start again
        self.threads.clear()
        for i in range(4):
            thread_x = MyThread(self.signal_from_thread, i)
            thread_x.start()
            self.threads.append(thread_x)

    # process and recieve signal from thread
    def update_text(self, idx, text):
        self.labels[idx].setText(text)


```


#### QMutex
- Es la versión PyQt de los locks. Permite controlar el acceso a zonas críticas y bloquearlo para que solo ocurra en un thread.
- El objeto es `QMutex`, viene de `PyQt6.QtCore` y se usa mediante `lock()` y `unlock()`.
- Ej lock 1:
  (ejecuta un loop con lock y otro sin)
  (el loop con lock solo se ejecuta en un thread a la vez, los otros esperan a que termines)
```py
class MyThread(QThread):
    def __init__(self, signal: pyqtSignal, index, mutex: QMutex, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.index = index
        self.mutex = mutex

    # runs after thread.start() is called
    def run(self) -> None:
        self.mutex.lock()  # inicio seccion critica, solo un thread puede hacer esto a la vez
        for i in range(10):
            # send signal with text to windowa
            # with lock
            self.signal.emit(self.index, str(i) + " critico")
            r = random.randint(1, 3)
            time.sleep(r)
        self.mutex.unlock()  # fin seccion critica
        for i in range(100):
            # send signal with text to windowa
            self.signal.emit(self.index, str(i) + " no critico")
            time.sleep(0.5)
        self.signal.emit(self.index, f"Thread #{self.index} terminado.")


class WindowA(QWidget):
    signal_from_thread = pyqtSignal(int, str)  # signal recibe texto a cambiar

    def __init__(self) -> None:
        super().__init__()
        self.mutex = QMutex()  # crear lock, supongo q aqui para poder compartirlo
        self.threads = []
        self.thread_1 = None  # created empty
        self.init_gui()
        self.signal_from_thread.connect(self.update_text)  # run update_text when recieving signal

    def init_gui(self):
        self.setGeometry(20, 20, 250, 250)
        self.setWindowTitle('test')

        layout_1 = QVBoxLayout()

        self.labels = []
        layout_1.addStretch(1)
        for i in range(4):
            label_x = QLabel(text=f"Status: Thread #{i} no ejecutado")
            layout_1.addWidget(label_x)
            self.labels.append(label_x)

        self.button_1 = QPushButton(text="Ejecutar Threads")
        # layout_1.addWidget(self.label_1)
        layout_1.addStretch(2)
        layout_1.addWidget(self.button_1)
        layout_1.addStretch(10)
        self.setLayout(layout_1)

        self.button_1.clicked.connect(self.start_thread)

    def start_thread(self):
        self.button_1.setText("Status: Thread iniciado..")

        for thread in self.threads:
            #if (thread is not None) or thread.isRunning():
            if thread.isRunning():
                return  # if any of the threads is alive, do not start again
        self.threads.clear()
        for i in range(4):
            thread_x = MyThread(self.signal_from_thread, i, self.mutex)
            thread_x.start()
            self.threads.append(thread_x)

    # process and recieve signal from thread
    def update_text(self, idx, text):
        self.labels[idx].setText(text)
```

### Ejemplo QThread
- Interesante, frontend backend. revisar mejor
- ej implementacion
```py
## sin qtimer
    def run(self):
        # Mientras pueda correr
        while self.correr:
            # Me muevo y luego espero un poco de tiempo.
            self.mover()

            # Descanso los MS indicados. sleep recibe la cantidad en segundos
            # por lo tanto, debemos dividir por 1000 para transformar p.TIEMPO_MOVIMIENTO
            # en segundos
            time.sleep(p.TIEMPO_MOVIMIENTO / 1000)

## con qtimer
    self.timer_movimiento = QTimer(self)
    self.timer_movimiento.timeout.connect(self.mover)
    self.timer_movimiento.setInterval(p.TIEMPO_MOVIMIENTO)
    ..
    def mover(self):
      ...

    def start(self):
        self.timer_movimiento.start()
```

## QTimer

### QTimer
- Se puede crear concurrencia via `QTimer`. Esto no es similar al `Timer` de `threading`. Timer permite ejecutar una subrutina una vez despues de untiempo.
- **QTimer**, ejecuta codigo cada cierto tiempo periodico y se repite.
- El mismo comportamiento se puede simular con un QThread:
```python
def run(self):
    while True:
        # Lo que quiero que el QThread haga en cada iteración
        time.sleep(self.tiempo)
```
- La desventaja de usar un Thread es que esto se ejecutaria indefinidamente y obligaria a usar `terminate()`, lo que es **mala practica**.
- `QTimer` si tiene metodos para terminar de buena manera
- `start()` inicia, `stop()` detiene
- Luego de iniciar un QTimer, se asigna el tiempo entre ejecuciones con `setInterval(ms)`
- La señal timeout se conecta al codigo que se ejecutara constantemente `timer.timeout.connect(funcion)`

- Ej 1 (Reloj) (copy paste):
```py

class RelojDigital(QWidget):
    def __init__(self):
        super().__init__()

        # Crear label encargado de mostrar la hora
        self.label_timer = QLabel()
        self.label_timer.setFont(QFont("Times", 50))

        # Crear layout vertical para nuestro label
        layout = QVBoxLayout()
        layout.addWidget(self.label_timer)
        self.setLayout(layout)

        # Crear nuestro QTimer encargado de actualizar el tiempo cada 1 segundo
        timer = QTimer(self)
        timer.timeout.connect(self.mostrar_hora)
        timer.setInterval(1000)
        timer.start()

        # Definir título y tamaño ventana
        self.setWindowTitle("Reloj Digital con QTimer")
        self.setGeometry(100, 100, 250, 100)

        # Ejecutar el método para mostrar hora por primera vez
        self.mostrar_hora()

        # Mostrar ventana
        self.show()

    def mostrar_hora(self):
        # Obtener hora actual
        hora_actual = datetime.datetime.now().time()
        # Actualizar texto del label
        self.label_timer.setText(hora_actual.strftime("%H:%M:%S %p"))
```


- Ej 2 (Multiples QTimer, ej anteriores pero con QTimer)
- TODO: revisar, deberia estar bien y equivalente a ejemplo multiple pero con qtimer
```py
class MyTimer(QObject):
    def __init__(self, signal: pyqtSignal, index, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.index = index
        self.idx_counter = 0 # counter

        self.timer = QTimer(self)
        self.timer.setInterval(2000) # set interval for each iteraiton
        self.timer.timeout.connect(self.run_code) # what code is executed

    # runs after thread.start() is called
    # def run(self) -> None:
    #     for i in range(10):
    #         # send signal with text to windowa
    #         self.signal.emit(self.index, str(i))
    #         r = random.randint(1, 3)
    #         time.sleep(r)
    #     self.signal.emit(self.index, f"Thread #{self.index} terminado.")

    def run_code(self):
        # replace for here
        if self.idx_counter < 10: # for loop
            self.signal.emit(self.index, str(self.idx_counter)) # emit
            self.idx_counter += 1 # increase
        else: # end loop. finished and stop timer
            self.signal.emit(self.index, f"Timer #{self.index} terminado.")
            self.timer.stop()  # ends the timer


class WindowA(QWidget):
    signal_from_thread = pyqtSignal(int, str)  # signal recibe texto a cambiar

    def __init__(self) -> None:
        super().__init__()
        self.timers = []
        self.init_gui()
        self.signal_from_thread.connect(self.update_text)  # run update_text when recieving signal

    def init_gui(self):
        self.setGeometry(20, 20, 250, 250)
        self.setWindowTitle('test')

        layout_1 = QVBoxLayout()

        self.labels = []
        layout_1.addStretch(1)
        for i in range(4):
            label_x = QLabel(text=f"Status: Timer #{i} no ejecutado")
            layout_1.addWidget(label_x)
            self.labels.append(label_x)

        self.button_1 = QPushButton(text="Ejecutar Timers")
        # layout_1.addWidget(self.label_1)
        layout_1.addStretch(2)
        layout_1.addWidget(self.button_1)
        layout_1.addStretch(10)
        self.setLayout(layout_1)

        self.button_1.clicked.connect(self.start_thread)

    def start_thread(self):
        self.button_1.setText("Status: Timer iniciado..")

        for timer in self.timers:
            # accesses the QTimer object of MyTimer 
            if timer.timer.isActive(): # if any timer is running, do not start again
                return  #
        self.timers.clear()
        for i in range(4):
            timer_x = MyTimer(self.signal_from_thread, i)
            # accesses the QTimer object of MyTimer
            timer_x.timer.start()
            self.timers.append(timer_x)

    # process and recieve signal from thread
    def update_text(self, idx, text):
        self.labels[idx].setText(text)

```

#### singleShot
- Si queremos que el QTimer se ejecute **solo una vez**, se usa `timer.setSingleShot(true)`


### Ejemplo QTimer
- mismo ejemplo de antes, no revisar tanto

## Otros
### QThreads y señales

### *isAutoRepeat* de *keyPressEvent*
- Como parte del keyPressEvent, queremos saber si la tecla se ha mantenido apretada para cambiar el comportamiento.
- `event.isAutoRepeat()` retorna True si la tecla se mantiene apretada
- Ej:
```py
    def keyPressEvent(self, evento):
        if event.key() == Qt.Key.Key_W: # esto pasa siempre
            self.contador_w += 1
            self.label_w_contador.setText(f"Presionada {self.contador_w} veces")
        ## esto solo pasa si son clics en la tecla separadas.
        if event.key() == Qt.Key.Key_A and not event.isAutoRepeat():
            self.contador_a += 1
            self.label_a_contador.setText(f"Presionada {self.contador_a} veces")
```

### Sonidos en PyQT

#### QMediaPlayer
- Permite reproducir `.mp3`
- Para hacerlo, se instancia el objeto.
- se llama a objeto_media_player.setAudioOutput(QAudioOutput(self))
- Se crea un objeto QURL
- Se pasa el objeto a media_player.setSource()
- Se usa play()
- codigo
```py
self.media_player_mp3 = QMediaPlayer(self)
self.media_player_mp3.setAudioOutput(QAudioOutput(self))
file_url = QUrl.fromLocalFile(join("sounds", "waku-waku.mp3"))
self.media_player_mp3.setSource(file_url)
self.media_player_mp3.play()

```


#### QSoundEffect
- Permite reproducir `.wav`
- codigo
```py
self.media_player_wav = QSoundEffect(self)
self.media_player_wav.setVolume(0.1) # Opcional
file_url = QUrl.fromLocalFile(join("sounds", "see-you-again.wav"))
self.media_player_wav.setSource(file_url)
if not self.media_player_wav.isPlaying():
   self.media_player_wav.play()
```


- Ej 1:
- pendiente



## MainWindow

### MainWindow
- PyQt tiene un tipo de ventana especial llamada `MainWindow`. Incluye el esqueleto basico de una aplicacion: barra de estado, barra de herramientas y de menu.
- Docs: https://doc.qt.io/qt-6/mainwindow.html
![](@attachment/Clipboard_2023-09-21-00-55-51.png)
- TODO: terminar



