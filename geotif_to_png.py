
# https://geoscripting-wur.github.io/PythonRaster/
# https://rasterio.readthedocs.io/en/latest/topics/overviews.html
# https://gis.stackexchange.com/questions/5701/differences-between-dem-dsm-and-dtm/5704#5704
# https://geoscripting-wur.github.io/PythonRaster/

# https://carpentries-incubator.github.io/geospatial-python/aio/index.html

# =====================================================================
# Date: 02/09/2021
# Author: Tiago B.
#
# Split a raster into subimages
#  
import os
import numpy as np
import rioxarray 
import rasterio
from rasterio.plot import show
import matplotlib.image as saver
import progressbar
import utils.utils as utils
from PIL import Image
import argparse


'''
# File 
source_path = '/home/tiago/greenai/dataset/QtaBaixo27Jul/altum/images_test_tiff/00000_00000.tif'
dest_path =  '/home/tiago/greenai/dataset/QtaBaixo27Jul/altum/'
OUTPUT_NAME = 'OrthoAltumQtaBaixoJul27'
# open file
raster = rioxarray.open_rasterio(source_path)

print(raster.rio.crs)
print(raster.rio.nodata)
print(raster.rio.bounds())
print(raster.rio.width)
print(raster.rio.height)

width = raster.rio.width 
height = raster.rio.height 


array = np.array(raster.values)

print(array.max())
print(array.min())
bands = [0,1,2]


#target_bands = array[bands,:,:]
target_bands = np.transpose(array,(1,2,0))

array = (utils.preprocessing(target_bands)*255).astype(np.uint8)
print(array.max())
print(array.min())



target_img = Image.fromarray(target_bands)

target_img.save(os.path.join(dest_path,OUTPUT_NAME + '.png'))

'''


def tif2png(tifarray):
    array = tifarray.values
    array = np.transpose(array,(1,2,0))
    tif = ((array ** (1/4)) * 255).astype(np.uint8)
    
    return(tif)

def conv_tif_to_png(file,bands=[0,1,2]):
    
    raster = rioxarray.open_rasterio(file)
    image = tif2png(raster)
    image = image[:,:,bands]
    image = Image.fromarray(image)
    return(image)


def main_conv_to_png(src,dst):
    # Get src files
    src_files = utils.get_files(src)

    if not os.path.isdir(dst):
        os.mkdir(dst)

    for file in src_files['files']:
        file_name = os.path.join(src_files['root'],file) + '.' + src_files['file_type']
        image = conv_tif_to_png(file_name)
        dest_file = os.path.join(dst,file) + '.' + 'png'
        image.save(dest_file)



if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--source_dir',
                        default =  '/home/tiago/learning/qtabaixo/altum/images',
                        help='')
    parser.add_argument('--dest_dir',
                        default = '/home/tiago/learning/qtabaixo/altum/png_images',
                        help='')

    args = parser.parse_args()

    source_dir = args.source_dir
    dest_dir    = args.dest_dir
    
    main_conv_to_png(source_dir,dest_dir)

'''
if array.shape[0]==1:
    array = utils.normalize(array) 
    array= array.squeeze()
    array = np.stack((array,array,array),axis=0)
else:
    # if array.shape[0]==6: # DSM
    array = array.transpose(1,2,0)
    rgb = array[:,:,bands]
    if array.shape[0]==6:
        for c in range(0,rgb.shape[2]):
            rgb[:,:,c] = utils.normalize(rgb[:,:,c])
        rgb = np.array(rgb*255,dtype=np.uint8)
    array = rgb


target_width  = 240 
target_height = 240 

max_itr = height
print(max_itr)
file_name = source_path.split('.')[0] + '.png'
#img_path = os.path.join(dest_path,"%05d_%05d.png"%(h_itr,w_itr))
saver.imsave(file_name, array)

'''










