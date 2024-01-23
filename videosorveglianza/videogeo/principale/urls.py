from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .scripts import url_script as script
from .scripts import importdataexternal as importerdata

urlpatterns = [
                  # re_path('', views.presentation, name='Landing pag'),
                  # re_path('test/', views.test, name='Test page'),
                  # re_path('db/load', script.loadTele_fromJson, name='Script functions'),
                  path('models/load', importerdata.telecamere_modelli, name="Modelli telecamere"),
                  path('punti/load', importerdata.telecamere_punti, name="Punti telecamere")

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
