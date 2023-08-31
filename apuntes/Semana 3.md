---
tags: [Import-20c0]
title: Semana 3
created: '2023-08-31T14:06:56.260Z'
modified: '2023-08-31T16:52:05.157Z'
---

# Semana 3


## Estructuras de datos
- Son construcciones que permiten acceder y modificar objetos de un conjunto.


### *built-in*
- Secuenciales:
  - Tuplas
- No secuenciales:
  - Diccionarios
  - Sets

### Tuplas
- Las tuplas, list y str son estructuras secuenciales con indexación

- Las tuplas almacenan datos secuenciales e **inmutables**
- Se accede con índice.
- Pueden tener elementos de distinto tipo.
- Posibles formas de declaración:
```py
a = tuple()

b = (0, 1, 2)

# Cuando creamos una tupla de tamaño 1, debemos incluir una coma al final.
c = (0, )

d = 0, 'uno'
````

#### Desempaquetamiento
- Las tuplas pueden desempacarse en distintas variables.
- Las funciones con múltiples valores de retorno realmente retornan tuplas.
- Ejemplo:

```py
def calcular_geometria(a, b):
    area = a * b
    perimetro = (2 * a) + (2 * b)
    punto_medio_a = a / 2
    punto_medio_b = b / 2
    # Los paréntesis son opcionales, ya que estamos creando una tupla
    return (area, perimetro, punto_medio_a, punto_medio_b)

## lo normal, y luego acceder por data[idx]
data = calcular_geometria(20.0, 10.0)

## desempacar a distintas variables directamente
a, p, mpa, mpb = calcular_geometria(20.0, 10.0)

```

#### Slicing
- Funciona igual que para una list
```py
secuencia[inicio:fin:pasos]
secuencia[:] # shallow copy
```

#### *Named* tuples
- Permite crear tuplas con campos
- Pendiente

### Diccionarios
- Son no secuenciales
- Permite mapeo llave-valor (especie de hashmap)
- Ej:
```py
# Se usan llaves para declararlos
monedas = {
    "Chile": "Peso",
    "Perú": "Soles",
    "España": "Euro", 
    "Holanda": "Euro",
    "Brasil": "Real"
}

## Accede a "Peso"
monedas["Chile"]

monedas["a"] ## KeyError exception


## Retorna el valor de monedas[sdsdsd] si tiene valor
## si no tiene valor, retorna No tiene moneda
print(monedas.get('sdsdsd', 'No tiene moneda'))

## Asignación o mutación de valor
monedas["Vaticano"] = "Lira"

## Eliminar ítems

del monedas["Holanda"]

## Checkear pertenencia (igual q en otras estructuras)
'Argentina' in monedas # True
```

#### Llaves permitidas
- Deben ser objetos hasheables
- Por lo general, los builtin lo son. la list no es.
- Detalles pendientes..

#### Iteración (Métodos útiles) 
- `dict.keys()` retorna una lista con las llaves
- `dict.values()` retorna lista con los valores
- `items()`, retorna lista con pares del diccionario
  - Un par se define como `(llave, valor)` (tupla)
- Ej:
```py
# lo mismo que .keys()
for m in monedas:
    print(f'{m}')
for m in monedas.keys():
    print(f'{m}')
for v in monedas.values():
    print(f'{v}')

for k, v in monedas.items():
    print(f'La moneda de {k} es {v}')
```

#### Definición por comprensión
- Se pueden escribir y crear diccionarios a partir de un concepto estructurado.
- Ej:
```py
from string import ascii_lowercase as letras


# Crea diccionario, con cada letra como key, y luego usa el contador para asignar un value incremental a cada key
numero_por_letra = {letras[i].upper(): i + 1 for i in range(len(letras))}
#{'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8...}

# Con condicional
numero_por_vocales = {
    letras[i].upper(): i + 1 for i in range(len(letras))
    if letras[i].upper() in "AEIOU"
}
# solo crea un valor k,v cuando se cumple la condicion
# el contador cuenta siempre
# {'A': 1, 'E': 5, 'I': 9, 'O': 15, 'U': 21}

```

#### Aplicaciones
- Pendiente

#### Defaultdicts
- Permite crear dicts con valor por defecto para las keys que no existen.
- Permite no preocuparse de eso.
- Ej:
```py
from collections import defaultdict

msg = 'supercalifragilisticoespialidoso'

vocales = defaultdict(int)

