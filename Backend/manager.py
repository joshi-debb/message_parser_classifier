class Response:
    def __init__(self) -> None:
        self.nombre: str = ''
        self.usuario: str = ''
        self.red_social: str = ''
        self.texto = ''
        self.total: str = ''

    def show_messages(self):
        print(' lugar: {}, fecha: {}, hora: {}, usuario: {}, red social: {} , mensaje: {}'.format(self.lugar, self.fecha, self.hora, self.usuario, self.red_social , self.texto))

class Message:
    def __init__(self) -> None:
        self.lugar: str = ''
        self.fecha: str = ''
        self.hora: str = ''
        self.usuario: str = ''
        self.red_social: str = ''
        self.texto = ''
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

    def add_negative(self,word):
        self.negative.append(word)

class Corp:
    def __init__(self,name):
        self.name = name
        self.services = Service_List()
        self.positive: int = 0
        self.negative: int  = 0
        self.neutral: int = 0
        self.total = int(self.positive) + int(self.negative) + int(self.neutral)

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
            obj = {'Nombre' : i.name}
            # list_services = self.get_by_name(i.name).services.send_datas()
            # for i in list_services:
            #     list_alias = i.aka.send_datas()
            json.append(obj)
        return json

class Service:
    def __init__(self,name):
        self.name = name
        self.aka = Akas_List()
        self.positive: int = 0
        self.negative: int  = 0
        self.neutral: int = 0
        self.total = int(self.positive) + int(self.negative) + int(self.neutral)

class Service_List():
    def __init__(self) -> None:
        self.services = []
    
    def add_to_end(self,name):
        new = Service(name)
        self.services.append(new)
    
    def get_by_name(self,name):
        for i in range(len(self.services)):
            if self.services[i].name == name:
                return self.services[i]
    
    def show_services(self):
        for i in range(len(self.services)):
            print(self.services[i].name)
            return self.services[i]
               
    def send_datas(self):
        json = []
        for i in self.services:
            obj = {'Nombre' : i.name}
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
            obj = {'Nombre' : i.name}
            json.append(obj)
        return json

class Positivo():
    def __init__(self, palabra):
        self.palabra = palabra

class Negativo():
    def __init__(self, palabra):
        self.palabra = palabra

class Neutro():
    def __init__(self, palabra):
        self.palabra = palabra