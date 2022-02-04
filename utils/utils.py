import os
import numpy as np
from PIL import Image

def preprocessing(img):
   
    img[img<=0]= 0
    nrom_bands = []
    for i,C in enumerate(img):
        C = normalize(C)

        nrom_bands.append(C)
    nrom_bands = tuple(nrom_bands)
    nrom_bands = np.stack(nrom_bands)
    #nrom_bands = nrom_bands.transpose(1,2,0)    
 
    return(nrom_bands)

def normalize(im):
    norm = (im - im.min()) / (im.max()-im.min())
    norm[norm<0.0] = 0.0
    norm[norm>1.0] = 1.0
    return norm

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
    return({'root':dir,'files':new_files,'file_type':t})



def match_files(sub_raster_files,sub_mask_files):
    #  use sub_raster as reference
    matched_files = []
    for file in sub_mask_files:
        if file in sub_raster_files:
            matched_files.append(file)
    
    return(matched_files)


def load_file(file_path,file_type):
    
    if file_type=='npy':
        data = np.load(file_path)
    elif file_type in ['tiff,tif,png']:
        data = np.array(Image.open(file_path))
    
    return(data.astype(np.uint8))

def build_global(file_structure):
    files = file_structure['files']
    root = file_structure['root']
    file_type = file_structure['file_type']
    return([os.path.join(root,f)+ '.' + file_type for f in files])

