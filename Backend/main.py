
from unicodedata import normalize
import re
from manager import State,Corps_List
from flask import Flask, jsonify, request
from flask.json import jsonify

from afd import Message,automata,scanner

from xml.dom import minidom

app = Flask(__name__)

manage = State()
corpse = Corps_List()

texto = []

tokens_list = []
msm_list = []

@app.route('/')
def index():
    return 'Pagina Principal: Proyecto 3 IPC2', 200

@app.route('/read_datas', methods=['POST'])
def add():
    
    xml = request.get_data().decode('utf-8')
    mydoc = minidom.parseString(xml)
    diccionarios = mydoc.getElementsByTagName('diccionario')
    mensajes = mydoc.getElementsByTagName('lista_mensajes')

    for elemento in diccionarios:
        positivos = elemento.getElementsByTagName('sentimientos_positivos')
        negativos = elemento.getElementsByTagName('sentimientos_negativos')
        empresas = elemento.getElementsByTagName('empresas_analizar')

        for items in positivos:
            palabra = items.getElementsByTagName('palabra')
            for pala in palabra:
                txt = pala.firstChild.data
                txt = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", txt), 0, re.I)
                manage.add_positive(txt)
        
        for itemses in negativos:
            palabra2 = itemses.getElementsByTagName('palabra')
            for pala2 in palabra2:
                txt1 = pala2.firstChild.data
                txt1 = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", txt1), 0, re.I)
                manage.add_negative(txt1)

        for subElemento in empresas:
            empresa = subElemento.getElementsByTagName('empresa')
            for attribs  in empresa:
                nombres = attribs.getElementsByTagName('nombre')
                servicios = attribs.getElementsByTagName('servicio')
                for names in nombres:
                    nombre = names.firstChild.data
                    corpse.add_to_end(nombre)
                for ser in servicios:
                    servicio = ser.attributes['nombre'].value
                    aliases = ser.getElementsByTagName('alias')
                    corps = corpse.get_by_name(nombre) 
                    corps.services.add_to_end(servicio)
                    for aka in aliases:
                        aliases = corps.services.get_by_name(servicio)
                        alias = aka.firstChild.data
                        aliases.aka.add_to_end(alias)
                        
    for elemento in mensajes:
        msm = elemento.getElementsByTagName('mensaje')     
        for item in msm:
            txt = item.firstChild.data
            txt = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", txt), 0, re.I)
            texto.append(txt)

    return jsonify({'ok' : True, 'msg':'Datos almacenados con exito'}), 200

@app.route('/analyze_datas', methods=['GET'])
def extract_datas():
    global tokens_list,corpse

    for cadena in texto:
        tokens = automata(cadena)
        tokens_list.append(tokens)
        
    for lista in tokens_list:
        msms = scanner(lista,manage.positive,manage.negative,corpse)
        for obj in msms:
            obj.show_messages()
            # for i in corpse.corps:
            #     print(i.name)
            #     for palabra in obj.texto:
            #         if palabra == i.name:
            #             print('coincidencia')
            #         print(palabra)

    return jsonify(corpse.send_datas()), 200

if __name__=='__main__':
    app.run(debug=True, port=4000)