---
attachments: [Clipboard_2023-08-23-22-56-03.png, Clipboard_2023-08-23-23-00-22.png, Clipboard_2023-08-24-01-02-10.png, Clipboard_2023-08-24-01-05-55.png, Clipboard_2023-08-24-01-10-37.png, Clipboard_2023-08-24-01-11-05.png]
tags: [prog-avanzada]
title: Semana 2
created: '2023-08-23T02:16:55.058Z'
modified: '2023-08-24T05:11:05.429Z'
---

# Semana 2

## Herencia
- Corresponde a especializacion y generalizacion entre clases. Una clase hereda atributos y metodos de otra clase.
- La clase que hereda se conoce como *subclase*, y hereda desde una *superclase*.
- Una subclase tiene todos los elementos de la superclase, pero puede tener adicionales.

### Uso
- No se hace nada en la clase padre.
- La subclase se debe inicializar de la siguiente forma:
```py
class Padre:
  def __init__(self, a, b):
    pass

## Se pasa la clase Padre cómo parametro
class SubClase(Padre):
  def __init__(self, a, b):
    # Se llama al constructor de la clase padre con sus párametros.
    Padre.__init__(self, a, b)
```


### Ejemplo 1:
```py
class Animal:
  def __init__(self, tipo, nivel_alimento, nivel_agua):
    self.tipo = tipo
    self._nivel_alimento = nivel_alimento
    self._nivel_agua = nivel_agua
  
  ## si no tuviera tipo_alimento seria overloading no overriding
  def alimentar(self, alimento, tipo_alimento):
    self._nivel_alimento += max(0, alimento)
  
  def comprobar_alimento(self):
    return self._nivel_alimento

  def comprobar_agua(self):
    return self._nivel_agua

class Mono(Animal):
  # Esta clase hereda de Animal, por lo que contiene sus atributos y metodos
  
  def __init__(self, tipo, nivel_alimento, nivel_agua):
    ## ojo, hicimos override del init original, por eso hay que llamarlo
    Animal.__init__(tipo, nivel_alimento, nivel_agua)
    self._arboles_trepados = []
  
  def trepar_arbol(self, tipo_arbol):
    if tipo_arbol not in self.arboles_trepados:
      self.arboles_trepados.append(tipo_arbol)
  
  ## OVERRIDING
  ## Sobreescribe un metodo de una superclase
  def alimentar(self, alimento, tipo_alimento):
    if tipo_alimento == "banana":
      self._nivel_alimento += alimento
    else:
      print(f"Mono: no come {tipo_alimento}")

```

### Uso de super()
- Es buena práctica y permite multiherencia.
- Se usa `super().__init__()` en vez de `ClaseA.__init__()`
- Ejemplo:
```py
class Padre:
  def __init__(self, a, b):
    pass

## Se pasa la clase Padre cómo parametro
class SubClase(Padre):
  def __init__(self, a, b):
    # Se llama al constructor de la clase Padre, buscada por super()
    super().__init__(self, a, b)
```



### Modificando clases *built-in*
- Se puede agregar funcionalidades a clases, por ejemplo a list.
- Ojo, para hacer una busqueda dentro de una lista por ejemplo, se puede usar
```py
for objeto in self:
  pass
## busca dentro de si misma, siendo self una list
```

#### Ejemplo oficial (pendiente hacer uno)
```py
class ContactList(list):
    """
    Estamos extendiendo y especializando la clase list estándar. 
    Tiene todos los métodos de la lista más los definidos por nosotros.
    """
    
    # Buscar es un método específico de esta sub-clase
    def buscar(self, nombre):
        matches = []
        for contacto in self:
            if nombre in contacto.nombre:
                matches.append(contacto)
        return matches

    
class Contacto:
    """La clase Contacto almacena nombre y correo electrónico."""
    
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email


class Familiar(Contacto):
    """Familiar es una clase especializada de Contacto que permite incluir el tipo de relación"""

    # Overriding sobre el método __init__()
    def __init__(self, nombre, email, relacion):
        super().__init__(nombre, email)
        self.relacion = relacion
```

