# Load django-wms classes
from wms import *

# Load model with spatial field (Point, Polygon, MultiPolygon)
from .models import Geo


# Subclass the WmsLayer class and point it to a spatial model
# use WmsVectorLayer for vector data and WmsRasterLayer for rasters
class MyWmsLayer(layers.WmsVectorLayer):
    model = Geo


# Subclass the WmsMap class and add the layer to it
class MyWmsMap(maps.WmsMap):
    layer_classes = [MyWmsLayer]


# Subclass the WmsView to create a view for the map
class MyWmsView(views.WmsView):
    map_class = MyWmsMap
