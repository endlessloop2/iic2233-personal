---
tags: [prog-avanzada]
title: Semana 6
created: '2023-09-20T01:50:44.607Z'
modified: '2023-09-20T04:48:29.783Z'
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
- hecho pero wip
```py


```


#### QMutex


### Ejemplo QThread


## QTimer

### QTimer


### Ejemplo QTimer

## Otros
### QThreads y señales

### a

### b



## MainWindow


