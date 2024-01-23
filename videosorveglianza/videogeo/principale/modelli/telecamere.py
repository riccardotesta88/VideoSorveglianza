from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from simple_history.models import HistoricalRecords

# Modelli locali dei dati
from .aree import *

DEFAULTPOINT = Point(8.466667, 44.683333, srid=4326)


###
# ANAGRAFICA AREE
class Specifiche(models.Model):
    class Meta:
        verbose_name = "Specifica"
        verbose_name_plural = "Specifiche"

    MARCHE = (('Mobotix', 'Mobotix'), ('Dahua', 'Dahua'), ('Hikvision', 'Hikvision'), ('Avigilon', 'Avigilon'))
    VISIONE = (('Notte', 'Notturna'), ('Giorno', 'Diurna'))

    identificativo = models.CharField(max_length=50, default="",
                                      help_text='Descrizione posizione')
    marche = models.CharField(choices=MARCHE, max_length=20, default="", help_text='Marca')
    modello = models.CharField(max_length=30, default="", help_text='Modello')
    campo_profondita = models.FloatField(blank=True, default=0, help_text='Indicare valore in metri')
    campo_angolo = models.FloatField(blank=True, default=0, help_text='Indicare valore in gradi')

    # Returns the string representation of the model.
    def __str__(self):
        return f'{self.marche} - {self.identificativo}'


class Telecamera(models.Model):
    class Meta:
        verbose_name = "Telecamera"
        verbose_name_plural = "Telecamere"

    COLLEGAMENTI = (('-', '-'), ('Cavo', 'Via cavo'), ('Radio', 'Wireless'), ('Altro', 'Altro'))
    VISIONE = (('Notte', 'Notturna'), ('Giorno', 'Diurna'), ('Entrambe', 'D/N'))

    identificativo = models.CharField(max_length=50, default="",
                                      help_text='Descrizione posizione')
    collegamenti = models.CharField(choices=COLLEGAMENTI, max_length=20, default="", help_text='Collegamento')
    visione = models.CharField(choices=VISIONE, max_length=20, default="", help_text='Visione D/N')
    campo_profondita = models.FloatField(blank=True, default=0, help_text='Indicare valore in metri')
    campo_angolo = models.FloatField(blank=True, default=0, help_text='Indicare valore in gradi')
    orientamento = models.FloatField(blank=True, default=0,
                                     help_text='Indicare valore in gradi rispetto all\'asse Nord/Sud')
    tipologia = models.CharField(max_length=100, default="",
                                 help_text='Tipologia telecamera', blank=True)
    immagine = models.ImageField(blank=True)

    latitude = models.FloatField(default='0.0', blank=True)
    longitude = models.FloatField(default='0.0', blank=True)

    point = PointField(help_text='Latitudine e longitudine', default=DEFAULTPOINT)

    luogo = models.CharField(max_length=100, default="",
                             help_text='Luogo', blank=True)
    caratteristiche = models.CharField(max_length=100, default="",
                                       help_text='Caratteristiche tecniche', blank=True)

    specifiche = models.ForeignKey(Specifiche, on_delete=models.SET_NULL, null=True, blank=True)

    ip = models.GenericIPAddressField(default='0.0.0.0')

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.luogo} - {self.ip} - {self.identificativo}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.point == DEFAULTPOINT:
            lat, long = self.point
            self.latitude = lat
            self.longitude = long

        super(Telecamera, self).save()

    def staticObject():
        # Invoca staticamente un oggetto per la creazione di default
        DEFAULTGEO = Geo()
        DEFAULTGEO.coordinate = DEFAULTPOINT

        return DEFAULTGEO

###
####### END - ANAGRAFICA PROPRIETA
