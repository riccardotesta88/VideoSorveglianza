from django import forms

from .modelli.aree import *
from .modelli.telecamere import *


class PuntoForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('title', 'descrizione', 'punti', 'proprietario',)
        widget = forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500})


class TelecameraForm(forms.ModelForm):
    point = forms.PointField(widget=
                             forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

    class Meta:
        model = Telecamera
        fields = ()
