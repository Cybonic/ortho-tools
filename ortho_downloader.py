import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import numpy as np
import os

URL = "http://www.mat.uc.pt/~gil/AIGreen/Geospatial/QtaBaixo27Jul/"
DIRECTORY = 'QtaBaixo27Jul'

MAIN_ROOT = 'Downloads'

EXCLUDE_ELEMENTS = ['~','?']


def download_files_html(url,local_file_name):
    '''
    Dowloads a remote file <url> and saves it locally under
    the name <local_file_name>.

    INPUTS:
    @parm url: pointer to remote file
    @parm local_file_name: 

    OUTPUT: None
    
    '''
    #print("=="*40)
    #print("[%s] Link: %s"%(__func_name__,url))
    #print("[%s] Destination directory: %s"%(__func_name__,file))
    print("File: " + local_file_name)
    r = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(r.headers.get('content-length'))
    initial_pos = 0
    with open(local_file_name,'wb') as f: 
        with tqdm(total=total_size, 
            unit_scale=True,                      
            #desc=file,
            initial=initial_pos, 
            ascii=True) as pbar:
                for ch in r.iter_content(chunk_size=1024):
                    if ch:
                        f.write(ch) 
                        pbar.update(len(ch))



def list_FD_html(url, ext=''):
    # https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/
    '''
    Returns a list of files and their respective pointers
    available on a html page <url>


    @parm url: [str] pointer to html page
    @param ext: extention
    
    @return numpy array [n x 2]
        [pointer 0, file 0]
        [pointer 1, file 1]
        [pointer 2, file 2]
        ...
        [pointer n, file n]
    
    '''
    list_of_files = np.array([])
    
    list_of_elements = _listFDhtml(url)
    
    if isinstance(list_of_elements,list):
        for sub_url in list_of_elements:
            if'.' in sub_url: # file
                if list_of_files.size==0:
                    list_of_files = np.array([url,sub_url])
                else:
                    list_of_files = np.vstack((list_of_files,[url,sub_url]))
            else: # Directory
                sub_url = url + '/' + sub_url
                new_array = np.array(list_FD_html(sub_url))
                if new_array.size==0: continue # empty array
                if list_of_files.size==0:
                    list_of_files = new_array
                else:
                    list_of_files = np.vstack((list_of_files,new_array))
                
        return(list_of_files)
    
def _listFDhtml(url):

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    list_of_content = []
    for node in soup.find_all('a'):
        href = node.get('href')
        check = [True for elm in EXCLUDE_ELEMENTS if elm in href]
        if not True in check:
            list_of_content.append(href)
    
    return(list_of_content)

def main_ortho_downloader(list_of_files):

    for root,file in  list_of_files:
        link = root+file 
        root_list = root.split('/')
        # Find root folder in remote path
        indix = [i for i,dir in enumerate(root_list) if dir == DIRECTORY][0] 
        # Build local path based on the remote path
        local_path = os.path.sep.join(root_list[indix:-1])
        
        # Build path to destination directory
        abs_local_path = os.path.join(MAIN_ROOT,local_path)
        if not os.path.isdir(abs_local_path):
            os.makedirs(abs_local_path)
        # Build absolute local file path
        file_path = os.path.join(abs_local_path,file)
        # Download file and save to destination path
        download_files_html(link,file_path)

if __name__=='__main__':

    # TO-DO: 
    # 1. Input arguments
    # 2. input argument that specifies wether to downloaded a specific file or all  

    list_of_files = list_FD_html(URL, ext='')
    main_ortho_downloader(list_of_files)

    print("[INF] FILES TO DOWNLOAD: %s"%(len(list_of_files)))
   
    



    