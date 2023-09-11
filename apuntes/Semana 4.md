---
attachments: [Clipboard_2023-09-10-16-44-05.png, Clipboard_2023-09-10-17-20-59.png, Clipboard_2023-09-10-17-33-32.png, Clipboard_2023-09-10-18-07-26.png, Clipboard_2023-09-10-19-13-29.png, Clipboard_2023-09-10-19-30-32.png, Clipboard_2023-09-10-21-48-19.png, Clipboard_2023-09-11-15-34-22.png]
tags: [prog-avanzada]
title: Semana 4
created: '2023-09-01T20:24:01.273Z'
modified: '2023-09-11T22:33:01.055Z'
---

# Semana 4

## Interfaces gráficas
- Creación de GUIs
- La idea es pasar de una arquitectura de *polling*, que se refiere a estar constantemente revisando si hay entrada del usuario vía un loop, a una arquitectura basada en **eventos**.
- Se pueden crear funciones que se hagan cargo de un evento de forma **asíncrona**, es decir no necesariamente en el flujo principal del programa.


## PyQt
### Básico
- Framework multiplataforma para interfaces gráficas.
- Documentación: https://www.riverbankcomputing.com/static/Docs/PyQt6/introduction.html#pyqt6-components
- Módulos principales: 
  - QtWidgets: elementos básicos de GUIS
  - QtCore: manejo de threads, archivos, y otras funcionalidades no GUI
  - QtGui: componentes de integración de ventanas, manejo de eventos y otros
  - QtNetwork: permite comunicacion con sockets
  - QTSql: uso de sql
  - otros...


### Creación de una ventana
- Se debe crear una `QApplication` (existe una sola por aplicacion). Se inicializa como `QApplication([])` ya que no recibe parametros por CLI.
- La `QApplication` contiene el main loop y maneja el iniciado y cierre de widgets.
- Se crea un `QWidget` para crear la ventana en si. Esta representa un elemento grafico, puede recibir eventos y representarse en pantalla. Es la clase base de todos los objetos de la interfaz.
- Nota: un `QWidget` puede ser una ventana o un elemento dentro de una ventana. SI no tiene padre se considera una ventana. Para los widgets que son padres, existe  setWindowTitle() y setWindowIcon().
![](@attachment/Clipboard_2023-09-10-16-44-05.png)
- También se pueden usar widgets de layout para ordenar el contenido de una ventana! https://doc.qt.io/qt-6/layout.html
- Docs de Widget: https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html
- Ej:
```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget


class MyWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()  # passing no parents and no flags

        # x e y parten con 0,0 arriba a la izquierda
        # x, y, width, height
        # ventana 360x100, 150 hacia la derecha, 500 hacia abajo
        self.setGeometry(150, 500, 360, 100)
        self.setWindowTitle('Ventana de prueba')


if __name__ == "__main__":
    app = QApplication([])  # create app instance
    main_window = MyWindow()  # instance window without parent
    main_window.show()  # show the window
    exit_code = app.exec()  # execute the app main loop
    sys.exit(exit_code)  # pass the exit code from execution to system

```

### Debuggeo
- Código que podría servir para debugear.
```py
if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QtWidgets.QApplication([])
    ventana = MiVentana(*args)
    ventana.show()
    sys.exit(app.exec())
```

### Elementos gráficos básicos
#### Sistema coordenado
- El sistema coordenado de Qt parte desde la esquina superior izquierda, ej:
```py
# ventana 300x300, 200 hacia la derecha X, 100 hacia abajo Y
self.setGeometry(200, 100, 300, 300)
```
![](@attachment/Clipboard_2023-09-10-17-20-59.png)
#### Etiquetas y cuadros de texto
- Para etiquetas `QLabel` y para cuadros de texto `QLineEdit`.

- QLabel
  - https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qlabel.html
  ![](@attachment/Clipboard_2023-09-10-17-33-32.png)
  - Use `setText()` to set text. `setAlignment()` to set alignment.

