
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
import overlap_mask as ovlp
from tqdm import tqdm

def load_im(file,band=[0,1,2]):
    #print("Image: " + file)
    array,name = load_file(file)
    
    array =  array[:,:,band]
    
    return(array,name)

def load_bin_mask(file):
    #print("Mask: " + file)
    array,name = load_file(file)
    if len(array.shape)>2:
        array = array[:,:,0]
    mask = np.expand_dims(array,axis=-1)/255
    
    mask[mask>0.5]  = 1 
    mask[mask<=0.5] = 0

    return(mask,name)

def tif2pixel(array):
    return(((array ** (1/2)) * 255).astype(np.uint8))


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def load_file(file):

    if not os.path.isfile(file):
        return(ValueError)
    
    file_type = file.split('.')[-1]

    if file_type=='tiff':
        array = np.array(Image.open(file)).astype(np.uint8)
    elif file_type=='tif':
         raster = rioxarray.open_rasterio(file)
         array  = tif2pixel(raster.values)
    elif(file_type=='png'):
        array = np.array(Image.open(file)).astype(np.uint8)
    else:
        array = np.load(file)
        array  = tif2pixel(array)

    # Get the dim order right: C,H,W
    if array.shape[-1]>array.shape[0]:
        array = array.transpose(1,2,0)


    name = file.split(os.sep)[-1].split('.')[0]
    return(array,name)

def concat_pair_PIL(src_img,src_msk):
    img,name = load_im(src_img)
    mask,name = load_bin_mask(src_msk)
    mask =(mask.squeeze()).astype(np.uint8)*255
    pil_mask = Image.fromarray(mask,'L')
    #pil_mask.show()
    pil_mask.convert(mode='RGB')
    #pil_mask.show()
    pil_img = Image.fromarray(img)
    concat_img = get_concat_h(pil_img,pil_mask)
    return(concat_img)
    #concat_img.show()
    concat_img.save(dst_img)

def get_data(src_dir):
    image_dir = os.path.join(src_dir,'images')
    mask_dir = os.path.join(src_dir,'masks')

    image_files = utils.get_files(image_dir)
    image_files['files'] = sorted(image_files['files'])

    mask_files = utils.get_files(mask_dir)
    mask_files['files'] = sorted(mask_files['files'])
    return(image_files,mask_files)

def main_concat_pair(src_dir):

    img_files, mask_files = get_data(src_dir)

    image_list= []
    name_list = []
    for im,mk in tqdm(zip(img_files['files'],mask_files['files'])):
        if im != mk:
            print("[ERROR] Different")
            continue

        src_img = os.path.join(img_files['root'],im) + '.' + img_files['file_type']
        src_msk = os.path.join(mask_files['root'],mk) + '.' + mask_files['file_type']
        

        concat_img = concat_pair_PIL(src_img,src_msk)
        image_list.append(concat_img)
        name_list.append(im)

    return(image_list,name_list)

        
def main_online_selection(src_dir):
    images,names = main_concat_pair(src_dir)

    file_to_remove = []

    
    for im,name in zip(images,names):
        im.show()
        input_char = input("Select: [s]")
        if input_char == 's':
           file_to_remove.append(name)
        
        import psutil
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()
    
    print("Files to remove: %d"%(len(file_to_remove)))
    
    return(file_to_remove)



def main_overlap_mask(src_dir,dst_dir):

    image_dir = os.path.join(src_dir,'png_images')
    mask_dir = os.path.join(src_dir,'masks')

    image_files = utils.get_files(image_dir)
    image_files_sorted = sorted(image_files['files'])
    mask_files = utils.get_files(mask_dir)
    mask_files_sorted = sorted(mask_files['files'])

    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)

    for im,mk in zip(image_files_sorted,mask_files_sorted):
        if im != mk:
            print("[ERROR] Different")
            continue
        src_img = os.path.join(image_files['root'],im) + '.' + image_files['file_type']
        src_msk = os.path.join(mask_files['root'],mk) + '.' + mask_files['file_type']
        dst_img = os.path.join(dst_dir,mk) + '.' + '.png'

        ovlp.main_overlap_mask(src_img,src_msk,dst_img)


if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--src',
                        default = '/home/tiago/learning/qtabaixo/x7/',
                        help='')
    parser.add_argument('--dst',
                        default = '/home/tiago/learning/qtabaixo/x7/',
                        help='')

    args = parser.parse_args()

    src_dir  = args.src
    dest_file = os.path.join(args.dst,'to_remove.txt')

    list_to_remove = main_online_selection(src_dir)

    with open(dest_file,'w') as f:
        f.write('\n'.join(list_to_remove))
    
    f.close()
    #main_overlap_mask(src_dir,dst_dir)
    

    










