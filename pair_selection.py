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


def find_positive_masks(mask_files):
    
    pos_files= {'root':'','files':[],'file_type':''}

    pos_files['root']=mask_files['root']
    pos_files['file_type']=mask_files['file_type']

    for file in mask_files['files']:
        # Load file
        f = os.path.join(mask_files['root'],file) + '.' + mask_files['file_type']

        mask_array = np.array(Image.open(f)).astype(np.uint8)
        #print(mask_array)

        # verify if there are positive labels
        if (mask_array > 1).any():
            pos_files['files'].append(file)
    
    return(pos_files)
    

def match_file_pair(ref_files,src_files):
    indices,_ = match_file_pair_list(ref_files['files'],src_files['files'])
    ref_files_cp = ref_files.copy()
    src_files_cp = src_files.copy()
    src_files_cp['files'] = np.array(src_files['files'])[indices]
    return(ref_files_cp,src_files_cp)

def match_file_pair_list(ref_files,src_files):
    #  use sub_raster as reference
    matched_files = []
    indices = []
    for i,file in enumerate(src_files):
        if file in ref_files:
            matched_files.append(file)
            indices.append(i)
    
    return(indices,matched_files)


def main_set_selection(src_dir,ref_dir,dst_dir):

    if not os.path.isdir(src_dir):
        return(NameError)
    
    # Get src files
    src_files = utils.get_files(src_dir)
    ref_files = utils.get_files(ref_dir)

    # find positive masks
    ref_files,src_files = match_file_pair(ref_files,src_files)
    
    #Build destination path
    src_dir = os.sep.join(src_dir.split(os.sep)[0:-1])
    src_dir= os.path.join(src_dir,'src_dir')

    if not os.path.isdir(ref_dir):
        os.makedirs(ref_dir)
    
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)

    # Save files to dest dir
    save_files(src_dir,src_files)





if __name__=='__main__':
    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--src_dir',
                        default =  '/home/tiago/research/greenai/split_dataset/esac/x7/dsm_all',
                        help='')
    parser.add_argument('--ref_dir',
                        default =  '/home/tiago/research/greenai/split_dataset/esac/x7/images',
                        help='')
    parser.add_argument('--dest_dir',
                        default = 'changed',
                        help='')
            
    args = parser.parse_args()
    

    src_dir  = args.src_dir
    dest_dir = args.dest_dir
    ref_dir = args.ref_dir


    print("="*50)
    print("src file: %s"%(src_dir))
    print("Dest. directory: %s"%(dest_dir))
    print("ref file: %s"%(ref_dir))

    print("="*50)


    main_set_selection(src_dir,ref_dir,dest_dir)
    