- QLineEdit
  - https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qlineedit.html
  ![](@attachment/Clipboard_2023-09-10-18-07-26.png)
  - Texto editable de una línea
  - Change text with `setText()`. Get user text with `text()`


- Ej:
```py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit


class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 380, 240)
        self.setWindowTitle('Ventana de prueba2')

        self.create_gui()

    def create_gui(self) -> None:
        self.text_1 = QLabel("Escribe aquí:", self)  # the parent is passed, MyWindow in this case
        self.text_1.move(10, 10)  # now it is located at 10, 10 inside the window

        self.input_1 = QTextEdit("Hint de texto", self)  # can also use ""
        # self.input_1.move(10, 50)
        self.input_1.setGeometry(100, 10, 250, 20)  # it is located at 100, 10 in the window, and it is 250x20

        self.text_2 = QLabel('Texto abajo', self)
        self.text_2.move(10, 50)  # moved below the text_1, at 10,50.

        self.show()  # shows the elements of the window


if __name__ == "__main__":
    app = QApplication([])  # create app instance
    main_window = MyWindow()  # instance window without parent
    main_window.show()  # show the window
    exit_code = app.exec()  # execute the app
    sys.exit(exit_code)  # pass the exit code from execution to system

```
#### Imágenes
- Se pueden cargar imagenes en una ventana mediante QPixMap del modulo QTGui. Se carga dentro de un QLabeol.
- Ej:
```py
class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 500, 320) # size 500x320 in pos 100, 200
        self.setWindowTitle('Ventana de prueba2')

        self.create_gui()

    def create_gui(self) -> None:
        self.label_1 = QLabel("", self)
        pixmap_obj = QPixmap(os.path.join('..', 'scripts', 'img', 'python.jpg'))
        self.label_1.setPixmap(pixmap_obj)
        
        self.label_1.setGeometry(100, 10, 300, 300) # set size 300x300, in pos 100,10 # centered

        self.show()  # shows the elements of the window

```


#### Botones
- Se pueden crear via el widget `QPushButton`
- Emiten la señal `clicked()`, `pressed()` y `released()`. 
- Tambíen puede mostrar un icono con `setIcon()`
- Use the method setMenu() to associate a popup menu with a push button.
- Ej:
```py
class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setWindowTitle('Ventana de prueba2')

        self.create_gui()

    def create_gui(self) -> None:
        # Creates a group of labels for convenience
        self.labels = {}  # dict
        self.labels["label1"] = QLabel("Texto:", self)
        self.labels["label1"].move(10, 10)

        self.labels["label2"] = QLabel("Aqui se escribe la respuesta", self)
        self.labels["label2"].move(10, 40)

        self.input_1 = QLineEdit('', self)
        self.input_1.setGeometry(80, 10, 200, 20) # at 80, 10. size 200x20

        # investigar para que sirve el & en los textos.
        self.submit_button = QPushButton("&Procesar", self)
        self.submit_button.move(10, 60)
        self.submit_button.resize(self.submit_button.sizeHint())  # modifies the size only, not the position
        # self.x.sizeHint() returns the recommended size for the content

        self.show()  # shows the elements of the window

```

