from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point

from .telecamere import *

DEFAULTPOINT = Point(8.466667, 44.683333, srid=4326)


class Geo(models.Model):
    # indirizzo = AddressField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri', on_delete=models.DO_NOTHING)
    indirizzo = models.CharField(max_length=200, default='', help_text='Indirizzo, max:200 caratteri, ES: via roma 1')
    citta = models.CharField(max_length=200, default='', help_text='Città, max:200 caratteri')
    coordinate = PointField(help_text='Latitudine e longitudine', default=DEFAULTPOINT)

    # Returns the string representation of the model.
    def __str__(self):
        return self.indirizzo + " " + self.citta

    def staticObject():
        # Invoca staticamente un oggetto per la creazione di default
        DEFAULTGEO = Geo()
        DEFAULTGEO.coordinate = DEFAULTPOINT

        return DEFAULTGEO


class Accessibilita(models.Model):
    descrizione = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')
    referente = models.ManyToManyField(Persona, blank=True, help_text='<strong>Propeitario dell\'impianto</strong><br>')
    dove = models.ForeignKey(Geo, on_delete=models.DO_NOTHING, blank=True)
    modalita = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')
    tempistiche = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')

    # Returns the string representation of the model.
    def __str__(self):
        return self.descrizione


class Punto(models.Model):
    identificativo = models.CharField(max_length=50, default='', help_text='Inserisci identificativo')
    # descrizione_punto = models.CharField(max_length=150,default='', blank=True,help_text='Inserisci descrizione del punto')
    posizione = models.ManyToManyField(Geo, blank=True, null=True)
    telecamere = models.ManyToManyField(Telecamera, blank=True, null=True,
                                        help_text='<strong>Punti del sistema</strong><br>')
    n_telecamere = models.IntegerField(default=0, blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return self.identificativo

    def save(self):
        n = len(self.telecamere.all())
        self.n_telecamere = n

        super(Punto, self).save()

    def get_telecamere(self):
        points = [p.__str__() for p in self.telecamere.all()]
        print(points)
        return "\n".join(points)


class Area(models.Model):
    title = models.CharField(max_length=40, default='', help_text='Identificativo area, max:40 caratteri')
    descrizione = models.CharField(max_length=200, default='', help_text='Descrizione dell\'area, max:200 caratteri')
    proprietario = models.ManyToManyField(Soggetti, blank=True,
                                          help_text='<strong>Propeitario dell\'impianto</strong><br>')
    punti = models.ManyToManyField(Punto, blank=True, null=True, help_text='<strong>Punti del sistema</strong><br>',
                                   related_name='rel_telecamere')

    TIPI = (('CAV', 'Cavo'), ('WIR', 'Wireless'), ('FIB', 'Fibra'), ('LOC', 'Locale'), ('NES', 'Nessuno'),)
    DEFCHOICE = ('NES', 'Nessuno')

    tipologia_collegamenti = models.CharField(choices=TIPI, max_length=10, default=DEFCHOICE)

    installatore = models.ManyToManyField(Installatori, blank=True,
                                          help_text='<strong>Propeitario dell\'impianto</strong><br>')

    manutenzione = models.ManyToManyField(Manutenzione, blank=True,
                                          help_text='<strong>Propeitario dell\'impianto</strong><br>')

    class Meta:
        ordering = ('title',)

    # Returns the string representation of the model.
    def __str__(self):
        return self.title

    def get_punti(self):
        points = [p.identificativo for p in self.punti.all()]
        print(points)
        return "<br>".join(points)

    def get_telecamere(self):
        points = [p.__str__() for p in (p.telecamere for p in self.punti.all())]
        print(points)
        return "<br>".join(points)

###
####### END - ANAGRAFICA PROPRIETA
