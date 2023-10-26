---
tags: [prog-avanzada]
title: Semana 11
created: '2023-10-25T23:47:41.966Z'
modified: '2023-10-26T02:30:44.045Z'
---

# Semana 11


## I/O

### I/O
- TODO: 
### *Context Manager*
- TODO:

### Emulación de IO
- TODO:


## *Strings*

### Strings
- Los strings son cadenas de caracteres que Python encodea en UTF-8.
- Son inmutables, para modificar `cadena[1]` se crea una nueva string `cadena`
- Se concatenan con `+=` o similares.

- Formas de definir strings:
```py
a = "programando"
b = 'mucho'
c = '''un string
con múltiples
lineas'''
d = """Multiples con
     comillas dobles"""
e = ("Tres" " strings" " juntos")
f = "un string " + "concatenado"
g = ("Otra forma de string que nos permite "
     "utilizar más de una línea pero en verdad solo es una,"
     " lo que es muy útil para cumplir PEP-8 :)")
```


#### Secuencias de escape
- El `\` es el cáracter de escape
- Se puede combinar para cambiar el significado de caracteres o insertar comillas, etc.
- Caracteres:
  - `\"`: Comilla doble 
  - `\'`: Comilla simple
  - `\n`: newline
  - `\t`: tab
  - `\\`: backslash

- Ej:
```py
# Si quiero escribir " en una string con "" es
a = "lorem ipsum \" jsdjsd sdsd s"
a2 = 'lorem ipsum \' sdsad ada ds'

# Si quiero escribir un backslash sin que sea escape character
b = "backslash como caracter \\"

```



### Métodos

#### Métodos de consulta (str.metodo())
- `isdigit()`: Esta compuesto por solo digitos?
- `isalpha()`: Esta compuesto por solo letras de un lenguaje?
- `startswith(s)`: Empieza por `s`?
- `endswith(s)`: Termina con `s`?
- ``

- Interesante: https://stackoverflow.com/questions/22190064/difference-between-find-and-index

#### Métodos que modifican (str.metodo())
- Nota: No modifican, crean una string nueva con los cambios.
- `split(s)`: Retorna una lista de strings que separa a la string por cada `s`
- `join(s)`: Contrario de split, junta los objetos de una lista con el separador `s`
- `replace(s1, s2)`: Reemplaza todas las ocurrencias de s1 en la string por s2



### Formatting con variables
- Se pueden usar f-strings con `f""`. Se ponen variables con `{nombre_variable}`.
- Ej 1 (basico):
```py
producto = "pan"
precio = 2500

print(f"El costo de {producto} es {precio}")
```


- Ej 2 (insertar `{}` como string):
```py
test = f"""{{ estas llaves se muestran }}"""
# { estas llaves se muestran }
# Se pone doble llave si se quiere colocar una llave literal.
## ej oficial:
# permite insertar {} de Java.

# Con estas variables generaremos el string
clase = "MiClase"
salida = "'hola mundo'" # 'hola mundo'

# En nuestra plantilla utilizamos llaves dobles cuando queremos mantenerlas...
codigo = f"""
public class {clase}
{{
       public static void main(String[] args)
       {{
           System.out.println({salida});
       }}
}}"""

# ... pero en el resultado a imprimir solo se verá una llave simple
print(codigo)
```

- Ej 3 (uso de dict y avanzado):
```py
# Las variables necesarias para crear nuestro string
message = {
    "emails": ["yo@ejemplo.com", "tu@ejemplo.com"],
    "subject": "mira este correo",
    "message": "\nSorry, no era tan importante"
}

# Nuestro f-string
print(f"""
From: <{message['emails'][0]}>
To: <{message['emails'][1]}>
Subject: {message['subject']}
{message['message']}
""")
```

- Ej 4 (uso de clase):
```py
# Esta clase representa a un e-mail
class EMail:
    def __init__(self, from_addr, to_addr, subject, message):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.message = message


# Creamos nuestra instancia de la clase
email = EMail(
    "a@ejemplo.com",
    "b@ejemplo.com",
    "Tienes un correo",
    "\nQue tengas un lindo día\n\nSaludos :)"
)

print(f"""
From: <{email.from_addr}>
To: <{email.to_addr}>
Subject: {email.subject}
{email.message}""")

## se accede a atributos de clase para formatear.
```


- Ej interesante (con format tmb):
```py
'{:<30}'.format('left aligned')
#'left aligned                  '

'{:>30}'.format('right aligned')
#'                 right aligned'

'{:^30}'.format('centered')
#'           centered           '

'{:*^30}'.format('centered')  # use '*' as a fill char
#'***********centered***********'
```

#### `str.format()`
- Se puede crear una f-string que sirva como plantilla reusable, y luego usar `format(parametros)` con los parametros a reemplazar en los `{}`

- Ej 1 Solo {}:
```py

```

- Ej 2 (Reemplazo con key-value):
```py


```


### Formatting Avanzado
- Especificación: https://docs.python.org/3/library/string.html#format-specification-mini-language


## RegEx

### Intro a RegEx
- Si queremos encontrar una o multiples secuencias complejas en un string, existen los patrones de búsqueda.
- Estos patroens se conocen como **regex** o **regular expressions**. Son secuencias especiales que permiten comparar y buscar conjuntos o strings.
- Sirven para: Validación de formularios, búsqueda y reemplazo, transformación de texto, etc.

- Cada cáracter hace match exactamente con ese patron dentro de la string. Por ejemplo `abcde` hace match con algo con `abcde`.
- Para poder hacer cosas mas avanzadas se usan **meta-caracteres**

- Estos son los **meta-caracteres**: `. ^ $ * + ? { } [ ] \ | ( )`. Explicación:
  - `[ ]`:
  - `+`:
  - `*`:
  - `?`:
  - `{m, n}`:
  - `.`:
  - `^`:
  - `$`:
  - `( )`:
  - `A | B`: Admite match con la regex A o B. Ej:
  - `\`: 


- En Python se usa el módulo `re` para usar regex. Las funciones son
  - `re.match()`
  - `re.fullmatch()`:
  - `re.search()`:
  - `re.sub()`:
  - `re.split()`:


### *Matching*
- ...

- Ej 1:


#### Verificación de email


#### Verificación de RUT




### Búsqueda



### Sustitución


### *split*
