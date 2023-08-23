---
tags: [prog-avanzada]
title: Semana 2
created: '2023-08-23T02:16:55.058Z'
modified: '2023-08-23T04:35:27.661Z'
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
    # Se llama al constructor de la clase padre
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
- Se conoce como multiherencia a que una subclase puede heredar más de una clase a la vez. (Varias superclases)

### Problema del diamante

### Ejemplo 1

#### Uso de *args y *kwargs



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


## Bonus: Diagrama de Clases
- Se pueden modelar las clases que componen un sistema, con sus atributos metodos y interacciones. 
- Se ocupa UML (Unified Modeling Language).

### Elementos de un diagrama de clases
- Estan las clases y relaciones

#### Clases
- Son las estructuras que encapsulan la información.

#### Relaciones


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


