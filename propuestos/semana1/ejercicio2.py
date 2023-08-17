class Misterio:
    def __init__(self, atributo):
        self._atributo = atributo
    
    @property
    def atributo(self):
        return self._atributo
    
    @atributo.setter
    def atributo(self, valor):
        if valor % 2 == 1: 
            self._atributo = valor + 1
        else:
            self._atributo = valor
        
if __name__ == "__main__":
    misterio = Misterio(1)
    misterio.atributo += 1
 
## la solucion era que habia que usar
##self._atributo y no self.atributo