# Pasamos int como callable. El callable se va a llamar sin parámetros
# cada vez que se consulte por una key que no existe.
# En este caso, int() devolverá el valor por defecto de este tipo (0)

for letra in msg:
    if letra not in 'aeiou':  # Revisa si la letra es una vocal
        continue

    ## si no existe retorna 0
    vocales[letra] += 1  # si ya existe, agrega una cuenta mas

print(vocales)
```
- Revisar

### Sets
- explicacion pendiente
- ej:
```py
conjunto_vacío = set()

lista_artistas = ["Olivia Newton-John", "Daddy Yankee", "Sting", 
                  "Dream Theater", "Mon Laferte", "Sting"]
lista_artistas_set = set(lista_artistas) # elimina el repetido


conjunto_artistas = {"Olivia Newton-John", "Daddy Yankee", "Sting", 
                     "Dream Theater", "Mon Laferte"}

intento_de_conjunto_vacío = {} # no se puede, crea un diccionariio

```

#### Operaciones de sets
```py
# Add
conjunto_artistas.add("Artista")


# Remove
## da error si no lo encuentra
conjunto_artistas.remove("Artista")

# Discard
## no da error si no lo encuentra
conjunto_artistas.discard("Dream Theater")

# Verificar pertenencia
"Sting" in conjunto_artistas

```

#### Iteracion no ordenada
- Ej:
```py
for artista in conjunto_artistas:
    print(f"Por favor, ¡saluden a {artista}!")
```

#### Operaciones de teoría de conjuntos
- Ej:
```py
set_a = {0, 1, 2, 3}
set_b = {5, 4, 3, 2}

# Union
set_union = set_a | set_b
set_union = set_a.union(set_b)

# Interseccion
set_intersection = set_a & set_b
set_intersection = set_a.intersection(set_b)

# Diferencia
set_difference_a_b = set_a - set_b
set_difference_b_a = set_b - set_a
set_difference_a_b = set_a.difference(set_b)
set_difference_b_a = set_b.difference(set_a)

# Diferencia simétrica
set_sym_difference = set_a ^ set_b
set_sym_difference = set_a.symmetric_difference(set_b)

```
##### Subconjuntos
- Pendiente



## args y kwargs
- args: argumentos
- kwargs: argumentos por palabra clave

- Concepto
- Argumentos: son los valores pasados al llamar una funcion `a(c,d)`
- Parametros: son los valores recibidos por la funcion `def a(b,c)`
- Los parametros estan establecidos y los args cambian.

### Argumentos vs argumentos por palabra clave
- Ej:
```py
def ejemplo(a, b, c):
    print(f'a: {a}, b: {b}, c: {c}')
ejemplo('hola', 'mundo', 42)

## es lo mismo, se pasan por keywords
ejemplo(b='mundo', c=42, a='hola')

## tambien es lo mismo combinando
ejemplo('hola', c=42, b='mundo')

## los argumentos posicionales van antes que las keywords
ejemplo(a='hola', 'mundo', 42)  # ERROR
## tampoco se pueden sobreescribir los posicionales usando keywords



```

#### Otras formas de usar argumentos en la llamada a una funcion
- func(*args): args siendo lista o tupla, desempaqueta y entrega los args como posicionales a la funcion
- func(**args): args siendo dict, desempaqueta y entrega los args por keywords a la funcion
- Se pueden usar simultaneamente estos
- Ej hola mundo 42
```py
ejemplo(*['hola'], **{'c': 42}, b='mundo')
ejemplo('hola', *['mundo', 42])
```

### Cantidad variable de parametros
- Se puede permitir cantidad variable de parametros, usando argumentos por defecto (`b=3`), y args y kwargs
```py
## ejemplo de funcion variable
## el unico obligatorio es a
def func3(a, b=3, *args, **kwargs):
    print(f'a: {a}, b: {b}, args: {args}, kwargs: {kwargs})')
func3(1, 2, 3, 4, c=5, d=6)
```




## Iterables y Generadores

### Iteracion sobre estructuras de datos
- Un iterable es cualquier objeto por el que se puede iterar
```py
for i in iterable:
  pass
```
- Un iterador es un objeto que itera sobre un iterable. Es el objeto retornado por el metodo `__iter__()`. El objeto iter implementa `__next__()` que retorna uno a uno los elementos al ser llamado.
- El iterador da exception StopIteration cuando ya no quedan elementos por recorrer.
- Ej1:
```py
conjunto = {1, 3, 4, 6}
iterador = iter(conjunto)  # Esto es lo mismo que conjunto.__iter__()
print(type(iterador))

