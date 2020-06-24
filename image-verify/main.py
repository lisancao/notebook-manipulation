#!/usr/bin/env python3

## Before running the script, you'll have to create an account with Google Cloud and create a project under Vision API
## Then download the credentials file somehwere on your local machine.
## Then set your credentials in your environment by "export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

import re
from web_detection import *
import glob

def get_matching_urls(image_file):
    annotations = annotate(image_file)
    annotations
    best_match = report(annotations)
    return best_match

def get_all_images(notebook_path):
    with open(notebook_path) as f:
        matches = re.findall(r'!\[([^)]+)\]\(([^)]+\.(?:jpg|gif|png))\)',f.read())
    return matches


dir_path = '../notebooks/Social_Sciences/History/'
nb_path = glob.glob(dir_path+'*.ipynb')
for ipynb_file in nb_path:
    print("Working on:  "+ipynb_file)
    image_list = get_all_images(ipynb_file)
    
    for match in image_list:
        print("Finding matching URL link for the image:  "+match[1])
        file_path = dir_path+match[1]
        web_url = get_matching_urls(file_path)
        with open(ipynb_file, 'r') as file:
            content = file.read()
            file.close()

        with open(ipynb_file, 'w') as file:
            content_new = re.sub(match[1], web_url, content)
            file.write(content_new)
            file.close()

    print("\n")

