from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import views as viste

from .scripts import url_script as script
from .scripts import importdataexternal as importerdata
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
                  path('', viste.presentation, name='Home_landing'),
                  path('test/', viste.test, name='Test page'),
                  # re_path('db/load', script.loadTele_fromJson, name='Script functions'),
                  path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('models/load', importerdata.telecamere_modelli, name="Modelli telecamere"),
                  path('punti/load', importerdata.telecamere_punti, name="Punti telecamere")

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