#### Layouts
- Los layouts permiten manejar la distribucion de los widgets en una ventana, sin usar setGeometry y move.
- Permiten que funcione bien en distintos tamaños de pantalla y que los objetos permanezcan en su posicion con cambios de tamaño de la pestaña.
- Se añaden los objetos a cada layout via `addWidget(widget)`.
- El layout se debe cargar a la ventana via `self.setLayout()`
- Se puede colocar un layout dentro de otro.
- Interesante: https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qboxlayout.html
- TODO: averiguar mas sobre stretch y spacing
![](@attachment/Clipboard_2023-09-10-19-13-29.png)
- Ej (revisar):
  ![](@attachment/Clipboard_2023-09-10-19-30-32.png)
  ```py
  class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 400, 400)
        self.setWindowTitle('Ventana con boton')

        self.create_gui()

    def create_gui(self) -> None:
        self.label_1 = QLabel('Texto:', self)
        self.input_1 = QLineEdit('', self)
        self.input_1.resize(100, 20)
        self.button_1 = QPushButton("&Submit", self)
        self.button_1.resize(self.button_1.sizeHint())

        horizontal_box = QHBoxLayout()
        horizontal_box.addStretch(1) # space to the left
        horizontal_box.addWidget(self.label_1)
        horizontal_box.addWidget(self.input_1)
        horizontal_box.addWidget(self.button_1)
        horizontal_box.addStretch(1)  # space to the right

        vertical_box = QVBoxLayout()
        vertical_box.addStretch(1)  # moves it downwards
        vertical_box.addLayout(horizontal_box)
        vertical_box.addStretch(5)  # prevents it from going too low

        self.setLayout(vertical_box)  # set window layout to vertical
        self.show()  # shows the elements of the window
  ```




##### Grid layout `QGridLayout()`
- TODO: revisar de nuevo
- El grid layout permite colocar items en una grilla, con posiciones i, j.
- uso: `grilla.addWidget(widget, i, j)`
- Ej: Calculadora
  ![](@attachment/Clipboard_2023-09-10-21-48-19.png)
```py
class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setWindowTitle('Calculator')

        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.label_1 = QLabel('Status:', self)
        self.label_1.resize(self.label_1.sizeHint())
        self.vertical_l_1 = QVBoxLayout()

        self.grid_layout = QGridLayout()
        # create number buttons
        self.buttons = [["1", "2", "3"],
                        ["4", "5", "6"],
                        ["7", "8", "9"],
                        ["CE", "0", "C"]]

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                new_button = QPushButton(self.buttons[i][j], self)
                self.grid_layout.addWidget(new_button, i, j)

        self.vertical_l_1.addStretch(15)
        self.vertical_l_1.addWidget(self.label_1)
        self.vertical_l_1.addStretch(2)
        self.vertical_l_1.addLayout(self.grid_layout)
        self.vertical_l_1.addStretch(15)

        self.setLayout(self.vertical_l_1)

```

#### Creación de Widgets con POO
- Se pueden crear *widgets* con funcionalidades adicionales, si creamos nuestra propia clase de objeto.
- Ej 1 (Boton contador):
  ```py
  class BotonContador(QPushButton):
    def __init__(self, nombre, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.move(*pos)  # sacar argumentos i, j
        self.resize(self.sizeHint())
        self.counter = 0

        self.clicked.connect(self.count)  # connected clicked() signal to count()

    def count(self):
        self.counter += 1
        print(f'El boton {self.nombre} contó {self.counter} clicks')


class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setMaximumSize(300, 400)
        self.setWindowTitle('Calculator')

        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.ct_button_1 = BotonContador("Boton 1", (10, 20), "Clickeame 1", self)
        self.ct_button_1 = BotonContador("Boton 2", (10, 60), "Clickeame 2", self)

  ```
- Ej 2 (Campo de formulario reutilizable):
  ```py
  class FormField(QHBoxLayout):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)  # hereda de QHBoxLayout
        label_1 = QLabel(text)
        label_1.resize(label_1.sizeHint())
        field_1 = QLineEdit('')
        # field_1.setBaseSize(100, 20)

        self.addWidget(label_1)
        self.addStretch(2)
        self.addWidget(field_1)
        # crea un campo con un texto label y al lado un campo de 1 linea


class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setMaximumSize(300, 400)
        self.setWindowTitle('form')

        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        layout_v_1 = QVBoxLayout()
        # crea objetos custom
        layout_v_1.addLayout(FormField("Nombre"))
        layout_v_1.addLayout(FormField("Apellido"))
        layout_v_1.addLayout(FormField("Dirección"))
        layout_v_1.addLayout(FormField("Correo"))
        layout_v_1.addLayout(FormField("Usuario"))
        layout_v_1.addLayout(FormField("Contraseña"))

        self.setLayout(layout_v_1)

  ```
