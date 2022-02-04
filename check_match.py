import argparse
import os 
import utils.utils as utils
import numpy as np
from PIL import Image 
import shutil

def save_files(dst_path,files):
    
    src_path = files['root']
    file_type = files['file_type']

    for file in files['files']:
        src_f = os.path.join(src_path,file) + '.' + file_type
        #img = Image.open(src_f)
        dst_f = os.path.join(dst_path,file) + '.' + file_type
        shutil.copy(src_f, dst_f)
        #img.save(dst_f)


def match_img_mask(img_files,mask_files):
    
    
    mask_outliers,img_outliers = [],[]
    for file in mask_files:
        # Load file
        if not file in img_files:
            mask_outliers.append(file)
    
    for file in img_files:
        # Load file
        if not file in mask_files:
            img_outliers.append(file)
    
    print("masks not matched %d"%(len(mask_outliers)))
    print("img not matched %d"%(len(img_outliers)))

    




def main_set_selection(src_dir,dst_dir):

    if not os.path.isdir(src_dir):
        return(NameError)
    
    # Build path of src files
    src_masks = os.path.join(src_dir,'masks')
    src_imgs = os.path.join(src_dir,'images')

    # Get src files
    src_mask_files = utils.get_files(src_masks)
    src_img_files = utils.get_files(src_imgs)

    # find positive masks
    pos_files = match_img_mask(src_img_files['files'],src_mask_files['files'])
    pos_mask_files = pos_files.copy()
    pos_img_files  = pos_files.copy()
    pos_img_files['root'] = src_img_files['root']
    
    
    #Build destination path
    dest_mask_dir= os.path.join(dst_dir,'masks')
    dest_img_dir= os.path.join(dst_dir,'images')

    if not os.path.isdir(dest_mask_dir):
        os.makedirs(dest_mask_dir)
    
    if not os.path.isdir(dest_img_dir):
        os.makedirs(dest_img_dir)

    # Save files to dest dir
    save_files(dest_mask_dir,pos_mask_files)
    save_files(dest_img_dir,pos_img_files)






if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--source_dir',
                        default =  '/home/tiago/desktop_home/workspace/dataset/learning/valdoeiro/altum',
                        help='')
    parser.add_argument('--dest_dir',
                        default = '/home/tiago/greenai/dataset/esac/altum/paper_set/',
                        help='')
            
    args = parser.parse_args()

    source_dir = args.source_dir
    dest_dir    = args.dest_dir


    print("="*50)
    print("Source file: %s"%(source_dir))
    print("Dest. directory: %s"%(dest_dir))
    print("="*50)


    main_set_selection(source_dir,dest_dir)
    