## Polimorfismo
- Revisar bien concepto.
- Formalmente, se refiere a "la propiedad por la que es posible enviar mensajes sintácticamente iguales a objetos de tipos distintos".
- Se refiere a usar objetos de distinto tipo con la misma *interfaz*
- Interfaz: Es algo parecido a las clases abstractas??
- Interfaz: Clase con métodos abstractos y propiedades constantes
- Sería como la definición de una clase sin su implementación completa.
- Se puede hacer overriding y overloading
- **Overriding**: Se implementa un método en una subclase, que sobreescribe la implementación de la super clase. (ej. anterior)
- **Overloading**: Se define un método con el mismo nombre pero con distinto número y tipo de argumentos. Ejecuta distintas acciones según el número y tipo de argumentos.
- Function overloading no esta soportado en Python (Definir funcion segun tipo y numero de argumento)

### Overriding
- Cada subclase tiene el mismo método, pero realiza distintas opciones
- Se invoca el mismo método sobre objetos de distinto tipo, y cada objeto lo interpreta según su definición.

- Ej oficial
```py
import statistics

class Variable:
    ## Esta sería una especie de interfaz
    ## Crea metodo y variable sin mayor implementación
    def __init__(self, data):
        self.data = data

    def representante(self):
        pass


class Ingresos(Variable):
    ## implementacion de representante() para objetos de tipo Ingresos
    def representante(self):
        return statistics.mean(self.data)


class Comunas(Variable):
    def representante(self):
        return statistics.mode(self.data)


class Puestos(Variable):
    # Ordenadas de menor a mayor
    # Este es un atributo de la clase Puestos, compartida por todas sus instancias
    # Este tipo de atributo se accede con la notación NombreDeLaClase.atributoClase
    # Por ejemplo: Puestos.categorias
    categorias = ['Alumno en Practica', 'Analista', 'SubGerente', 'Gerente']

    def representante(self):
        # Paso 1: Transformar la lista en lista de números, donde 0 es alumno en práctica y 3 gerente
        puestos = []
        for cargo in self.data:
            puestos.append(Puestos.categorias.index(cargo))
        # Paso 2: Vemos cuál es el máximo
        maximo = max(puestos)
        # Paso 3: Retornar cargo asociado
        return Puestos.categorias[maximo]
```


### Overloading
- Python no permite definir la misma función con distinto tipo o número de argumentos.
```py
def funcion(arg):
    print(arg)


def funcion(arg1, arg2):
    print(arg1, arg2)
## da error
```
- Si existe el overloading de operadores.

#### Overloading de operadores
- El operador + actua distinto según el tipo de clase que se esta operando, por ejemplo al sumar una string o una lista, se realizan distintas acciones.
- Podemos definir o redefinir el comportamiento de los operadores para operandos de cierta clase.
- Se puede usar por ejemplo ```def __add__()``` para alterar el retorno de la operación `+` entre dos operandos de una clase.
- Ejemplo
```py
class Billetera:
  def __init__(self, pesos, dolares, bitcoin):
    self.pesos = pesos
    self.dolares = dolares
    self.bitcoin = bitcoin
  
  ## Se redefine el comportamiento de Billetera1 + Billetera2
  def __add__(self, otra_billetera):
    return Billetera(self.pesos + otra_billetera.pesos, 
    self.dolares + otra_billetera.dolares,
    self.bitcoin + otra_billetera.bitcoin)

## ahora podemos sumar 2 billeteras.
Billetera(10, 11, 23) + Billetera(1000, 22, 2323)
```

- Ejemplo 2 oficial
- Cambia el < y retorna el valor de self.magnitud < otro.magnitud
```py
import math

class Vector: 
    """Vector desde el origen"""
    def __init__(self, x, y): 
        self.x = x 
        self.y = y
        
    @property
    def magnitud(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def __lt__(self, otro_punto):
        return self.magnitud < otro_punto.magnitud

v1 = Vector(2,4)
v2 = Vector(8,3)
print(v1 < v2)
```
### _/_repr_/_ y __str_/_
- El método __repr__ es la version para desarrollador de imprimir un objeto.
- Por defecto print(objeto) imprime el repr de un objeto
- Con la funcion __str__ podemos crear una version mas legible de la representacion de un objeto.
- Si existe str, print lo llamara.

