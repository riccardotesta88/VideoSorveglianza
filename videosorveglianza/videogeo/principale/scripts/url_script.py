import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from ..modelli.aree import *
from ..modelli.anagrafiche import *
from ..modelli.telecamere import *
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

ABSPATH = "/home/master/videosorveglianza/videogeo/principale/scripts/"


def loadTele_fromJson(request):
    data = openJson()
    print(data)
    context = {}
    template = loader.get_template('dashboard/index.html')

    entries = data

    for e in entries:
        ent = e['data']

        tele = Telecamera()
        tele.identificativo = ent['TELECAMERA']
        tele.tipologia = ent['Tipologia']
        tele.luogo = ent['Dati di Geolocalizzazine']
        if (e['GPS']):
            tele.longitude, tele.latitude = e['GPS'][0], e['GPS'][1]
        tele.caratteristiche = ent['Caratteristiche Tecniche']
        angolo = ent['Superficie di visibilit\u00e0'][6:-1]
        tele.campo_angolo = float(angolo)
        tele.save()

    return HttpResponse(template.render(context, request))


def openJson(filename=""):
    if not filename:
        print('File base lettura per elenco telecamere')
        filename = (ABSPATH + 'repo/telecamere.json')
        print(filename)

    with open(filename, 'r+') as json_file:
        data = json.load(json_file)
        return data


def menu(request):
    template = loader.get_template('landing-page.html')

    print('Scegli la routine:')
    print('1 - Load telecamere da file json')

    routine = input()

    if routine == 1:
        loadTele_fromJson()

    else:
        print('Comando non presente - digitare exit per uscire')

        if (input() == 'exit'):
            exit()
        else:
            menu()
