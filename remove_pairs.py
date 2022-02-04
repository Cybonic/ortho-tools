import argparse
import os
import utils.utils as utils


def remove_files(src_img_files,src_mask_files,files_to_remove):
    
    for file in files_to_remove:
        if file in src_img_files['files']:
            print("file found")
        image_to_remove = os.path.join(src_img_files['root'],file) + '.' + src_img_files['file_type']
        mask_to_remove = os.path.join(src_mask_files['root'],file) + '.' + src_mask_files['file_type']

        if os.path.isfile(image_to_remove):
            os.remove(image_to_remove)
        else:
            print("Image does not exist")
        if os.path.isfile(mask_to_remove):
            os.remove(mask_to_remove)
        else:
            print("MAsk does not exist")


        

def main_remove_pairs(src_dir,file):
    if not os.path.isdir(src_dir):
        return(NameError)
    file_path = os.path.join(src_dir,file)
    if not os.path.isfile(file_path):
        return(NameError)
    # Build path of src files
    src_masks = os.path.join(src_dir,'masks')
    src_imgs = os.path.join(src_dir,'images')

    # Get src files
    src_mask_files = utils.get_files(src_masks)
    src_img_files = utils.get_files(src_imgs)

    with open(file_path,'r') as f:
        cont = f.read()
    file_to_remove = cont.split('\n')
    # find positive masks
    #src_img_files = utils.build_global(src_img_files)
    #src_mask_files = utils.build_global(src_mask_files)

    remove_files(src_img_files,src_mask_files,file_to_remove)

if __name__ == '__main__':
    

    
    # TEST_SAVE_SUB_IM()
    parser = argparse.ArgumentParser(description='Split and save sub tiff images')
    parser.add_argument('--source_dir',
                        default =  '/home/tiago/learning/qtabaixo/x7/',
                        help='')
    parser.add_argument('--file',
                        default = 'to_remove.txt',
                        help='')
            
    args = parser.parse_args()

    source_dir = args.source_dir
    file    = args.file


    print("="*50)
    print("Source file: %s"%(source_dir))
    print("file: %s"%(file))
    print("="*50)

    main_remove_pairs(source_dir,file)