### Eventos y Señales

#### Intro
- Son parte clave de nuestra **arquitectura basada en manejo de eventos**. Se detectan eventos generados por el usuario o la misma app y se procesan por el elemento apropiado.
- PyQt empieza a detectar eventos al entrar al mainloop, es decir al llamar a exec de la QApplication.
- ![](@attachment/Clipboard_2023-09-11-15-34-22.png)
- Existen 3 elementos fundamentales:
  - Fuente del evento: Objeto que genera cambio de estado o genera el evento
  - Objeto evento: encapsula el cambio de estado mediante el evento
  - Objeto destino: Objeto al que se le notifica el cambio de estado

- En este modelo, la **fuente del evento delega la tarea de manejo al objeto destino**, pasando el *objeto evento*.
- PyQt tiene un sistema de *signal* y *slot*. Al ocurrir un evento, el objeto activado activa una señal, al slot correspondiente. El slot puede ser cualquier elemento callable de Python. (funcion por ejemplo)


- Ej 1: extension calculadora: (Se conectan el evento clicked a un slot)
  ```py
  class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setWindowTitle('Calculator')

        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.label_1 = QLabel('Status:', self)
        self.label_1.resize(self.label_1.sizeHint())
        self.vertical_l_1 = QVBoxLayout()

        self.grid_layout = QGridLayout()
        # create number buttons
        self.buttons = [["1", "2", "3"],
                        ["4", "5", "6"],
                        ["7", "8", "9"],
                        ["CE", "0", "C"]]

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                new_button = QPushButton(self.buttons[i][j], self)
                new_button.clicked.connect(self.clicked_button)  # connects clicked() signal to self.clicked_button slot

                self.grid_layout.addWidget(new_button, i, j)

        self.vertical_l_1.addStretch(15)
        self.vertical_l_1.addWidget(self.label_1)
        self.vertical_l_1.addStretch(2)
        self.vertical_l_1.addLayout(self.grid_layout)
        self.vertical_l_1.addStretch(15)

        self.setLayout(self.vertical_l_1)

    def clicked_button(self):
        button = self.sender() # obtains origin object (QPushButton)
        idx = self.grid_layout.indexOf(button)  # from QLayout, gets id of button, starting from 0
        # row, column, rowSpan, columnSpan
        position = self.grid_layout.getItemPosition(idx)  # passed idx, returns position
        self.label_1.setText(f'Status: Boton {idx} apretado en pos {position[:2]}')

  ```
#### Obteniendo sender
- Para obtener una referencia al objeto que envio una señal, se usa la función `sender()` dentro de la función que maneja el evento.
- Ej (Botones con distintos listeners):
  ```py
  class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 200, 300, 400)
        self.setWindowTitle('Calculator')

        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.label_1 = QLabel('Status:', self)
        self.label_1.resize(self.label_1.sizeHint())
        self.vertical_l_1 = QVBoxLayout()

        self.horizontal_l_1 = QHBoxLayout()
        self.button_1 = QPushButton('&Boton 1', self)
        self.button_1.resize(self.button_1.sizeHint())
        self.button_1.clicked.connect(self.clicked_button)
        self.button_2 = QPushButton('&Boton 2', self)
        self.button_2.resize(self.button_2.sizeHint())
        self.button_2.clicked.connect(self.clicked_button)

        # los botones 1 y 2 llaman a clicked_button

        self.button_3 = QPushButton('&Salir', self)
        self.button_3.resize(self.button_3.sizeHint())
        self.button_3.clicked.connect(QCoreApplication.instance().quit)  # envia signal de quit() a instance
        # el boton 3 llama al slot quit de la instancia

        self.horizontal_l_1.addStretch(1)
        self.horizontal_l_1.addWidget(self.button_1)
        self.horizontal_l_1.addWidget(self.button_2)
        self.horizontal_l_1.addWidget(self.button_3)
        self.horizontal_l_1.addStretch(1)

        self.vertical_l_1.addStretch(15)
        self.vertical_l_1.addWidget(self.label_1)
        self.vertical_l_1.addStretch(2)
        self.vertical_l_1.addLayout(self.horizontal_l_1)
        self.vertical_l_1.addStretch(15)

        self.setLayout(self.vertical_l_1)

    def clicked_button(self):
        button = self.sender()  # obtains origin object
        self.label_1.setText(f'Status: Boton {button.text()} apretado')

  ```

