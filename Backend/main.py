
import xml.etree.cElementTree as ET
from unicodedata import normalize
import re

from manager import State,Corps_List,Corp,Service,Aka,Message,Date
from flask import Flask, Response, jsonify, request
from flask.json import jsonify

from afd import automata,scanner

from xml.dom import minidom

app = Flask(__name__)

manage = State()
corpse = Corps_List()

texto = []

tokens_list = []
msm_list = []

tokens_list_aux = []
fast_analisis = []

@app.route('/')
def index():
    return 'Pagina Principal: Proyecto 3 IPC2', 200

@app.route('/read_datas', methods=['POST'])
def add_datas():
    
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
                    nombre = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", nombre), 0, re.I)
                    corpse.add_to_end(nombre)
                for ser in servicios:
                    servicio = ser.attributes['nombre'].value
                    servicio = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", servicio), 0, re.I)
                    aliases = ser.getElementsByTagName('alias')
                    corps: Corp = corpse.get_by_name(nombre) 
                    corps.services.add_to_end(servicio)
                    for aka in aliases:
                        aliases: Service = corps.services.get_by_name(servicio)
                        alias = aka.firstChild.data
                        alias = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", alias), 0, re.I)
                        aliases.aka.add_to_end(alias)
                        
    for elemento in mensajes:
        msm = elemento.getElementsByTagName('mensaje')     
        for item in msm:
            txt = item.firstChild.data
            txt = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", txt), 0, re.I)
            texto.append(txt)

    return jsonify({'ok' : True, 'msg':'Datos almacenados con exito'}), 200

@app.route('/consult_datas', methods=['GET'])
def Consult_datas():
    global corpse,manage
    return jsonify(corpse.send_datas(),manage.send_datas_pos(),manage.send_datas_neg()), 200
    
@app.route('/analyze_datas', methods=['POST'])
def extract_datas():
    global tokens_list,texto,corpse

    dates = []

    cont_positivos = 0
    cont_negativos = 0
    cont_neutros = 0

    for cadena in texto:
        tokens = automata(cadena)
        tokens_list.append(tokens)
        
    for lista in tokens_list:
        msms,positivos,negativos,neutros,txts = scanner(lista,manage.positive,manage.negative,corpse)
        cont_positivos += positivos
        cont_negativos += negativos
        cont_neutros += neutros

        for obj in msms:
            date_obj = Date()

            fecha = ''
            # obj.show_messages()
            fecha = str(obj.fecha)
            if len(dates) == 0:
                print('estaba vacio')
                date_obj.fecha = fecha
                date_obj.positivos += obj.positivos
                date_obj.negativos += obj.negativos
                date_obj.neutros += obj.neutros
                dates.append(date_obj)
                break
            else:
                for x in dates:
                    x: Date
                    if str(x.fecha) == str(obj.fecha):
                        print('la fecha es igual')
                        x.positivos += obj.positivos
                        x.negativos += obj.negativos
                        x.neutros += obj.neutros
                        break
                    elif str(x.fecha) != str(obj.fecha):
                        print('la fecha no es igual')
                        date_obj.fecha = fecha
                        date_obj.positivos += obj.positivos
                        date_obj.negativos += obj.negativos
                        date_obj.neutros += obj.neutros
                        dates.append(date_obj)
                        break

    root = ET.Element("lista_respuestas")
    respuesta = ET.SubElement(root, "respuesta")

    for dat in dates:
        dat: Date
        ET.SubElement(respuesta, "fecha").text = "{}".format(dat.fecha)
        mensajes = ET.SubElement(respuesta, "mensajes")
        ET.SubElement(mensajes, "Total").text = "{}".format(str(dat.positivos+dat.negativos+dat.neutros))
        ET.SubElement(mensajes, "Positivos").text = "{}".format(str(dat.positivos))
        ET.SubElement(mensajes, "Negativos").text = "{}".format(str(dat.negativos))
        ET.SubElement(mensajes, "Neutros").text = "{}".format(str(dat.neutros))
    
    analisis = ET.SubElement(respuesta, "analisis") 
    for corp in corpse.corps:
        corp: Corp

        empresa = ET.SubElement(analisis, "empresa", nombre="{}".format(str(corp.name)))
        mensajes = ET.SubElement(empresa, "mensajes")
        ET.SubElement(mensajes, "Total").text = "{}".format(str(corp.positive+corp.negative+corp.neutral))
        ET.SubElement(mensajes, "Positivos").text = "{}".format(str(corp.positive))
        ET.SubElement(mensajes, "Negativos").text = "{}".format(str(corp.negative))
        ET.SubElement(mensajes, "Neutros").text = "{}".format(str(corp.neutral))
        
        for serv in corp.services.servis:
            serv: Service
            servicios = ET.SubElement(empresa, "servicio", nombre="{}".format(str(serv.name)))
            mensajes = ET.SubElement(servicios, "mensajes")
            ET.SubElement(mensajes, "Total").text = "{}".format(str(serv.positive+serv.negative+serv.neutral))
            ET.SubElement(mensajes, "Positivos").text = "{}".format(str(serv.positive))
            ET.SubElement(mensajes, "Negativos").text = "{}".format(str(serv.negative))
            ET.SubElement(mensajes, "Neutros").text = "{}".format(str(serv.neutral))
     
    ET.indent(root)
    

    return ET.tostring(root)
   
