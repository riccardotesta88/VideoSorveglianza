from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from phone_field import PhoneField  # Gestione campo telefono
from select_multiple_field.codecs import *
from simple_history.models import HistoricalRecords

DEFAULTPOINT = Point(8.466667, 44.683333, srid=4326)


###
# ANAGRAFICA PROPRIETA

class Persona(models.Model):
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
    '''
    Definizione delle informazioni dell'installatore
    '''
    soggetto = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, help_text='Indicazioni dell\'installatore')
    data_installazione = models.DateField(default=200001)

    def __str__(self):
        return self.installatore.name + " " + self.installatore.cognome


class Manutenzione(models.Model):
    '''
       Definizione delle informazioni del manutentore
       '''
    manutenzione_ditta = models.CharField(max_length=200, default="", help_text='Estremi ditta')
    manutenzione_persona = models.ManyToManyField(Persona, help_text='Indicazioni del manutentore')
    manutenzione_utltimo_intervento = models.DateField(auto_now=False)

    def __str__(self):
        return self.manutenbzione_persona.nome + " " + self.manutenbzione_persona.ncognome


class Reperibilita(models.Model):
    '''
    Definizione
    '''
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, blank=True)
    reperibilita = models.TextField(default='', help_text='Indicare orari di reperibilità')

    def __str__(self):
        return self.persona.nome + " " + self.persona.cognome + ' ' + self.reperibilita[:20]


class Contatti(models.Model):
    '''
    Definizione dei contatti per raggiungere il soggetto
    '''
    telefono = PhoneField(blank=False, help_text='Recapito telefonico fisso')
    mobile = PhoneField(blank=True, help_text='Recapito telefonico mobile', )
    mail = models.EmailField(blank=True)
    mail_pec = models.EmailField(blank=True)
    altro_recapito = models.TextField(blank=False, default='', help_text='Eventuale altro recapito')
    is_legal = models.BooleanField(default=False, help_text='Selezionare se il contatto è un contatto LEGALE')
    is_tecnical = models.BooleanField(default=False, help_text='Selezionare se il contatto è un contatto TECNICO')

    def __str__(self):
        return str(self.telefono) + " " + str(self.mobile) + " " + self.mail


class Soggetti(models.Model):
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


###
# ANAGRAFICA AREE
class Tecniche(models.Model):
    MARCHE = (('Mobotix', 'Mobotix'), ('Dahua', 'Dahua'), ('Hikvision', 'Hikvision'), ('Avigilon', 'Avigilon'))
    VISIONE = (('Notte', 'Notturna'), ('Giorno', 'Diurna'))

    identificativo = models.CharField(max_length=50, default="",
                                      help_text='Descrizione posizione')
    marche = models.CharField(choices=MARCHE, max_length=20, default="", help_text='Marca')
    modello = models.CharField(max_length=20, default="", help_text='Modello')
    campo_profondita = models.FloatField(blank=True, default=0, help_text='Indicare valore in metri')
    campo_angolo = models.FloatField(blank=True, default=0, help_text='Indicare valore in gradi')

    # Returns the string representation of the model.
    def __str__(self):
        return self.indirizzo + " " + self.citta


class Geo(models.Model):
    # indirizzo = AddressField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri', on_delete=models.DO_NOTHING)
    indirizzo = models.CharField(max_length=200, default='', help_text='Indirizzo, max:200 caratteri, ES: via roma 1')
    citta = models.CharField(max_length=200, default='', help_text='Città, max:200 caratteri')
    coordinate = PointField(help_text='Latitudine e longitudine', default=DEFAULTPOINT)

    # Returns the string representation of the model.
    def __str__(self):
        return self.indirizzo + " " + self.citta


class Accessibilita(models.Model):
    descrizione = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')
    referente = models.ManyToManyField(Persona, blank=True, help_text='<strong>Propeitario dell\'impianto</strong><br>')
    dove = models.ForeignKey(Geo, on_delete=models.DO_NOTHING, blank=True)
    modalita = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')
    tempistiche = models.CharField(max_length=200, default='', help_text='Descrizione area, max:200 caratteri')

    # Returns the string representation of the model.
    def __str__(self):
        return self.descrizione


class Telecamera(models.Model):
    COLLEGAMENTI = (('Cavo', 'Via cavo'), ('Radio', 'Wireless'), ('Altro', 'Altro'))
    VISIONE = (('Notte', 'Notturna'), ('Giorno', 'Diurna'), ('Entrambe', 'D/N'))

    identificativo = models.CharField(max_length=50, default="",
                                      help_text='Descrizione posizione')
    collegamenti = models.CharField(choices=COLLEGAMENTI, max_length=20, default="", help_text='Collegamento')
    visione = models.CharField(choices=VISIONE, max_length=20, default="", help_text='Visione D/N')
    campo_profondita = models.FloatField(blank=True, default=0, help_text='Indicare valore in metri')
    campo_angolo = models.FloatField(blank=True, default=0, help_text='Indicare valore in gradi')
    orientamento = models.FloatField(blank=True, default=0,
                                     help_text='Indicare valore in gradi rispetto all\'asse Nord/Sud')

    immagine = models.ImageField(blank=True)
    ip = models.IPAddressField(blank=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.identificativo


class Punto(models.Model):
    identificativo = models.CharField(max_length=50, default='', help_text='Inserisci identificativo')
    # descrizione_punto = models.CharField(max_length=150,default='', blank=True,help_text='Inserisci descrizione del punto')
    posizione = models.ManyToManyField(Geo)
    telecamere = models.ManyToManyField(Telecamera, help_text='<strong>Punti del sistema</strong><br>')
    n_telecamere = models.IntegerField(default=0)

    # Returns the string representation of the model.
    def __str__(self):
        return self.identificativo

    '''def save(self):
        tel_n=0
        for t in self.telecamere:
            tel_n=+1
            
        self.n_telecamere=tel_n
        self.save()

        super(self)'''


class Area(models.Model):
    title = models.CharField(max_length=40, default='', help_text='Identificativo area, max:40 caratteri')
    descrizione = models.CharField(max_length=200, default='', help_text='Descrizione dell\'area, max:200 caratteri')
    proprietario = models.ManyToManyField(Soggetti, blank=True,
                                          help_text='<strong>Propeitario dell\'impianto</strong><br>')
    punti = models.ManyToManyField(Punto, blank=True, help_text='<strong>Punti del sistema</strong><br>')

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

###
####### END - ANAGRAFICA PROPRIETA
