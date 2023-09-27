---
attachments: [Clipboard_2023-09-26-22-54-46.png]
tags: [prog-avanzada]
title: Semana 7
created: '2023-09-25T22:41:25.296Z'
modified: '2023-09-27T03:09:44.542Z'
---

# Semana 7

## Serialización de objetos

### Intro
- La información de los computadores se guarda en base a *bits*. Se debe poder guardar estructuras de datos o instancias de clases como secuencia de *bytes* en archivos o bases de datos. Esto es **serialización**.

### `pickle`
- Módulo `pickle` de Python permite guardar y cargar objetos como objeto de class `bytes`.
- Metodo `dumps`: Serializa y guarda un objeto como bytes
- Metodo `loads`. Deserializa un objeto y lo devuelve a su estado original.
- Metodo `dump` y `load`. Hacen lo mismo pero guardan y recuperan desde archivos.

- Ejemplo serializacion y deserializacion:
```py
import pickle

my_tuple = ("u", 1, 4, "arbol")
my_tuple = my_tuple.dumps() # Ahora son bytes

tuple_deserialized = my_tuple.loads() # ahora es igual a my_tuple


```
- Ej serializacion y deserializacion archivos:
```py
from os import path

my_list = [1, 2, 9, 11, 17, 77, "1"]
# rb read binary mode
# Serialize list into file
with open(path.join("micarpeta", "miarchivo.bin"), "wb") as my_file:
  pickle.dump(my_list, my_file)

# Deserialize file into list
with open(path.join("mi carpeta", "miarchivo.bin"), "rb") as my_file:
  loaded_list = pickle.load(my_file)

```


### Personalizar la serialización en `pickle`
- Al serializar un objeto se verifica que sea de una clase con el metodo `__getstate__`. Si no esta implementada, guarda el atributo `__dict__` del objeto, es decir los atributos en forma de diccionario. Por ejemplo `objeto.atributo` seria `objeto.__dict__["atributo"]`.

- Reimplementar `__getstate__` permite personalizar serialización del objeto. Se recibe `self.__dict__` y se retorna el diccionario que queramos guardar para el objeto.
- Ej:
```py
class Animal:
  def __init__(self, name, species):
    self.name = name
    self.species = species

  def __getstate__(self):
    # Create copy of original object dict (dont modify) and return changed dict
    temp_dict = self.__dict__.copy() #
    temp_dict.update({"species": "Monkey"}) # Every animal will be serialized as monkey
    return temp_dict

```

### Personalizar deserializacion en `pickle`
- Podemos personalizar el objeto siendo deserializado. La funcion `__setstate__` permite modificar el comportamiento al deserializar un archivo. Cambia el diccionario retornado.
```py
class Animal:
  ...
  # state es el diccionario que representa el objeto serializado.
  def __setstate__(self, state):
    # deserializando objeto..
    state.update({"name": f"{state['name']} deserializado"})
    # cambia el atributo name en el diccionario de retorno
    self.__dict__ = state # setea el objeto al diccionario proviniente de deserializar.

my_object = Animal("Esteban", "Dog")

serialized = pickle.dumps(my_object) ## esto llama a __getstate__ del objeto, cambia el species
deserialized = pickle.loads(serialized) ## llama __setstate__ del objeto, cambia el name!
```
- Ejemplo de uso: se puede usar para almacenar atributos relacionados con el estado del programa o similares al guardar un archivo.

### JSON

## Intro
- `pickle` solo puede ser deserializado por otros programas con Python. JSON es interpretable por multiples lenguajes, estandar y legible por humanos. Es similar a los dicts de Python.
- Solo se pueden serializar `int`, `str`, `float`, `dict`, `bool`, `list`, `tuple` y `NoneType`. No cosas de clases.
- Modulo `json`: Incluye `dump(s)` y `load(s)` `dumps()` retorna str en JSON, `loads()` convierte de vuelta a dict.
- Ej deserializacion y serializacion JSON:
```py
from itertools import count
import json

class Animal:
  id = count() # itertools.count(start=0, step=1) # generates increasing numbers (iterator)
  def __init__(self, name, species, age):
    self.name = name
    self.species = species
    self.age = age
    self._id = next(self.id) # generates next count() id

my_animal = Animal("pedro", "Cat", 8)

my_animal_json = json.dumps(my_animal.__dict__) # se usa el dict, ya que json dumps no soporta objetos y soporta ciertos tipos de instancias, como dict.

# recuperar objeto de json a dict
my_animal_dict = json.loads(my_animal_json)

```

### Personalizar la serialización de JSON
- Se puede personalizar la transformación a JSON usando una clase que herede de `json.JSONEncoder`, similar a `__getstate__`.
- Sobreescibimos el metodo `default()`. A default se le pasa el objeto como obj, y se retorna una tupla, formato json, la cual se serializa.
- Al usar `json.dumps()` se pasa el atributo `cls=ClaseEncoder`.