print(next(iterador))      # Esto es lo mismo que iterador.__next__()
print(next(iterador))
print(next(iterador))
```

#### Creando estructura iterable
- Forma mas simple, creando clase iteradora.
- Ej:
```py
class Iterable:
    
    def __init__(self, objeto):
        self.objeto = objeto
    
    def __iter__(self):
        return Iterador(self.objeto)

class Iterador:
    
    def __init__(self, iterable):
        # copia de iterable para no afectar valor original
        self.iterable = iterable.copy()
    
    def __iter__(self): 
        return self
    
    def __next__(self):
        if not self.iterable: # self iterable esta vacio.
            # levantar exception
            raise StopIteration("Llegamos al final")
        else:
            valor = self.iterable.pop(0) ## it is a list, removes element at 0
            return valor

datos = [1, 2, 3, 4, 5]
iterable = Iterable(datos)
for i in iterable: ## se puede repetir mas de una vez el for
    print(i, end=" ")

## se puede iterar hasta cierto punto y se mantiene la posicion
for i in iterador:
    print(i, end=" ") # 1,2,3 
    if i >= 3:
        break

## despues continua
for i in iterador:
    print(i, end=" ") # 4, 5
## para volver a iterar se debe obtener otro iterador.
## al usar otro for se llama a __iter__ y se crea uno nuevo.
```

#### Iteradores personalizados
- Se puede cambiar la forma de recorrer un objeto y sus elementos.
- Ej: Itera ordenadamente
```py
class IteradorOrdenado:

    def __init__(self, iterable):
        self.iterable = iterable.copy()

    def __iter__(self):
        # Ordenamos los elementos del iterable antes de empezar a recorrerlos
        self.iterable.sort()
        return self

    def __next__(self):
        if not self.iterable:
            raise StopIteration("Llegamos al final")
        else:
            valor = self.iterable.pop(0)
            return valor


iterable = IteradorOrdenado(datos)
for i in iter(iterable):
    print(i, end=" ")
```

### Generadores
- Caso especial de los **iteradores**. Permiten iterar sobre secuencias de datos sin usar estructura especial que ocupa memoria.
- Al terminar la iteracion sobre un generador, el generador desaparece.
- Sirve para generar calculos temporales
- Sintaxis similar a list comprehension pero con ()

- Ej:
```py
## el usar parentesis crea un generador
generador_pares = (2 * i for i in range(10))
## genera los primeros 10 numeros pares del 0 al 18

## se pueden mostrar los numeros generados con un for
## esto se puede ya que los generadores implementan __iter__, que retorna self.
for i in generador_pares:
    print(i, end=" ")
    # 0 2 4 6 8 10 12 14 16 18 

```
- Ej usando next:
```py
generador_pares = (2 * i for i in range(10))
print(next(generador_pares)) # 0
print(next(generador_pares)) # 2
```
- Un caso de uso puede ser, en lugar de usar archivo.readlines() y llenar un array, usar un generador para extraer una linea a la vez


#### Otra forma de crear un iterable

#### Funciones generadoras
- Las funciones tambien pueden funcionar como generadores, "retornando" con `yield`.
- `yield` retorna el valor indicado, pero asegura que la proxima llamada ejecute la funcion en el mismo estado anterior.
- Ej 1:
```py
def conteo_decreciente(n):
    print(f"Contando en forma decreciente desde {n}")
    while n > 0:
        yield n
        n -= 1

## obteniendo
for number in x:
    print(number)

## obteniendo con next
x = conteo_decreciente(5)
print(next(x)) # 5

```

#### Otra forma de hacer iterable una estructura propia
- Se puede usar una funcion generadora en __iter__ en vez de crear una clase iteradora.
- Ej:
```py
class Iterable:
    
    def __init__(self, objeto):
        self.objeto = objeto.copy()
    
    def __iter__(self):
        while self.objeto:
            yield self.objeto.pop(0)
```


##### Ejemplos de funcion iteradora
- Ej 1:
```py
def fibonacci():
    a, b = 0, 1
    while True: # Notar que este generador nunca "se agota"
        yield b
        a, b = b, a + b

generador_fibonacci = fibonacci()