#### Eventos de mouse y move event
- Se puede sobreescribir el mousePressEvent, mouseReleaseEvent y mouseMoveEvent de un QWidget, creando una funcion de forma event(self, event).

- Ej 1: Trackeo de clicks y posicion mientras este clickeado
  ```py
  class MyWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 100, 110, 400)
        self.create_gui()
        self.show()

    def create_gui(self) -> None:

        self.label = QLabel("Haz clic en mí", self)
        self.label.setGeometry(10, 10, 90, 100)
        self.label.setStyleSheet("background-color: lightblue;")
        self.label.show()
        self.click_dentro_del_label = False # track prev state
  
    def mousePressEvent(self, event) -> None:
        # event.position() returns QPoint()
        print(f'Se presiono el mouse en {event.position().x()}, {event.position().y()}')
        if self.label.underMouse():  # if the label is under mouse
            print('El mouse se apreto dentro del label')
            self.click_dentro_del_label = True
        else:
            print('El mouse se apreto fuera del label')
            self.click_dentro_del_label = False

    def mouseReleaseEvent(self, event) -> None:
        # event.position() returns QPoint()
        print(f'Se solto el mouse en {event.position().x()}, {event.position().y()}')
        if (self.click_dentro_del_label):
            print('Antes el mouse se apreto dentro del label')
        else:
            print('Antes el mouse se apreto fuera del label')

    def mouseMoveEvent(self, event) -> None:
        # event.position() returns QPoint()
        print(f'El mouse se mueve, pos: {event.position().x()}, {event.position().y()}')

  ```
- Ej 2: Trigger permanente de move event (no relevante) 
```py
  import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 110, 400)
        self.label = QLabel("Haz clic en mí", self)
        self.label.setGeometry(10, 90, 90, 100)
        self.label.setStyleSheet("background-color: lightblue;")
        self.label.show()
        self.click_dentro_del_label = False

        self.setMouseTracking(True)  # Activamos el tracking en nuestra ventana

        # Descomentar la siguiente línea si queremos seguir el mouse cuando estamos sobre el label
        # self.label.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        print(f"El mouse se mueve... está en {x},{y}")
```