- Ej oficial:
```py
class Fraccion:
    def __init__(self, numerador, denominador): 
        self.numerador = numerador 
        self.denominador = denominador
        
    def __repr__(self):
        return f"Fraccion({self.numerador}, {self.denominador})"
    
    def __str__(self):
        return f"{self.numerador} / {self.denominador}"
    
frac = Fraccion(3, 4)
```

### *Duck typing*
- Pendiente
- En Python ya tenemos comportamiento polimorfico sin necesidad de herencia, por lo que no es tan atractivo usarla
- Si tenemos una funcion activar() que recibe un parametro, el cual no sabemos su tipo, podemos llamar a los metodos del tipo, (que podrian ser iguales), y tener polimorfismo, al tener distintos comportamientos de metodos para objetos de distinta clase. (reescribir y entender mejor)
- Por lo tanto, usar herencia no es tan necesario.
- Por ejemplo:
```py
class Pato:
    def gritar(self):
        print("Quack!")
        
    def caminar(self):
        print("Caminando como un pato")        
    
class Persona:
    def gritar(self):
        print("¡Ahhh!")
        
    def caminar(self):
        print("Caminando como un humano")

def activar(pato):  # Esto, en otro tipo de lenguaje, obligaría a que pato sea del tipo "Pato", por lo tanto
    pato.gritar()   # la función activar no podría ser llamada con un argumento tipo "Persona"
    pato.caminar()

donald = Pato()
juan = Persona()
activar(donald)
activar(juan)

```

## Multiherencia
- Nota: Todas las clases de Python heredan de `object`.
- Se conoce como multiherencia a que una subclase puede heredar más de una clase a la vez. (Varias superclases)
- Por ejemplo, una clase Academico podría tener dos roles, y heredar de Investigador y Docente.
- Ejemplo base (bien hecho):

```py
class Investigador:

    def __init__(self, area='', **kwargs):
        # Utilizamos super() para heredar correctamente
        super().__init__(**kwargs)
        self.area = area
        self.num_publicaciones = 0


class Docente:

    def __init__(self, departamento='', **kwargs):
        # Utilizamos super() para heredar correctamente
        super().__init__(**kwargs)
        self.departamento = departamento
        self.num_cursos = 3

# Aquí decimos que Academico hereda tanto de Docente como de Investigador
class Academico(Docente, Investigador):
    
    def __init__(self, nombre, oficina, **kwargs):
        # Utilizamos super() para heredar correctamente
        super().__init__(**kwargs)
        self.nombre = nombre
        self.oficina = oficina


p1 = Academico(
    "Emilia Donoso",
    oficina="O5",
    area="Inteligencia de Máquina",
    departamento="Ciencia De La Computación"
)
#tmb funciona
# p1 = Academico(
#     "Emilia Donoso",
#     "O5",
#     area="Inteligencia de Máquina",
#     departamento="Ciencia De La Computación"
# )
print(p1.nombre)
print(p1.area)
print(p1.departamento)
```

### Problema del diamante
- Si tenemos, por ejemplo, una claseB (padre), de la cual heredan 2 subclases, por la izquierda y derecha, tenemos una **jerarquía de diamante**.
![](@attachment/Clipboard_2023-08-23-22-56-03.png)
- El problema con esto, es que tenemos más de un "camino" desde la clase inferior (SubClaseA), que puede pasar por 2 clases distintas (SubClaseIzquierda y SubClaseDerecha) hasta la clase superior (ClaseB).
- Esto pasa para todas las clases de Python, las cuales heredan de `object`:
![](@attachment/Clipboard_2023-08-23-23-00-22.png)

- El problema con tener mas de un camino para llegar a laclase padre, es decir "problema del diamante", es que, por ejemplo, al hacer `super()` desde la clase SubClase de la foto anterior, llamaríamos dos veces al inicializador de object. Entre otros problemas.

