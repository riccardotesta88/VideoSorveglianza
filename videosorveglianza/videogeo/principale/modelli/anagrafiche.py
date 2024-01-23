from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from phone_field import PhoneField  # Gestione campo telefono
from simple_history.models import HistoricalRecords

DEFAULTPOINT = Point(8.466667, 44.683333, srid=4326)


###
# ANAGRAFICA PROPRIETA

class Persona(models.Model):
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = "Persone"

    '''
    Definizione delle persone
    '''
    nome = models.CharField(max_length=40, default='')
    cognome = models.CharField(max_length=40, default='')
    TIPI = (('IST', 'Istituzionale'), ('TEC', 'Tecnico'),)
    tipologia = models.CharField(choices=TIPI, max_length=20, default="")

    def __str__(self):
        return self.nome + " " + self.cognome


class Installatori(models.Model):
    class Meta:
        verbose_name = 'Installatore - Società o persona'
        verbose_name_plural = "Installatori - Società o persona"

    '''
    Definizione delle informazioni dell'installatore
    '''
    soggetto = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, help_text='Indicazioni dell\'installatore')
    data_installazione = models.DateField(default=200001)

    def __str__(self):
        return self.installatore.name + " " + self.installatore.cognome


class Manutenzione(models.Model):
    class Meta:
        verbose_name = 'Manutenzione - Società o persona'
        verbose_name_plural = "Manutenzioni - Società o persona"

    '''
       Definizione delle informazioni del manutentore
       '''
    manutenzione_ditta = models.CharField(max_length=200, default="", help_text='Estremi ditta')
    manutenzione_persona = models.ManyToManyField(Persona, help_text='Indicazioni del manutentore')
    manutenzione_utltimo_intervento = models.DateField(auto_now=False)

    def __str__(self):
        return self.manutenbzione_persona.nome + " " + self.manutenbzione_persona.ncognome


class Contatti(models.Model):
    '''
    Definizione dei contatti per raggiungere il soggetto
    '''
    nominativo = models.ManyToManyField(Persona)
    telefono = PhoneField(blank=False, help_text='Recapito telefonico fisso')
    mobile = PhoneField(blank=True, help_text='Recapito telefonico mobile', )
    mail = models.EmailField(blank=True)
    mail_pec = models.EmailField(blank=True)
    altro_recapito = models.TextField(blank=False, default='', help_text='Eventuale altro recapito')
    is_legal = models.BooleanField(default=False, help_text='Selezionare se il contatto è un contatto LEGALE')
    is_tecnical = models.BooleanField(default=False, help_text='Selezionare se il contatto è un contatto TECNICO')

    def __str__(self):
        return str(self.telefono) + " " + str(self.mobile) + " " + self.mail


class Reperibilita(models.Model):
    '''
    Definizione
    '''
    persona = models.ForeignKey(Contatti, on_delete=models.DO_NOTHING, blank=True)
    reperibilita = models.TextField(default='', help_text='Indicare orari di reperibilità')

    def __str__(self):
        return self.persona.nome + " " + self.persona.cognome + ' ' + self.reperibilita[:20]


class Soggetti(models.Model):
    class Meta:
        verbose_name = 'Elenco soggetti'
        verbose_name_plural = "Elenco soggetti proprietari"

    TIPI = (('PB', 'Pubblico'), ('PR', 'Privato'), ('AZ', 'Azienda'))

    identificativo = models.CharField(max_length=50, default="",
                                      help_text='Denominazione, per i privati cognome e cognome. Es Mario Rossi')
    tipologia = models.CharField(choices=TIPI, max_length=15, default="Pubblico")
    referenti = models.ManyToManyField(Persona, help_text='<strong>Indicare i soggetti referenti</strong><br>')
    contatti_legali = models.ManyToManyField(Contatti, blank=True,
                                             help_text='<strong>Contatti legali del soggetto</strong><br>')

    history = HistoricalRecords()

    def __str__(self):
        return self.identificativo

###
######## END --- ANAGRAFICA PROPRIETA