#### Eventos de teclado
- Se pueden manejar usando el keyPressEvent
- TODO: investigar mas
- Ej generico:
```py
    def keyPressEvent(self, event) -> None:
        # event.text() para texto y event.key() en codigo
        # por ejemplo, las teclas especiales solo tienen key()
        self.etiqueta.setText(f'Se presiono la tecla {event.text()} de codigo {event.key()}')
        self.etiqueta.resize(self.etiqueta.sizeHint())

```
#### Crear señales custom
- Se pueden crear señales personalizadas
- Par hacer esto, se debe alojar la señal en un objeto que herede de `QtCore.Qobject`.
- Dentro de la subclase se crea una señal, que es instancia de QTCore.pyqtSignal.
- Luego se reciben y se conectan señales.
- El metodo emit permite emitir la señal
- El metodo connect permite definir la funcion a ejecutar acuando la señal es emitida.
- Ej simple señal entre 2 ventanas:
```py
class ClickableWindow(QWidget):
    edit_signal = pyqtSignal()  # creates signal

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Ventana clickeable')
        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.label = QLabel('Clickea esta ventana', self)
        self.label.resize(self.label.sizeHint())

    def mousePressEvent(self, event) -> None:
        # why self if it is static?
        self.edit_signal.emit()  # EMIT SIGNAL without args


class EditedWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(400, 300, 300, 200)
        self.setWindowTitle('Ventana editable')
        self.create_gui()
        self.show()

    def create_gui(self):
        self.label1 = QLabel('', self)  # label vacia, despues se edit

    def edit_label(self):
        self.label1.setText('Se apreto la otra ventana')
        self.label1.resize(self.label1.sizeHint())


if __name__ == "__main__":
    app = QApplication([])  # create app instance
    clickable_window = ClickableWindow()  # instance window without parent
    edited_window = EditedWindow()

    # connects edit_signal of clickable window to edited window edit_label function (slot)
    # CONNECT SIGNAL TO SLOT
    clickable_window.edit_signal.connect(edited_window.edit_label)

    # main_window.show()  # show the window
    exit_code = app.exec()  # execute the app
    sys.exit(exit_code)  # pass the exit code from execution to system

```
#### Emitir eventos con información
- Ej emision de señal entre ventanas:
```py
class ClickableWindow(QWidget):
    edit_signal = pyqtSignal()  # CREATE SIGNAL
    text_signal = pyqtSignal(str)  # SIGNAL THAT PASSES STR
    pos_signal = pyqtSignal(int, int)  # SIGNAL TO PASS X, Y

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # passing no parents and no flags

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Ventana clickeable')
        self.setMouseTracking(True)  # el movemouseevent siempre activo
        self.create_gui()
        self.show()

    def create_gui(self) -> None:
        self.label = QLabel('Clickea esta ventana', self)
        self.label.resize(self.label.sizeHint())

        self.text_edit = QLineEdit('', self)  # vacio

    def mousePressEvent(self, event) -> None:
        self.edit_signal.emit()  # emit signal without args, will edit the other window
        self.text_signal.emit(self.text_edit.text())  # emit signal with the text in the label

    def mouseMoveEvent(self, event) -> None:
        # EMIT SIGNAL WITH COORDS
        self.pos_signal.emit(event.pos().x(), event.pos().y())


class EditedWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(400, 300, 300, 200)
        self.setWindowTitle('Ventana editable')
        self.create_gui()
        self.show()

    def create_gui(self):
        self.layout_v = QVBoxLayout()

        self.label1 = QLabel('', self)  # label vacia, despues se edit
        self.label2 = QLabel('', self)  # for text passed
        self.label3 = QLabel('', self)  # for position passed
        self.layout_v.addWidget(self.label1)
        self.layout_v.addWidget(self.label2)
        self.layout_v.addWidget(self.label3)
        self.setLayout(self.layout_v)

    # recieves signal w no args
    def edit_label(self):
        self.label1.setText('Se apreto la otra ventana')
        self.label1.resize(self.label1.sizeHint())

    # recieves text via the text_signal(str)
    def edit_label_text(self, text):
        self.label2.setText(f'Texto: {text}')
        self.label2.resize(self.label2.sizeHint())

    # recieves the new pos x, y via pos_signal(int, int)
    def edit_label_pos(self, x, y):
        self.label3.setText(f'Pos: {x}, {y}')
        self.label3.resize(self.label3.sizeHint())


if __name__ == "__main__":
    app = QApplication([])  # create app instance
    clickable_window = ClickableWindow()  # instance window without parent
    edited_window = EditedWindow()

    # connects edit_signal of clickable window to edited window edit_label function
    clickable_window.edit_signal.connect(edited_window.edit_label)
    clickable_window.text_signal.connect(edited_window.edit_label_text)
    clickable_window.pos_signal.connect(edited_window.edit_label_pos)

    # main_window.show()  # show the window
    exit_code = app.exec()  # execute the app
    sys.exit(exit_code)  # pass the exit code from execution to system

```