### __mro__, obteniendo el orden de herencia
- Podemos obtener el orden en el que se ejecutan los métodos en un esquema de multiherencia, por ejemplo:
```py
MiSubclase.__mro__
## puede retornar algo como
# (__main__.MiSubClase,
#  __main__.SubClaseIzquierda,
#  __main__.SubClaseDerecha,
#  __main__.ClaseB,
#  object)
```

- blablabla mucho texto

### Uso de *args y *kwargs
- Python permite otorgar argumentos a una función mediante `*args` y `**kwargs`. Para que sirven?


- `*args`: Permite recibir una lista de argumentos de largo variable, sin keywords asociados. * desempaqueta los args y los pasa como argumentos posicionales. Al ser una lista, se puede acceder a un argumento usando [].
Ej:
```py
def imprimir2(argumento_obligatorio, *args, **kwargs):
    print("kwarg 0", args[0])  ## IMPRIME 4444
    

print("\nEjemplo 2, Usar *")
imprimir2("waku waku", 4444, "starlight", [2021, 2020])
```
- `**kwargs`: Es una secuencia de argumentos de largo variable, cada elemento de la lista tiene asociado un **keyword**. ** mapea los elementos desde un map y los pasa a la función por su keyword asociado.
Ej:
```py

def imprimir(arg1, **kwargs):
  ## no importa el orden de los argumentos
  test = "SI" ## hace algo con el test que recibe
  mono = 0## hace algo con el mono que recibe
  pass

## seria equivalente a que imprimir se llamara como
## imprimir(arg1, mono, test), y se pasara asi los elementos
## tmb equivalente a imprimir(arg1, test, mono) ## NO IMPORTA EL ORDEN
imprimir("hola", mono=1, test="SI")

```

- Nota: kwargs y args son solo nombres por convencion, se puede usar cualquier nombre, usando `*argumentosposicionales` o `**args_keywords` por ejemplo.

### Ejemplo 1 y sus implementaciones
- Por ejemplo, una clase Academico podría tener dos roles, y heredar de Investigador y Docente.

#### Implementación original
- El problema de este ejemplo es que al inicializar Academico llamamos dos veces al inicializador de `object` por problema del diamante.
```py
class Investigador:

    def __init__(self, area):
        self.area = area
        self.num_publicaciones = 0


class Docente:

    def __init__(self, departamento):
        self.departamento = departamento
        self.num_cursos = 3


class Academico(Docente, Investigador):

    def __init__(self, nombre, oficina, area_investigacion, departamento):
        # Queremos reemplazar esto por un super().__init__(...)
        Investigador.__init__(self, area_investigacion)
        Docente.__init__(self, departamento)
        self.nombre = nombre
        self.oficina = oficina


p1 = Academico("Emilia Donoso", "O-5", "Inteligencia de Máquina", "Ciencia De La Computación")
print(p1.nombre)
print(p1.area)
print(p1.departamento)
```
#### Mejor solución para el ejemplo 1
- Usar solo `super().__init__()` para inicializar y los kwargs 
- Mi solución:
```py
class Investigador:
    ## si queremos que area sea opcional
    ## se escribe area='' para el caso de que no se entregue area
    
    ## con kwargs acepta elementos adicionales y no los usa.
    def __init__(self, area = '', **kwargs):
        super().__init__(**kwargs) ## segun el mro, inicializamos object
        self.area = area
        self.num_publicaciones = 0


class Docente:

    def __init__(self, departamento = '', **kwargs):
        ## OJO, TAMBIEN SE PONE SUPER KWARGS AQUI
        ## YA QUE SEGUN MRO, EL ORDEN DE PYTHON ES
        ## (<class '__main__.Academico'>, <class '__main__.Docente'>, <class '__main__.Investigador'>, <class 'object'>)
        ## por lo tanto, todos deben tener ese super.
        super().__init__(**kwargs) # mro: inicializamos Investigador

        self.departamento = departamento
        self.num_cursos = 3


class Academico(Docente, Investigador):
    ## area_investigacion y departamento reemplazados por kwargs
    def __init__(self, nombre, oficina, **kwargs):
        # Queremos reemplazar esto por un super().__init__(...)
        #Investigador.__init__(self, area_investigacion)
        #Docente.__init__(self, departamento)
        # le pasamos los kwargs y la clase padre vera que hace con ellos.
        super().__init__(**kwargs) # mro, llamaria a docente
        self.nombre = nombre
        self.oficina = oficina


## Se pasan dos elementos con keys asociadas, que son tomados como
## **kwargs por Academico, y luego si son usados directamente en Docente
## o Investigador. En Docente se usa area, y en Invest. usa departamento
p1 = Academico("Emilia Donoso", "O-5", area="Inteligencia de Máquina", departamento="Ciencia De La Computación")
print(p1.nombre)
print(p1.area)
print(p1.departamento)
```
- Mro: `(<class '__main__.Academico'>, <class '__main__.Docente'>, <class '__main__.Investigador'>, <class 'object'>`

