import re
from typing import List
from unicodedata import normalize
from manager import State,Corps_List,Message,Token,Errors,Corp

contador_mensajes = 0
contador_neutrals = 0

mensaje_positivo = 0
mensaje_negativo = 0
mensaje_neutro = 0

manage = State()
corpse = Corps_List()


def automata(starter: str):
    #agregando al final
    starter += '\n'
    #lista de tokens
    tokens: List[Token] = []
    #lista de errores
    errores: List[Errors] = []
    #estado inicial
    state: int = 0
    tmp_state: int = 0
    #estado actual
    lexeme: str = ''
    #apuntador
    pointer: int = 0
    #Contador de filas y columnas
    row: int = 1
    col: int = 0

    while pointer < len(starter):
        char = starter[pointer]
        # state inicial
        if state == 0:
            #Lista de transiciones
            #Si el caracter es una letra [A-Z,Ñ , a-z,ñ]
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                state = 1
                pointer += 1
                col += 1
                lexeme += char
            #Si el caracter un digito [0-9]
            elif(ord(char) >= 48 and ord(char) <= 57):
                state = 2
                pointer += 1
                col += 1
                lexeme += char
            
            #Si el caracter un digito [: , .]
            elif(char == ":" or char == "," or char == "."):
                state = 15
                pointer += 1
                col += 1
                lexeme += char

            # caracteres ignorados
            #si es un salto de linea [\n]
            elif (ord(char) == 10):
                row += 1
                col = 0
                pointer += 1
            #si es un tabulador horizontal [\t]
            elif (ord(char) == 9):
                col += 1
                pointer += 1
            #si es un espacio en blanco ['']
            elif (ord(char) == 32):
                col += 1
                pointer += 1

            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        #estado 1
        elif state == 1:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 or ord(char) == 165):
                pointer += 1
                col += 1
                lexeme += char
            
                if lexeme.lower() in ['lugar','fecha','usuario','red','social']:
                    tokens.append(Token('reservada', lexeme, row, col))
                    state = 0
                    lexeme = ''
            else:
                # if((ord(char) >= 48 and ord(char) <= 57) or ord(char) == 95 or ord(char) == 46 or ord(char) == 64):
                if((ord(char) >= 48 and ord(char) <= 57)):
                    state = 3
                    pointer += 1
                    col += 1
                    lexeme += char 
                else:
                    tokens.append(Token('id', lexeme, row, col))
                    state = 0
                    lexeme = ''

        #estado 3
        elif state == 3:
            if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or ord(char) == 164 \
                or ord(char) == 165 or (ord(char) >= 48 and ord(char) <= 57) or ord(char) == 95 or ord(char) == 46 or ord(char) == 64):
                pointer += 1
                col += 1
                lexeme += char
            else:
                tokens.append(Token('user', lexeme, row, col))
                state = 0
                lexeme = ''

        #estado 2
        elif state == 2:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 5
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        #estado 5
        elif state == 5:
            if( char == "/"):
                state = 7
                pointer += 1
                col += 1
                lexeme += char
            elif char == ":":
                state = 6
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        #estado 6
        elif state == 6:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 8
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 8
        elif state == 8:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 4
                tmp_state = 8
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1


        #estado 7
        elif state == 7:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 9
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 9
        elif state == 9:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 10
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 10
        elif state == 10:
            if(char == "/"):
                state = 11
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 11
        elif state == 11:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 12
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 12
        elif state == 12:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 13
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1

        #estado 13
        elif state == 13:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 14
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 14
        elif state == 14:
            if((ord(char) >= 48 and ord(char) <= 57)):
                state = 4
                tmp_state = 14
                pointer += 1
                col += 1
                lexeme += char
            else:
                errores.append(Errors(row, col, char))
                pointer += 1
                col += 1
        
        #estado 1 -> Aceptacion General
        elif state == 4:
            if tmp_state == 8:
                state = 0
                tmp_state = 0
                tokens.append(Token('hora', lexeme, row, col))
                lexeme = ''
            elif tmp_state == 14:
                state = 0
                tmp_state = 0
                tokens.append(Token('fecha', lexeme, row, col))
                lexeme = ''
        
        #estado 15
        elif state == 15:
            state = 0
            tokens.append(Token('simbolo', lexeme, row, col))
            lexeme = ''   
        
    return tokens

def scanner(tokens: List[Token],positives,negatives,empresas: Corps_List):
    global contador_mensajes
    list_parameters: List[Message] = []
    tmp_messages: list = []
    messages: list = []
    tmp_messages.append(messages)
    for i in range(len(tokens)):
        if tokens[i].token == '':
            new_msms: list = []
            tmp_messages.append(new_msms)
            continue
        tmp_messages[-1].append(tokens[i])
    try:
        for messages in tmp_messages:
            msm = Message()
            for i in range(len(tokens)):
                #extraer datos
                if tokens[i].token == 'reservada' and tokens[i].lexeme.lower() == 'lugar' \
                    and tokens[i+1].lexeme.lower() == 'y'and tokens[i+2].token == 'reservada' \
                    and tokens[i+2].lexeme.lower() == 'fecha' and tokens[i+3].lexeme == ':' \
                    and tokens[i+4].token == 'id'and tokens[i+5].lexeme == ',' \
                    and tokens[i+6].token == 'fecha' and tokens[i+7].token == 'hora' \
                    and tokens[i+8].token == 'reservada' and tokens[i+8].lexeme.lower() == 'usuario' \
                    and tokens[i+9].lexeme == ':'  and tokens[i+10].token == 'user' \
                    and tokens[i+11].token == 'reservada' and tokens[i+11].lexeme.lower() == 'red' \
                    and tokens[i+12].token == 'reservada' and tokens[i+12].lexeme.lower() == 'social' \
                    and tokens[i+13].lexeme == ':' and tokens[i+14].token == 'id':
                    
                    
                  
                    #variables locales reseteables
                    positivo:int  = 0
                    negativo:int = 0
                    neutro:int = 0

                    corps = ''
                    services = ''

                    txt = []

                    msm.lugar = tokens[i+4].lexeme
                    msm.fecha = tokens[i+6].lexeme
                    msm.hora = tokens[i+7].lexeme
                    msm.usuario = tokens[i+10].lexeme
                    msm.red_social = tokens[i+14].lexeme
                    for j in range(14,len(tokens)):
                        palabra = ''
                        palabra = tokens[j].lexeme
                        palabra = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", palabra), 0, re.I)
                        msm.texto += palabra
                        msm.texto += ' '
                        txt.append(palabra)

                    for pos in positives:
                        for word in txt:
                            if pos == word:
                                positivo += 1

                    for neg in negatives:
                        for word in txt:
                            if word == neg:
                                negativo += 1
                            
                    if positivo > negativo:
                        msm.estado = 'Positivo'
                    elif positivo < negativo:
                        msm.estado = 'Negativo'
                    elif positivo == negativo:
                        msm.estado = 'Neutro'

                    print(len(empresas.corps))

                    for i in empresas.corps:
                        print(i.name)
                        empresa = corpse.get_by_name(i.name)
                        for k in empresa.services:
                            print(k.name)
                            servicio = empresa.services.get_by_name(k.name)
                            for l in servicio:
                                print(l.name)  
                    
                    print('mensaje aniadido')
                    contador_mensajes += 1

                    break

            list_parameters.append(msm)
        return list_parameters
    except:
        messages = 'null'