```py
from datetime import datetime
class Animal:
  ...

class AnimalEncoder(json.JSONEncoder):
  def default(self, obj):
    ## only of obj is of type Animal
    if isinstance(obj, Animal):
      return {
        "animal_id": obj._id, # internal id
        "name": obj.name,
        "species": obj.species,
        "age": obj.age,
        "birthdate": datetime.now().year - obj.age, # datetime.now() # retorna objeto datetime?
      }
    # for other objects, nothing is changed for their serialization
    return super().default(obj)

my_animal = Animal("pedro", "Cat", 10)
my_animal_json = json.dumps(my_animal.__dict__, cls=AnimalEncoder) # Se pasa la clase de encoder a usar!

```


### Personalizar deserializacion de JSON
- Para personalizar el paso de JSON a objetos de python, se puede usar el parametro `object_hook` de los métodos `load` y `loads`, de forma similar a `__setstate__`
- Todo objeto JSON se convertira a un dict, y luego se pasara a object_hook para la transformacion final.
- Ej (retorna como lista de tuplas en vez de dict):
```py
def hook_function(in_dict):
  # transforms dict  to list of tuples
  return [(key, value) for key, value in in_dict.items()] # items() retrurns key ,value

json_string = '{"name": "juan", "species": "Monkey", "age": 18}'

data_deserialized = json.loads(json_string, object_hook=hook_function)

print(data_deserialized) # returns list of tuples
```
- **Importante**: Todo objeto JSON se convierte a diccionario y se entrega al object_hook. Es decir los objetos **anidados** se manejan desde dentro hacia afuera.
- Ejemplo:
```py
def funcion_hook(diccionario):
    """Esta función transforma un diccionario en un número"""
    print(f"Me llegó el diccionario: {diccionario}")
    valor = 33 if len(diccionario) > 1 else 42
    print(f"Lo transformaré en {valor}\n")
    return valor


json_string = '{"a": {"b": 1, "c": [2, 3, {}], "d": null, "e": {"f": true}}}'
datos = json.loads(json_string, object_hook=funcion_hook)

print(datos)

#Me llegó el diccionario: {}
#Lo transformaré en 42
#Me llegó el diccionario: {'f': True}
#Lo transformaré en 42
#Me llegó el diccionario: {'b': 1, 'c': [2, 3, 42], 'd': None, 'e': 42}
#Lo transformaré en 33
#Me llegó el diccionario: {'a': 33}
#Lo transformaré en 42
#42
## SE ARRASTRA EL RESULTADO
```


## Manejo de Bytes
- TODO: revisar esta semana
// ### IO?

### Bytes y encoding
- Los strings en Python son una coleccion de caracteres inmutables.
- Los caracteres se encodean comunmente en ASCII, segun se detalla en esta tabla:
![](@attachment/Clipboard_2023-09-26-22-54-46.png)
- La tabla tiene representacion en decimal, hexadecimal y como caracter interpretado.
- Las letras mayus son 65-90, minus son 97-122 y digitos 48-57. Tambien hay caracteres especiales.
- `chr(decimal)` permite obtener el caracter a partir de un decimal.
- `ord(caracter)` permite obtener el codigo en decimal de un caracter.
- mas comun: `hex(decimal)` permite obtener la representacion hexadecimal de un decimal.
- Ej:
```py
print(chr(50)) # 2
print(ord('y')) # 121
print(f"Decimal: 8, Hexadecimal: {hex(8)}") # 0x8 
```
- En el curso se usa **Unicode**, que permite representar hasta 65536 caracteres. Es el estandar moderno.

### Objeto `bytes`
- En Python los *bytes* se representan con un objeto de tipo `bytes`. Es una secuencia inmutable como los string. PAra declararlos se escribe `b"bits"`
- Ej:
```py
# Este ejemplo almacena los caracteres c, l, i, c, h, é
caracteres = b"\x63\x6c\x69\x63\x68\xe9" # b'clich\xe9' # <class 'bytes'>
```
- `\x` indica que los siguientes dos caracteres despues de la x corresponden a un byte en hexa. Los que coinciden con ASCII se reconocen inmediatamente, pero no la é, por lo tanto se imprime como hexa. Por otro lado, la b recuerda que es un objeto bytes no str.

- Los *bytes* se pueden usar para representar cualquier entidad, desde strings a pixeles de una imagen. Para decodificarlo necesitamos saber el encoding usado. Por ejemplo, se decodea usando: `byte_obj.decode("ascii")`

- Para encodear: `str_obj.encode("UTF-8")`
- Ej encode decode:
```py
caracteres = b'\x63\x6c\x69\x63\x68\xe9'
print(caracteres.decode("latin-1"))
print(caracteres.decode("iso8859-5"))

caracteres = "estación"
print(caracteres.encode("UTF-8"))  # 8-bit Unicode Transformation Format
# da error ya que ó no tiene rep ascii
print(caracteres.encode("ascii"))

```
- Tambien se pueden manejar los caracteres no validos en x encoding en la funcion `encode()`, mediante el parametro errors.
- Ej:
```py
print(caracteres.encode("ascii", errors='replace'))  # en ascii se reemplaza el caracter desconocido con "?"
print(caracteres.encode("ascii", errors='ignore'))
print(caracteres.encode("ascii", errors='xmlcharrefreplace'))  # se crea una entidad xml que representa el caracter Unicode
```
- Nota: Los primeros 128 caracteres de UTF-8 son los mismos de ASCII, es backwards comaptible. por lo tanto utf-8 suele ser buena opcion.

