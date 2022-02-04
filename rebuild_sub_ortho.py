
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

DEBUG_FLAG = True

def load_file(file_path,file_type):
    
    if file_type=='npy':
        data = np.load(file_path)
    elif file_type in ['tiff','tif','png']:
        data = np.array(Image.open(file_path))
    
    return(data.astype(np.uint8))

def show_info(n_sub_raster,n_sub_mask,matches):
    # plot info 
    # - qtd sub raster images
    # - qtd sub masks
    # - qtd matches
    #  
    print("="*50)
    print("Show Image Info: ")
    print("Sub raster files: %d"%(n_sub_raster))
    print("Sub mask files: %d"%(n_sub_mask))
    print("Matches: %d"%(len(matches)))
    print("Matched img: {}".format(matches))
    print("="*50)

def __FUNC__(traceback_call):
    import traceback
    stack = traceback.extract_stack()
    (filename, line, procname, name) = stack[-traceback_call]
    return(procname)

def debug_print(arg):
    if not DEBUG_FLAG:
        return()
    
    name = __FUNC__(3) 
    head = "[DEBUG] %s()"%(name)
    print(head)
    print(arg)
    print("[DEBUG] end")
    
def get_files(dir):
    '''
    return files in a directory
    @param dir (string) target direcotry
    @retrun (list): list of files  
    '''
    if not os.path.isdir(dir):
        return(list([]))

    files = os.listdir(dir)
    #if not end:
    new_files = [f.split('.')[0] for f in files]
    # Runs only when DEBUG FLAG == TRUE
    t = files[0].split('.')[1]
    return({'root':dir,'files':new_files,'type':t})

def match_sub_files(sub_raster_files,sub_mask_files):
    #  use sub_raster as reference
    matched_files = []
    for file in sub_mask_files:
        if file in sub_raster_files:
            matched_files.append(file)
    
    return(matched_files)
    
def parse_name(file):
    h,w = file.split('_')
    return(int(h),int(w))

def build_mask_(sub_files,target_height,target_width):
    '''
    Build mask function.

    @param sub_files (list): file list os the sub rasters
    @param target_height (int): target/output height 
    @param target_width (int): target/output width 
    '''
    raster_mask = np.zeros((target_height,target_width),dtype=np.uint8)
    for file in sub_files['files']:
        sub_im_file = os.path.join(sub_files['root'],file) + '.' + sub_files['type']
        #rgb_raster = rioxarray.open_rasterio(sub_im_file)
        mask_array = load_file(sub_im_file,sub_files['type'])
        # mask_array = np.array(Image.open(sub_im_file)).astype(np.uint8)
        h,w= mask_array.shape
        ph,pw = parse_name(file)
        lh,hh,lw,hw = ph,ph+h,pw,pw+w
        raster_mask[lh:hh,lw:hw] = mask_array
    
    return(raster_mask)


def main_rebuild_sub_ortho(src_raster_file,sub_raster_dir,sub_mask_dir,dest_file):
    '''
    Rebuild sub orthos. Used primarily to rebuild annotated mask

    @param: src_raster (string) file path to ortho with target size
    @param: sub_raster_dir (string) dir path to sub raster's directory
    @param: sub_mask_dir (string) dir path to sub mask's directory
    @param: dest_file (string) destination path 
    '''
    # get all sub raster files
    sub_raster_files = get_files(sub_raster_dir)
    # get all sub mask files
    sub_mask_files= get_files(sub_mask_dir)
    # match both file list

    if sub_raster_files == [] or sub_mask_files == []:
       raise EOFError("No files found")
        
    matches = match_sub_files(sub_raster_files['files'],sub_mask_files['files'])
    # Show Info
    show_info(len(sub_raster_files['files']),len(sub_mask_files['files']),matches)
    
    raster = rioxarray.open_rasterio(src_raster_file)
    target_height = raster.rio.height
    target_width = raster.rio.width
    # build raster 
    mask_raster = build_mask_(sub_mask_files,target_height,target_width)
    # Save mask
    mask_img = Image.fromarray(mask_raster)
    mask_img.save(dest_file)
    
    

if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--root',
                        default = '/home/tiago/greenai/dataset/QtaBaixo27Jul/x7',
                        help='')
    parser.add_argument('--sub_raster_dir',
                        default = 'annotation/sub_imgs',
                        help='')
    parser.add_argument('--sub_mask_dir',
                        default = 'annotation/sub_masks',
                        help='')
    parser.add_argument('--src_ortho_file',
                        default = 'OrthoRGBQtaBaixoJul27.tif',
                        help='')              
    parser.add_argument('--dest_file',
                        default = 'mask.png',
                        help='')
    args = parser.parse_args()

    root            = args.root
    src_ortho_file  = args.src_ortho_file 
    sub_raster_dir  = args.sub_raster_dir
    sub_mask_dir    = args.sub_mask_dir
    dest_file       = args.dest_file

    print("="*50)
    print("Root: " + root)
    print("Src Ortho File: " + src_ortho_file)
    print("Sub raster Dir: " + sub_raster_dir)
    print("Sub mask Dir: " + sub_mask_dir)
    print("Destination Mask: " + dest_file)
    print("="*50)

    
    src_raster      = os.path.join(root,src_ortho_file)
    sub_raster_dir  = os.path.join(root,sub_raster_dir)
    sub_mask_dir    = os.path.join(root,sub_mask_dir)
    dest_file       = os.path.join(root,dest_file)

    main_rebuild_sub_ortho(src_raster,sub_raster_dir,sub_mask_dir,dest_file)
    

    










