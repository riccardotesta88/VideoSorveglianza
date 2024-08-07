from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from django.conf import settings

import os
import pandas as pd

from ..modelli.aree import *
from ..modelli.anagrafiche import *
from ..modelli.telecamere import Specifiche, Telecamera

# percorso elenchi
p_elenchi = getattr(settings, "BASE_DIR") + '/principale/scripts/elenchi/'


@login_required
def telecamere_modelli(request):
    file = 'modelli_tel.txt'
    print(f'{p_elenchi}{file}')
    fr = open(str(f'{p_elenchi}{file}'), 'r')

    lines = fr.readlines()
    objects = [k.modello for k in Specifiche.objects.all()]

    print(objects)

    for line in lines:
        if line not in objects:
            spec = Specifiche()
            spec.modello = line
            spec.identificativo = line
            spec.marche = 'Hikvision'
            spec.save()

        print(line)

    return redirect('/')


@login_required
def telecamere_punti(request):
    file = 'telecamere.csv'
    path = f'{p_elenchi}{file}'

    print(path)
    telecamere_data = pd.read_csv(path, delimiter=';')

    print(telecamere_data.head())

    objects = [(k.identificativo, k.luogo) for k in Telecamera.objects.all()]

    print(objects)

    for index, tel in telecamere_data[:].iterrows():
        if (tel['Host'], tel['Ubicazione']) not in objects:
            spec = Telecamera()
            spec.identificativo = tel['Host']
            spec.luogo = tel['Ubicazione']
            spec.collegamenti = '-'
            # foreign key specific modello
            # if tel['Modello']:
            #     print(tel['Modello'])
            #     spec.specifiche=Specifiche.objects.get(modello=tel['Modello'])

            spec.ip = str(tel['IP'])

            spec.save()

        print(tel)

    return redirect('/')
