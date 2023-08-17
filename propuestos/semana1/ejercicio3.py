class DCCgram:
    def __init__(self):
        self._usuarios = []
    
    def agregar(self, nuevo_usuario):
        current_usernames = [usuario.username for usuario in self._usuarios]
        if not nuevo_usuario.username == None and \
            not nuevo_usuario.mail == None and \
            not nuevo_usuario.edad == None and \
            not nuevo_usuario.rut == None and \
            nuevo_usuario.username not in current_usernames:
            self.usuarios.append(nuevo_usuario)
        pass
    @property
    def usuarios(self):
        return self._usuarios
    @usuarios.setter
    def usuarios(self, valor):
        self._usuarios = valor
        
class Usuario:
    def __init__(self, username, mail, edad, rut):
        # Así validamos de inmediato los atributos
        self.__username = None
        self.__mail = None
        self.__edad = None
        self.__rut = None
        self.username = username
        self.mail = mail
        self.edad = edad
        self.rut = rut
    
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value):
        self.__username = value
    
    @property
    def mail(self):
        return self.__mail
    
    @mail.setter
    def mail(self, value):
        temp_list = value.split("@", 1)
        if len(temp_list) == 2 and temp_list[1] == "uc.cl":
            self.__mail = value 
        
    @property
    def edad(self):
        return self.__edad
    
    @edad.setter
    def edad(self, value):
        if value >= 18:
            self.__edad = value
        
    @property
    def rut(self):
        return self.__rut
    
    @rut.setter
    def rut(self, value):
        #WIP: check digits##not wip anymore
        ct = 0
        for char in value:
            if char in '0123456789':
                ct += 1
        if(value.count('-') == 1 and ct <= 10):
            self.__rut = value
        #pass
    
    
 
if __name__ == "__main__":
    dcc_gram = DCCgram()
    u1 = Usuario('usuario1', 'usuario1@uc.cl', 17, '00000-0')
    u2 = Usuario('usuario2', 'usuario2@uc.cl', 19, '00000')
    u3 = Usuario('usuario3', 'usuario1@gmail.cl', 19, '00001-0')
    u4 = Usuario('usuario4', 'usuario4@uc.cl', 18, '00002-0')
 
    dcc_gram.agregar(u1)
    dcc_gram.agregar(u2)
    dcc_gram.agregar(u3)
    dcc_gram.agregar(u4)
    # Si todo ha salido bien, solo user 4 debería estar en la lista
    print(dcc_gram.usuarios)  # ¿Qué método deberias implementar para poder verlo en la lista?
    print(dcc_gram.usuarios[0].username)
