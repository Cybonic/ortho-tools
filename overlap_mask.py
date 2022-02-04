
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
import math
import numpy as np
import rioxarray 
import matplotlib.image as saver
import progressbar
import utils.utils as utils
from tqdm import tqdm
from PIL import Image
import numpy as np
import argparse
import utils.tif_utils as tifu 

def tif2png(tifarray):
    array = tifarray.values
    array = np.transpose(array,(1,2,0))
    tif = ((array ** (1/4)) * 255).astype(np.uint8)
    
    return(tif)

def overlap_mask(img,mask_img,label,transp):
    '''
    @brief: overlap image with the mask 
    overlap_mask(img,mask_img,label,transp)

    @param img (PIL Image)
    @param mask_img (PIL Image)
    @param label (int) label to be overlaped with the image
    @param transp (int) range ->[0:255] 
    @return image (PIL Image) 
    
    '''
    
    mask_array = conv_mask_to_array(mask_img).squeeze().astype(np.uint8)
    
    unique_class = np.unique(mask_array).astype(np.uint)
    if not label in unique_class:
        return(ValueError)

    new_mask_array = np.ones(mask_array.shape[0:2]).astype(np.uint8)*255

    new_mask_array[mask_array == label] = transp
    mask_img = Image.fromarray(new_mask_array)
    #mask_array = np.asarray(mask_img)
    imga = img.copy()
    imga.putalpha(mask_img)

    return(imga)

def conv_mask_to_array(img_mask):
    '''
    @brief:  array_mak = conv_mask_to_array(img_mask):
    @param img_mask (PIL.Image): mask
    @return: (numpy) mask as an numpy array
    
    '''
    mask_array = np.asarray(img_mask)[:,:,0]
    img_labels = np.unique(mask_array)
    un_img_labels = np.unique(img_labels)

    n_class = list(range(len(un_img_labels)))

    new_mask = np.zeros(mask_array.shape)
    for i_c, c in zip(un_img_labels,n_class):
        new_mask[mask_array==i_c] = c
    
    new_mask = np.expand_dims(new_mask,axis=-1)
    return(new_mask)


def show_img_info(image):
    print("Show Image Info: ")
    print("Width    {}".format(image.size[1]))
    print("Height   {}".format(image.size[0]))


def main_overlap_mask(tif_file,mask_file,dest_file):

    rgb_raster = Image.open(tif_file)
    mask_img = Image.open(mask_file)

    print("="*50)
    print("Tif File: %s"%(tif_file))
    show_img_info(rgb_raster)
    print("Mask File: %s"%(mask_file))
    show_img_info(mask_img)
    print("="*50)

    # Convert Raster to array
    #img_array = tif2png(rgb_raster)
    #img_array = np.transpose(img_array, (1, 2, 0))
    img_array = np.array(rgb_raster)
    im_rgb    = Image.fromarray(img_array).copy()
    
    im_rgba = overlap_mask(im_rgb,mask_img,0,10)
    
    im_rgba.save(dest_file)
    

if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--tif_file',
                        default = '/home/tiago/greenai/dataset/QtaBaixo27Jul/altum/images_test/00000_00000.tiff',
                        help='')
    parser.add_argument('--mask_file',
                        default = '/home/tiago/greenai/dataset/QtaBaixo27Jul/altum/masks/00000_00000.tiff',
                        help='')

    parser.add_argument('--dest_file',
                        default = 'image.png',
                        help='')
    args = parser.parse_args()

    tif_file  = args.tif_file
    mask_file = args.mask_file
    dest_file = args.dest_file


    main_overlap_mask(tif_file,mask_file,dest_file)
    

    










