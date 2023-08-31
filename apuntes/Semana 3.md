---
tags: [prog-avanzada]
title: Semana 3
created: '2023-08-31T04:22:10.746Z'
modified: '2023-08-31T04:56:55.756Z'
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
for m in monedas.keys():
    print(f'{m}')
for v in monedas.values():
    print(f'{v}')

for k, v in monedas.items():
    print(f'La moneda de {k} es {v}')
```

#### Definición por comprensión
- Pendiente

#### Defaultdicts
- pendiente

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
##### Subcojuntos
- Pendiente



## args y kwargs
- Pendiente

## Iterables y Generadores
- Importante, ver



## Programación Funcional

### Funciones `lambda`


### `map`

### `filter`

### `reduce`


## Anexo built-ins
- Pendiente
