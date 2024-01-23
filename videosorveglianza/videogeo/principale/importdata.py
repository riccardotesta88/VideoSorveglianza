import os

from django.conf import settings

world_shp = os.path.abspath(settings.BASE_DIR, 'data', 'TM_WORLD_BORDERS-0.3.shp')

from django.contrib.gis.gdal import DataSource

ds = DataSource(world_shp)
print(ds)
