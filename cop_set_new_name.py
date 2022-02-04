import argparse
import os 
import utils.utils as utils
import numpy as np
from PIL import Image 
import shutil

from utils import utils


def save_files(dst_path,files,matched_files):
    
    src_path = files['root']
    file_type = files['file_type']

    for file in files['files']:
        new_name = file.split('_')[-1]
        if not new_name in matched_files:
            continue
        
        src_f = os.path.join(src_path,file) + '.' + file_type

        dst_f = os.path.join(dst_path,new_name) + '.' + file_type
        shutil.copy(src_f, dst_f)


def find_positive_masks(mask_files):
    
    pos_files= {'root':'','files':[],'file_type':''}

    pos_files['root']=mask_files['root']
    pos_files['file_type']=mask_files['file_type']

    for file in mask_files['files']:
        # Load file
        f = os.path.join(mask_files['root'],file) + '.' + mask_files['file_type']

        mask_array = utils.load_file(f)
        #mask_array = np.array(Image.open(f)).astype(np.uint8)
        #print(mask_array)

        # verify if there are positive labels
        if (mask_array > 1).any():
            pos_files['files'].append(file)
    
    return(pos_files)
    

def match_file_names(img_files,mask_files):
    
    new_files_a = [int(file.split('_')[-1]) for file in img_files]
    new_files_b = [int(file.split('_')[-1]) for file in mask_files]
    
    unique_values,counts =np.unique(np.sort(np.append(new_files_a,new_files_b)),return_counts=True)
    matched_names = unique_values[counts==2]

    return([str(name) for name in matched_names])


# ar_unique = np.unique(ar,

def main_copy_set(src_dir,dst_dir):

    if not os.path.isdir(src_dir):
        return(NameError)
    
    # Build src files
    src_masks = os.path.join(src_dir,'masks')
    src_imgs = os.path.join(src_dir,'images')

    # Get src files
    src_mask_files = utils.get_files(src_masks)
    src_img_files = utils.get_files(src_imgs)

    matched_files = match_file_names(src_img_files['files'],src_mask_files['files'])
    print("Images: %d"%(len(src_img_files['files'])))
    print("Masks: %d"%(len(src_mask_files['files'])))
    print("Matched Files: %d"%len(matched_files))
    # find positive masks
    #pos_files = find_positive_masks(src_mask_files)
    #matched_mask_files = src_mask_files.copy()
    #pos_img_files  = pos_files.copy()
    #pos_img_files['root'] = src_img_files['root']
    
    
    #Build destination path
    dest_mask_dir= os.path.join(dst_dir,'masks')
    dest_img_dir= os.path.join(dst_dir,'images')

    if not os.path.isdir(dest_mask_dir):
        os.makedirs(dest_mask_dir)
    
    if not os.path.isdir(dest_img_dir):
        os.makedirs(dest_img_dir)

    print("Destination mask: " + dest_mask_dir)
    print("Destination mask: " + dest_img_dir)
    # Save files to dest dir
    save_files(dest_mask_dir,src_mask_files,matched_files)
    save_files(dest_img_dir,src_img_files,matched_files)






if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--source_dir',
                        default =  '/home/tiago/greenai/dataset/valdoeiro/altum/split',
                        help='')
    parser.add_argument('--dest_dir',
                        default = '/home/tiago/desktop_home/workspace/dataset/learning/valdoeiro/altum/',
                        help='')
            
    args = parser.parse_args()

    source_dir = args.source_dir
    dest_dir    = args.dest_dir


    print("="*50)
    print("Source file: %s"%(source_dir))
    print("Dest. directory: %s"%(dest_dir))
    print("="*50)


    main_copy_set(source_dir,dest_dir)
    