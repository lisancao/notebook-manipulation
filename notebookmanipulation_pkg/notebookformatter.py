#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:47:44 2020

@author: lisancao, misterhay
"""

import os
import json
import pandas as pd

################################### generate-links-for-youtube-videos.ipynb
def nbgiturl(notebook_name):
    a = 'https://hub.callysto.ca/jupyter/hub/user-redirect/git-pull?repo='
    repo_path = 'https%3A%2F%2Fgithub.com%2Fcallysto%2Finteresting-problems&branch=main'
    nbgitpuller_url = a+repo_path+'&subPath=notebooks/'+notebook_name+'&depth=1'
    return nbgitpuller_url

################################### notebooks-button-creator.ipynb
    
def _button_code_generator(notebook_path, notebook_filename):
    notebook_path = notebook_path.replace('./','',1)
    button_image = 'https://raw.githubusercontent.com/callysto/curriculum-notebooks/master/open-in-callysto-button.svg?sanitize=true'
    repo_path = 'https%3A%2F%2Fgithub.com%2Fcallysto%2Fcurriculum-notebooks&branch=master'
    a = '<a href="https://hub.callysto.ca/jupyter/hub/user-redirect/git-pull?repo='
    size_etc = '" width="123" height="24" alt="Open in Callysto"/></a>'
    button_code = a+repo_path+'&subPath='+notebook_path+'/'+notebook_filename+'&depth=1" target="_parent"><img src="'+button_image+size_etc
    return button_code

def _replace_first_cell(notebook_name_and_path, first_cell_code):
    original_file = open(notebook_name_and_path, 'r')
    notebook_contents = json.load(original_file)
    original_file.close()
    del notebook_contents['cells'][0]
    notebook_contents['cells'].insert(0, first_cell_code)
    with open(notebook_name_and_path, 'w') as notebook_file:
        json.dump(notebook_contents, notebook_file)
        
def _button_df():
    df = pd.DataFrame(columns=['Notebook', 'Button Code'])
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'):
                if not 'checkpoint' in filename:
                    notebook_name_and_path = os.path.join(root, filename).strip('./')
                    button_code = _button_code_generator(root, filename)
                    df = df.append({'Notebook':notebook_name_and_path, 'Button Code':button_code}, ignore_index=True)
                    for i, row in df.iterrows():
                        notebook_name_and_path = row['Notebook']
                        banner_code = '![Callysto.ca Banner](https://github.com/callysto/curriculum-notebooks/blob/master/callysto-notebook-banner-top.jpg?raw=true)'
                        first_cell_code = {'cell_type': 'markdown', 'metadata': {}, 'source': [banner_code, '\n', '\n', row['Button Code']]}
                        if notebook_name_and_path != './notebooks-button-creator.ipynb':
                            _replace_first_cell(notebook_name_and_path, first_cell_code)
    return df


def openincallysto(show_df = True, checkwork = True): 
    if show_df == True:
        button_df = _button_df()
        button_df
    else: 
        button_df()
        
    if checkwork == True: 
        #checkwork
        df2 = pd.DataFrame(columns=['Name','First Cell'])
        for root, dirs, files in os.walk("."):
            for filename in files:
                if filename.endswith('.ipynb'):
                    if not 'checkpoint' in filename:
                        notebook_name = filename[:-6]
                        notebook_name_and_path = os.path.join(root, filename)
                        notebook = json.load(open(notebook_name_and_path))
                        first_cell = notebook['cells'][0]['source']#[0]
                        df2 = df2.append({'Name':notebook_name,'First Cell':first_cell}, ignore_index=True)
        for i, row in df2.iterrows():
            print(i, row['Name'])
            print(row['First Cell'])
            print('')        

        