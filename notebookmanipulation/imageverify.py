#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:56:05 2020

@author: lisacao
"""

## Before running the script, you'll have to create an account with Google Cloud and create a project under Vision API
## Then download the credentials file somehwere on your local machine.
## Then set your credentials in your environment by "export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

import argparse
import io
import re
import glob 
from google.cloud import vision
from google.cloud.vision import types

def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    best_match=""
    """Prints detected features in the provided web annotations."""

    ### Get full matches for the local image

    # print('\n{} Full Matches found: '.format(
    #           len(annotations.full_matching_images)))

    # for image in annotations.full_matching_images:
    #         print('Url  : {}'.format(image.url))

    if annotations.full_matching_images:
        images = annotations.full_matching_images
        for image in images:
            url = image.url
            pattern = re.compile(r'https?:\/\/\S+?\.(?:jpg|jpeg|gif|png)')
            if pattern.match(url):
                print("Matching link to the image:  "+ url)
                best_match = url
                break
            else:
                pass

    ### Get a list of pages that contain matching images.

    # if annotations.pages_with_matching_images:
        
    #     print('\n{} Pages with matching images retrieved'.format(
    #         len(annotations.pages_with_matching_images)))
        
    #     for page in annotations.pages_with_matching_images:
    #         print('Url   : {}'.format(page.url))


    ### Get partial matches for the local image:

    # if annotations.partial_matching_images:
    #     print('\n{} Partial Matches found: '.format(
    #           len(annotations.partial_matching_images)))

    #     for image in annotations.partial_matching_images:
    #         print('Url  : {}'.format(image.url))

    ### Get web entities:
    
    # if annotations.web_entities:
    #     print('\n{} Web entities found: '.format(
    #           len(annotations.web_entities)))

    #     for entity in annotations.web_entities:
    #         print('Score      : {}'.format(entity.score))
    #         print('Description: {}'.format(entity.description))

    return best_match

def get_matching_urls(image_file):
    annotations = annotate(image_file)
    annotations
    best_match = report(annotations)
    return best_match

def get_all_images(notebook_path):
    with open(notebook_path) as f:
        matches = re.findall(r'!\[([^)]+)\]\(([^)]+\.(?:jpg|gif|png))\)',f.read())
    return matches

def verifyimages(): 
    print("Make sure you created an account with Google Cloud and create a project under Vision API\nThen download the credentials file somehwere on your local machine.\nThen set your credentials in your environment by \"export GOOGLE_APPLICATION_CREDENTIALS=\"path/to/your/credentials.json")
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

