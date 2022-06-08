
# https://geoscripting-wur.github.io/PythonRaster/
# https://rasterio.readthedocs.io/en/latest/topics/overviews.html
# https://gis.stackexchange.com/questions/5701/differences-between-dem-dsm-and-dtm/5704#5704
# https://geoscripting-wur.github.io/PythonRaster/


# =====================================================================
# Raster Visualization demo using rasterio lib

import numpy as np
import rasterio
from rasterio.plot import show
import os
import matplotlib.pyplot as plt
import rioxarray
import tifffile
from PIL import Image



file_path = '/media/tiago/vbig/dataset/greenAI/Satelite_alta_resolucao/Satelite_alta_resolução/esac/IMG_PHR1B_PMS_202009301132105_ORT_2e86f0c6-3174-476c-c77b-433fd389463f-001_R1C1.TIF'
img_path = '/home/tiago/dsm.tif'
tiff_list = []

src = rasterio.open(file_path)
# arr = os.listdir(file_path)
raster = rioxarray.open_rasterio(file_path).squeeze()

print(f"Raster shape: {raster.shape}")
print(np.array(raster.data).max())
print(np.array(raster.data).min())


#histogram, bin_edges = np.histogram(raster.data, bins=100, range=(-40000, 100))

#plt.plot(bin_edges[0:-1], histogram)  # <- or here
#plt.show()


# Rescale
raster.data[raster.data<0] = 0
histogram, bin_edges = np.histogram(raster.data, bins=100, range=(0, 255))


plt.plot(bin_edges[0:-1], histogram)  # <- or here
plt.show()

image =(raster.data/np.max(raster.data))*255



image = 255 - image
print(image.max())
print(image.min())



image = Image.fromarray(image)
newsize = (1000,1000)
image = image.resize(newsize)

image.convert('L')
image.show()
image.save("/home/tiago/dsm.tiff")
# tifffile.imsave(img_path, raster.data)
#f, ax = plt.subplots(figsize=(10, 5))
raster.plot()
#plt.show()

# show(raster, title='Digital Surface Model', cmap='gist_ncar')