- Solución oficial con toda la explicación y su output intuitivo:
```py
class Investigador:

    def __init__(self, area, **kwargs):
        print(f"init Investigador con area '{area}' y kwargs:{kwargs}")
        super().__init__(**kwargs)
        self.area = area
        self.num_publicaciones = 0


class Docente:

    def __init__(self, departamento, **kwargs):
        print(f"init Docente con depto '{departamento}' y kwargs:{kwargs}")
        super().__init__(**kwargs)
        self.departamento = departamento
        self.num_cursos = 3


class Academico(Docente, Investigador):

    def __init__(self, nombre, oficina, **kwargs):
        print(f"init Academico con nombre '{nombre}', oficina '{oficina}', kwargs:{kwargs}")
        super().__init__(**kwargs)
        self.nombre = nombre
        self.oficina = oficina


print(Academico.__mro__)
print("--------")

p1 = Academico(
    "Emilia Donoso",
    oficina="O5",
    area="I.A.",
    departamento="Computación"
)
print("--------")
print(p1.nombre)
print(p1.area)
print(p1.departamento)
```
- Salida:
```
(<class '__main__.Academico'>, <class '__main__.Docente'>, <class '__main__.Investigador'>, <class 'object'>)
--------
init Academico con nombre 'Emilia Donoso', oficina 'O5', kwargs:{'area': 'I.A.', 'departamento': 'Computación'}
init Docente con depto 'Computación' y kwargs:{'area': 'I.A.'}
init Investigador con area 'I.A.' y kwargs:{}
--------
Emilia Donoso
I.A.
Computación
```

#### Otras implementaciones y sus problemas
- pendiente

### Ejemplo Avatar
- pendiente (probablemente nunca lo haga.)


## Clases abstractas
- Son clases cuya intención es **no ser instanciadas**. Se usan solo como parte del modelamiento de otras clases.
- Ejemplo: `Mamifero` es algo abstracto, pero describe a Perro, Mono y Humano.
- Mamifero no tiene sentido por si solo, pero si al tener subclase.
- La subclase se instancia.

- Un **método abstracto** de una clase abstracta representa un comportamiento que deben tener todas las clases que heredan de la clase.
- Generalmente difieren de implementacion entre subclases.

- La clase abstracta establece comportamiento minimo, y las subclases deben implementarlo.

- Las clases abstractas tambien pueden tener metodos normales, que no son necesarios de reimplementar.
- Esto es util para ahorrar tiempo y el sentido de todo esto.

- Entonces, una clase es **abstracta** si:
  - Es una clase que no se instancia directamente
  - Contiene uno o más métodos abstractos
  - Sus subclases implementan todos sus métodos abstractos

### *Abstract Base Class*
- Python no tiene forma de crear abstract classes, pero el modulo abc lo incluye.
- Se usa la clase ABC y el decorador @abstractmethod.

- Ejemplo genérico:
```py
from abc import ABC, abstractmethod


class Base(ABC):

    ## aqui tambien podriamos tener un init y metodos normales.
    @abstractmethod
    def metodo_1(self):
        pass

    @abstractmethod
    def metodo_2(self):
        pass

    ## no se puede acceder directamente a base.valor, si se puede desde la clase hija
    @property
    @abstractmethod
    def valor(self):
        return '¿Llegaremos aquí?'

class SubClase1(Base):

    def metodo_1(self):## reimplementa el metodo 2
        pass

    def metodo_2(self): ## lo mismo, reimplementa
        pass
    def a(self): ## puede tener mas cosas
        pass

    ## reimplementa y redefine valor, ahora si es accesible
    @property
    def valor(self):
        return 'Propiedad concreta'

b = Base()## 
print(f'Base.value: {b.valor}') ## error, no se puede acceder desde una clase Base a nada de abstract.
i = Implementacion()
print(f'implementacion.valor: {i.valor}')## 'Propiedad concreta'.

```

