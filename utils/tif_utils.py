'''

https://gis.stackexchange.com/questions/57005/python-gdal-write-new-raster-using-projection-from-old


'''

import yaml
import os
#import rasterio
import numpy as np
import tifffile


def show_raster_info(raster):
    print("Geotiff information: ")
    print("CRS      {}".format(raster.rio.crs))
    print("NODATA   {}".format(raster.rio.nodata))
    print("Bounds   {}".format(raster.rio.bounds()))
    print("Width    {}".format(raster.rio.width))
    print("Height   {}".format(raster.rio.height))

def tiff2numpy(tiff):
    return(np.array(tiff.values))