### Objeto `bytearray`
- Son **listas** de bytes, que a diferencia de los bytes en si, son mutables.
- Tienen slicing, extend y otros metodos de listas. Se crean con un objeto bytes inicial.
- Definicion: `bytearray(b'bytes')` \x15... o caracteres.
- Ej basico:
```py
# crear
my_ba = bytearray(b"holamundo")
print(ba[3:7]) # bytearray(b'amun')
ba[4:6] = b"\x15\xa3"
ba.extend(b"programa") # agrega bytes al final.

ba[0]# imprime un byte, se muestra el entero que es ascii (104)

bin(ba[0]) # genera un string con la rep binaria del byte (0b1101000)

bin(ba[0])[2:].zfill(8) # elimina el 0b con [2:], y luego llena hasta completar 8 ceros a la izquierda. (01101000)

```
- El hacer print de un byte de un bytearray printea el int, pero tambien sirve ord() de un solo byte:
```py
print(bytearray(b"a")[0])
print(ord(b"a")) # son iguales
```
- Haciendo cambios a bytearray usando ascii en int o ord.
```py
b = bytearray(b'abcdef')
b[3] = ord(b'g')         # El caracter g tiene como código ascii el 103
b[4] = 68                # El caracter D tiene como código ascii el 68, esto sería lo mismo que ingresar b[4] = ord(b'D')
```

- Ejemplo de otros detalles: `append()` solo funciona con un int, que se interpreta como bit. `extend()` acepta bytes o bytearrays.
```py
mi_bytearray = bytearray()

# El método append solo funciona en bytearray con un int
mi_bytearray.append(2)
# El método extend funciona con byte o bytearray
mi_bytearray.extend(b'\xff') #extendemos con un byte
```

### *Chunks*
- Al manejar bytes, puede que queramos leer grupos de bytes, por ejemplo por temas de encoding. Una forma es leyendo *chunks* (grupos) de cierta cantidad de bytes.
- Ej:
```py
my_bytes = bytearray(b"Lorem ipsum sjdjsdsd ...adsd")
SIZE_CHUNK = 4

for i in range(0, len(my_bytes), SIZE_CHUNK): # itera desde 0 con steps de SIZE_CHUNK
  chunk = bytearray(my_bytes[i:i+SIZE_CHUNK]) # :o, raro, si i llega al len no se saldria del array?, a menos q el step se salga..?. Si, se sale. no llega al final. EJ si es 55 el len, llega a 52 y ahi toma algunos. aunque sean menos parece.
  ## REVISAR




```

### Transformación de números
- El tipo de dato `int` tiene metodos que permiten ver su representacion en *bytes*.
- En python se usa `byteorder`. Los ordenes son:
  - *big endian*: El byte mas significativo queda al inicio del byte array. 256 = `0x01 0x00`.
  - *little endian*: EL byte mas significativo queda al final del byte array. 256 = `0x00 0x01`.

- Pasar int a bytearray: Se usa `int.to_bytes(length, byteorder)` Si *length* es mas grande que la cantidad de bytes necesairos para representar el numero, se rellenara con ceros que no afecten al valor (ceros a la izquierda en big endian). 
- Ejs:
```py
(256).to_bytes(5,'big')
(256).to_bytes(2,'little')
i = 1024
i.to_bytes(4, byteorder='big') # prueba cambiando el segundo argumento a 'little'
```
- Pasar bytearray a int: Se usa `int.from_bytes(bytes, byteorder)`. Se le pasa un arreglo de bytes y retorna un int normal.
- Ejs:
```py
int.from_bytes(b'\x00\x00\x04\x00', byteorder='big') # 1024
int.from_bytes(b'\x00\x00\x04\x00', byteorder='little') # 262144
int.from_bytes(b'A', byteorder='little') # 65
```

### Print de `bytes`
- **Importante:** No se debe confiar en los print de bytes. El computador puede reemplazar visualmente un byte por otro caracter segun las formas que tenga de representarlo. Al trabajar con bytes, no depender de como se ven, sino transformar a int usando `from_bytes()` y verificar asi que sea el esperado.
- Ej (se representa incorrectamente): 
```py
int.from_bytes(b'\x0d', byteorder='big') # 13
(13).to_bytes(1,'big') # Esto debería ser \x0d # b'\r'
int.from_bytes(b'\r', byteorder='big') # 13
```



## Excepciones
- TODO: revisar despues

## Levantamiento y manejo de Excepciones
### Levantamiento: `raise`

### Manejo: `try` y `except`

## Bonus: Excepciones personalizadas