@app.route('/fast_analisis', methods=['POST'])
def read_datas():
    global fast_analisis, tokens_list_aux

    mensaje = ''

    fecha = ''
    red_social = ''
    usuario = ''

    sentimiento = ''

    cont_positivos = 0
    cont_negativos = 0

    xml = request.get_data().decode('utf-8')
    mydoc = minidom.parseString(xml)
    mensaje = mydoc.getElementsByTagName('mensaje')

    for texto in mensaje:
        txt = texto.firstChild.data
        txt = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", txt), 0, re.I)
        fast_analisis.append(txt)
    
    for cadena in fast_analisis:
        tokens = automata(cadena)
        tokens_list_aux.append(tokens)
    
    for lista in tokens_list_aux:
        msms,positivos,negativos,neutros,palabras = scanner(lista,manage.positive,manage.negative,None)
        cont_positivos += positivos
        cont_negativos += negativos
        mensaje = palabras

        for obj in msms:
            fecha = obj.fecha
            sentimiento = obj.estado
            red_social = obj.red_social
            usuario = obj.usuario

    total = cont_positivos + cont_negativos

    prctje_pos = (cont_positivos/total)*100
    prctje_neg = (cont_negativos/total)*100

    root = ET.Element("respuesta")
    ET.SubElement(root, "fecha").text = "{}".format(fecha)
    ET.SubElement(root, "red_social").text = "{}".format(red_social)
    ET.SubElement(root, "usuario").text = "{}".format(usuario)
    empresas = ET.SubElement(root, "empresas")

    for corp in corpse.corps:
        corp: Corp
        for word in mensaje:
            if word.upper() == corp.name:
                empresa = ET.SubElement(empresas, "empresa", nombre="{}".format(str(corp.name)))
        for serv in corp.services.servis:
            serv: Service
            for word in mensaje:
                if word.lower() == serv.name:
                    ET.SubElement(empresa, "servicio").text = "{}".format(str(serv.name))

    ET.SubElement(root, "palabras_positivas").text = "{}".format(str(cont_positivos))
    ET.SubElement(root, "palabras_negativas").text = "{}".format(str(cont_negativos))
    ET.SubElement(root, "sentimiento_positivo").text = "{}%".format(str(prctje_pos))
    ET.SubElement(root, "sentimiento_negativo").text = "{}%".format(str(prctje_neg))
    ET.SubElement(root, "sentimiento_analizado").text = "{}".format(str(sentimiento))
     
    ET.indent(root)

    return ET.tostring(root)

@app.route('/reset', methods=['POST'])
def reset_datas():
    global fast_analisis, tokens_list_aux
    global tokens_list,texto,msm_list
    global corpse,manage
    
    fast_analisis = []
    tokens_list_aux = []
    tokens_list = []
    texto = []
    msm_list = []

    corpse = Corps_List()
    manage = State()

    return jsonify({'ok' : True, 'msg':'La memoria se ha reseteado'}), 200

if __name__=='__main__':
    app.run(debug=True, port=4000)