### Diseño frontend y backend
- Es recomendable separar el frontend y el backend de los programas.
- Es decir, separar la GUI de la logica detras de esta.
- Se debe cumplir con un programa de **alta cohesión** y **bajo acoplamiento**.
  - Cohesión: Cada componente del software debe realizar solo tareas relacionadas con este. Ej: Un `Restaurant` debe tener funciones como `abrir_restaurant()`, pero no `servir_platos()`, ya que esto debe ser manejado por un objeto distinto, por ejemplo `Mesero`.
  - Acoplamiento: Se refiere a que la modificación de un componente implica modificar otro componente para que funcione. Ejemplo: modificar clase a implica modificar clase b. Se debe reducir. 

- Ejemplo de programa bien hecho (alta cohesion y bajo acoplamiento):
  - El procesamiento de datos y el comportamiento de la ventana principal esta separado.
  - Se usan señales backend>frontend y viceversa para evitar llamado directo de objetos de distintos componentes.
  - senal_procesar (frontend) > procesar_input (backend)
  - senal_actualizar (backend) > actualizar_resultado (frontend)
  - al final cambio pero xd
  - Backend (Procesador):
```py
import typing
from PyQt6.QtCore import QObject, pyqtSignal


class Procesador(QObject):
    update_text_signal = pyqtSignal(str)  # signal to pass new text to ui

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def is_valid(self, text: str) -> bool:
        for c in text:
            if not (c.isnumeric() or c == ','):
                return False
        return True

    def text_to_list(self, text: str) -> list:
        return text.strip('').split(',')

    def sort(self, list_edit: list):
        list_edit.sort(key=lambda element: int(element))

    def list_to_text(self, curr_list: list) -> str:
        return ",".join(curr_list)

    # recieves a signal from frontend with text
    def process_input(self, input: str) -> None:
        print(f'backend process_input(): {input}')
        if self.is_valid(input):
            new_list = self.text_to_list(input)
            self.sort(new_list)
            new_text = self.list_to_text(new_list)
            self.update_ui(new_text)

    # emits signal and updates frontend
    def update_ui(self, text: str):
        print(f'update_ui() emits: {text}')
        self.update_text_signal.emit(text)

```
  - Frontend:
```py
import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

from backend import Procesador


class MainWindow(QWidget):
    pass_data_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(400, 300, 300, 400)
        self.setWindowTitle('Ventana')
        self.create_gui()
        self.show()

    def create_gui(self):
        self.layout_v = QVBoxLayout()

        self.label1 = QLabel('Ingresa una lista de números:', self)  # label vacia, despues se edit
        self.edit_label_1 = QLineEdit('Ej: 1, 2, 3', self)
        self.button_1 = QPushButton('Ordenar', self)
        self.label2 = QLabel('Result: ', self)  # for position passed
        self.label2.hide()
        self.layout_v.addWidget(self.label1)
        self.layout_v.addWidget(self.edit_label_1)
        self.layout_v.addWidget(self.button_1)
        self.layout_v.addWidget(self.label2)
        self.setLayout(self.layout_v)

        self.button_1.clicked.connect(self.clicked_button)  # calls the clicked_button slot
        # no se puede hacer directo?
        #self.button_1.clicked(self.pass_data_signal.emit(self.edit_label_1.text()))

    def clicked_button(self):
        print(f'clicked_button(), {self.edit_label_1.text()}')
        self.pass_data_signal.emit(self.edit_label_1.text())  # emit signal and pass the test in the edit area

    # called via backend emitted signal
    def update_text_label(self, new_text: str):
        print(f'update_text_label() recieved {new_text}')
        self.label2.setText(new_text)
        self.label2.show()


if __name__ == "__main__":
    app = QApplication([])  # create app instance
    main_window = MainWindow()

    # connect signals

    # connect frontend signal to backend and call update_ui
    proc = Procesador()
    main_window.pass_data_signal.connect(proc.process_input)

    # connect backend signal to frontend and call update_text_label
    proc.update_text_signal.connect(main_window.update_text_label)

    exit_code = app.exec()  # execute the app
    sys.exit(exit_code)  # pass the exit code from execution to system

```

### Ejemplo de conexion entre ventanas
- TODO

### Propuestos
- TODO: a


