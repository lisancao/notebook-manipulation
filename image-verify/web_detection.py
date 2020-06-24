#!/usr/bin/env python3

import argparse
import io
import re

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