### Ejemplo personaje
- Pendiente, copiado y pegado
```py
from random import randint
from time import sleep


class Personaje(ABC):

    def __init__(self, nombre, x, y, energia):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.energia = energia

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, valor):
        self.__energia = max(valor, 0)

    def simular(self):
        while self.energia > 0:
            sleep(1)
            self.saludar()
            self.moverse()
            self.gastar_energia()
        print("Perdí toda mi energía :(")

    @abstractmethod
    def moverse(self):
        pass

    @abstractmethod
    def gastar_energia(self):
        pass

    @abstractmethod
    def saludar(self):
        print(f"Soy {self.nombre}. Estoy en {(self.x, self.y)}.")


## una implementacion de la abstract class personaje
## personaje igual tiene cosas no abstractas, como x, y, simular q no son abstractas
class Jugador(Personaje):

    ## redefine
    def moverse(self):
        # El jugador se mueve en la misma dirección de forma constante
        self.x += 1
        self.y += 1

    ##redefine
    def gastar_energia(self):
        # Pierde una cantidad aleatoria de energía
        cambio = randint(-1, 3)
        ## usa property no abstract de la clase padre
        self.energia -= cambio
        if cambio < 0: # Puede que gane energía de vez en cuando
            print("¡Gané energía!")

    ##redefine llamando a saludar abstract, si se puede
    def saludar(self):
        # Utiliza la definición de Personaje para saludar
        super().saludar()

## otra implementacion de la clase abstracta personaje
class Enemigo(Personaje):

    ##redefine
    def moverse(self):
        # Se mueven aleatoriamente por el mapa
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)

    ##redefine
    def gastar_energia(self):
        # Gastan energía a tasa constante
        ## usa property no abstract de la clase padre
        self.energia -= 1

    def saludar(self):
        # Agrega un grito por sobre la implementación original
        print("¡Te atraparé!")
        super().saludar()## llama a saludar de personaje

```

## Bonus: Diagrama de Clases
- Se pueden modelar las clases que componen un sistema, con sus atributos metodos y interacciones. 
- Se ocupa UML (Unified Modeling Language).

### Elementos de un diagrama de clases
- Estan las clases y relaciones

#### Clases
- Son las estructuras que encapsulan la información.

#### Relaciones

##### Composición
- En esta relacion, la vida del objeto esta condicionada por el tiempo de vida del objeto que lo incluye.
- Es decir, no tiene sentido que exista el objeto incluido si no existe quien lo incluye.
- Ejemplo: Mario no tiene sentido si no existe Juego:
- Ej:
![](@attachment/Clipboard_2023-08-24-01-10-37.png)


##### Agregación
- Es un tipo de relacion donde no hay necesidad de que exista el elemento que contiene a la clase para tener sentido. (reescribir)
- Ej: Los goombas pueden existir por si solos y tiene sentido, sin que existan como parte de un ejercito. Por otro lado los goombas no tienen sentido sin existir el juego.
![](@attachment/Clipboard_2023-08-24-01-05-55.png)

##### Herencia
- Se representa así:
![](@attachment/Clipboard_2023-08-24-01-02-10.png)

##### Ejemplo completado:
![](@attachment/Clipboard_2023-08-24-01-11-05.png)

## Bonus: Métodos estáticos
- Son métodos que pertenecen a una clase, pero no dependen de informacion ni de atributos de la instancia. No ocupan self. Se usa el `@staticmethod` para definir un metodo estatico.
- Es cómo en Java :)
- Ejemplo:
```py
class Math:
  @staticmethod
  def sumar(n1, n2):
    return n1 + n2
  @staticmethod
  def multiplicar(n1, n2):
    return n1 * n2
```


