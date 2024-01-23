from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.template import loader

from .forms import PuntoForm
from .modelli.aree import *
from .modelli.telecamere import *

ACQUI = Point(8.466667, 44.683333, srid=4326)


@login_required(login_url='/accounts/login/')
def test(request):
    places = Area.objects.filter(proprietario__area__isnull=False).all()

    punto = PuntoForm()
    template = loader.get_template('dashboard/index.html')
    mex = []
    mex.append({
        'level': 'danger',
        'title': "HTOP",
        'message': 'Haloworld'
    })
    mex.append({
        'level': 'primary',
        'title': "HTOP",
        'message': 'Haloworld'
    })

    pnt = GEOSGeometry(ACQUI, srid=4326)
    gs = Telecamera.objects.filter(point__distance_lte=(pnt, D(km=1)))

    context = {'punto': punto, 'mex': mex, 'places': places, 'puntos': gs}

    return HttpResponse(template.render(context, request))


def presentation(request):
    template = loader.get_template('landing-page.html')
    context = {}

    return HttpResponse(template.render(context, request))
