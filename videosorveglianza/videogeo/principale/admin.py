from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .modelli.anagrafiche import *
from .modelli.aree import *
from .modelli.telecamere import *

# from mapwidgets.widgets import GooglePointFieldWidget


# Register your models here.
admin.site.register(Persona)
admin.site.register(Contatti)
admin.site.register(Reperibilita)
admin.site.register(Soggetti)


class TelecameraAdmin(admin.ModelAdmin):
    """
    Telecamera Admin
    """
    list_display = ['identificativo', 'luogo', 'caratteristiche', 'campo_angolo']
    search_fields = ['luogo', 'caratteristiche', 'campo_angolo']
    list_filter = ('luogo', 'caratteristiche', 'campo_angolo')
    # prepopulated_fields = {'slug': ('first_name', 'last_name', 'title')}


admin.site.register(Geo, LeafletGeoAdmin)
admin.site.register(Accessibilita)
admin.site.register(Telecamera, LeafletGeoAdmin)


class PuntoAdmin(admin.ModelAdmin):
    search_fields = ['telecamere']
    list_display = ('identificativo', 'get_telecamere',)


admin.site.register(Punto, PuntoAdmin)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ['punti']
    list_display = ("title", "get_punti", 'get_telecamere',)
    autocomplete_fields = ['punti']
    pass


admin.site.register(Manutenzione)
admin.site.register(Installatori)


@admin.register(Specifiche)
class SpecificheAdmin(admin.ModelAdmin):
    pass
