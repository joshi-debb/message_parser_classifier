
class Date:
    def __init__(self) -> None:
        self.fecha: str = ''
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0

class Message:
    def __init__(self) -> None:
        self.lugar: str = ''
        self.fecha: str = ''
        self.hora: str = ''
        self.usuario: str = ''
        self.red_social: str = ''
        self.texto = ''
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0
        self.estado = ''


    def show_messages(self):
        print(' lugar: {}, fecha: {}, hora: {}, usuario: {}, red social: {}, mensaje: {} estado: {}'.format(self.lugar, self.fecha, self.hora, self.usuario, self.red_social , self.texto, self.estado))

class Token:
    def __init__(self, token: str, lexeme: str, row: int, col: int) -> None:
        self.token: str = token
        self.lexeme: str = lexeme
        self.row: int = row
        self.col: int = col

    def show_token(self):
        print('token: {} lexema: {} fila: {} columna: {}'.format(self.token,self.lexeme,self.row, self.col))

class Errors:
    def __init__(self, line: int, col: int, char: str) -> None:
        self.line: int = line
        self.col: int = col
        self.char: str = char
    
    def show_errors(self):
        print('error: {} fila: {} columna: {} '.format(self.char, self.line, self.col))

class State():
    def __init__(self) -> None:
        self.positive = []
        self.negative = []

    def add_positive(self,word):
        self.positive.append(word)
    
    def send_datas_pos(self):
        json = []
        for i in self.positive:
            obj = {
                'Palabra Positiva' : i, 
                }
            json.append(obj)
        return json

    def add_negative(self,word):
        self.negative.append(word)
    
    def send_datas_neg(self):
        json = []
        for i in self.negative:
            obj = {
                'Palabra Negativa' : i, 
                }
            json.append(obj)
        return json

class Corp:
    def __init__(self,name):
        self.name = name
        self.services = Service_List()
        self.positive: int = 0
        self.negative: int  = 0
        self.neutral: int = 0
        self.total: int = 0

class Corps_List():
    def __init__(self) -> None:
        self.corps = []
    
    def add_to_end(self,name):
        new = Corp(name)
        self.corps.append(new)
    
    def get_by_name(self,name):
        for i in range(len(self.corps)):
            if self.corps[i].name == name:
                return self.corps[i]
    
    def show_corps(self):
        for i in range(len(self.corps)):
            print(self.corps[i].name)
            return self.corps[i]
    
    def send_datas(self):
        json = []
        for i in self.corps:
            obj = {
                'Empresa' : i.name , 
                'Servicios' : self.get_by_name(i.name).services.send_datas()
                }
            json.append(obj)
        return json

class Service:
    def __init__(self,name):
        self.name = name
        self.aka = Akas_List()
        self.positive: int = 0
        self.negative: int  = 0
        self.neutral: int = 0
        self.total: int = 0

class Service_List():
    def __init__(self) -> None:
        self.servis = []
    
    def add_to_end(self,name):
        new = Service(name)
        self.servis.append(new)
    
    def get_by_name(self,name):
        for i in range(len(self.servis)):
            if self.servis[i].name == name:
                return self.servis[i]
    
    def show_services(self):
        for i in range(len(self.servis)):
            print(self.servis[i].name)
            return self.servis[i]
               
    def send_datas(self):
        json = []
        for i in self.servis:
            obj = {
                'Servicio' : i.name , 
                'Aliases' : self.get_by_name(i.name).aka.send_datas()
                }
            json.append(obj)
        return json


class Aka:
    def __init__(self,name):
        self.name = name

class Akas_List():
    def __init__(self) -> None:
        self.akas = []
    
    def add_to_end(self,name):
        new = Aka(name)
        self.akas.append(new)
    
    def get_by_name(self,name):
        for i in range(len(self.akas)):
            if self.akas[i].name == name:
                return self.akas[i]
    
    def show_akas(self):
        for i in range(len(self.akas)):
            print(self.akas[i].name)
    
    def send_datas(self):
        json = []
        for i in self.akas:
            obj = {
                'Alias' : i.name
                }
            json.append(obj)
        return json

class Positivo():
    def __init__(self, palabra):
        self.palabra = palabra

class Negativo():
    def __init__(self, palabra):
        self.palabra = palabra