# Imprimimos los primeros 5 elementos
for i in range(5):
    print(next(generador_fibonacci))
```
- Ej 2:
  - Sobre una lista.
```py
def maximo_acumulativo(valores):
    """Retorna el máximo visto hasta ahora en una colección de valores."""
    max_ = float('-inf')
    for valor in valores:
        max_ = max(valor, max_)
        yield max_
        
lista = [1, 10, 14, 7, 9, 12, 19, 33]

for i in maximo_acumulativo(lista):
    print(i)
```

##### Enviando mensajes a funcion generadora
- Pendiente


## Programación Funcional

### Funciones `lambda`
- En Python las funciones se consideran de primera clase, es decir, las funciones se pueden almacenar y tratar como cualquier otra variable (objeto).
- Ej
```py
# al asignar funcion a una variable, esa variable despues es la funcion
def suma(x, y):
    return x + y

adición = suma

# Son la misma funcion y entregan el mismo resultado
print(suma(3, 5))
print(adición(3, 5))
```
- Las funciones pueden ser pasadas como parametros a otras funciones.
```py
def saludar_joven(nombre):
    return "Joven " + nombre

def saludar_tarde(función_saludo, nombre):
    return "Buenas tardes " + función_saludo(nombre)

print(saludar_tarde(saludar_joven, "Bon")) # Buenas tardes Joven Bon
```

- Las funciones lambda son una forma alternativa de definir funciones en Python.
- La sintaxis es `lambda parametros : valor de retorno`
- No ocupa return.
- Ejemplo:
```py
sucesor = lambda x: x + 1
restar = lambda x, y: x - y

# las funciones lambda no tienen nombre, son anonimas
sucesor.__name__ # <lambda>
```

### `map`
- Recibe como parametros una funcion y al menos un iterable
- `map (f, iterable)` es equivalente a `(f(x) for x in iterable)`
- map() aplica la funcion a cada articulo en el iterable
- Ej:
```py
strings = ['Señores pasajeros', 'Disculpen', 'mi', 'IntencIÓN', 'no', 'Es', 'MolEstar']
mapeo = map(lambda x: x.lower(), strings) ## retorna generator como resultado de ejecutar funcion sobre cada elemento del iterable
', '.join(mapeo) ## printea las strings separadas por , y en lowercase
```
### `filter`
- recibe como parametros una funcion que retorna un bool y un iterable.
- Retorna un generador que entrega los elementos del iterable donde f(x) es True.
- `filter (f, iterable)` es igual a `(x for x in iterable if f(x))`
- Ej:
```py
def fibonacci(límite):
    a, b = 0, 1
    for _ in range(límite):
        yield b
        a, b = b, a + b

## retorna generador con los elementos que cumplen con la condicio 
filtrado_impares = filter(lambda x: x % 2 != 0, fibonacci(10))
print(list(filtrado_impares))
```
### `reduce`
- no mantiene orden
- Reduce es una funcion f(x,y) llamada sobre el resultado de su anterior ejecucion.
- x es el resultado acumulado e y es un elemento de la secuencia
- `reduce(f, iterable)` recibe una funcion que toma dos valores y un iterable. retorna la suma acumulada.
- Ej:
```py
from functools import reduce
lista = [1, 2, 3, 4, 5, 6] # 21
reduce(lambda x, y: x + y, lista)
# retorna la suma acumulada

## con inicializador
reduce(lambda x, y: x + y, lista, 2) # 21+2 # 23

reduce_sin_init = reduce(lambda x, y: f'{x} {y}', lista) # 1 2 3 4 5
reduce_con_init = reduce(lambda x, y: f'{x} {y}', lista, '[Lista]') # [Lista] 1 2 3 4 5



```

### Ejemplos con `reduce`
- Ejs
```py
## aplanar lista
lista_con_listas = [[1, 2], [3, 4], [5, 6], [7, 8, 9]]
lista_aplanada = reduce(lambda x, y: x + y, lista_con_listas) # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

```py
## union/interseccion de conjuntos
conjuntos = [{3, 5, 1}, {4, 3, 1}, {1, 2, 5}, {9, 5, 4, 1}]

unión = reduce(lambda x, y: x | y, conjuntos) # {todo}
intersección = reduce(lambda x, y: x & y, conjuntos) # {1}

## calculo de maximo. mejor usar max()
reduce(lambda x, y: x if x > y else y, unión) 
```

## Anexo built-ins
- Pendiente
