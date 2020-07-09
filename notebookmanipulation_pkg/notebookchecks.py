#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:02:08 2020

@author: lisancao, misterhay
"""
import os 
import re
import json
import urllib3
import shutil
import requests
import pandas as pd

################################### notebookpaths.py

def notebookpaths(df = False):
    if df == True: 
        fn = pd.DataFrame() #init empty DF
        path = []
        for root, dirs, files in os.walk("."):
            for filename in files:
                if filename.endswith('.ipynb'): # select notebooks
                    file = os.path.join(root, filename)
                    path.append(file) #add to list
        fn['path'] = path #list to col in fn
        e = ["checkpoint", "deprecated", "Untitled"] #keywords to avoid
        fn = fn[~fn.path.str.contains('|'.join(e))] #regex match and exclude
        fn.to_csv("notebookpaths.csv") #write to file
        print("Filewrite complete")
        return fn
    else: 
        path = [] 
        for root, dirs, files in os.walk("."): 
            for filename in files: 
                if filename.endswith('.ipynb'): # select notebooks 
                    file = os.path.join(root, filename) 
                    path.append(file) 
                    e = ["checkpoint", "deprecated", "Untitled"]
                    regex = re.compile('|'.join(e))
                    path = [x for x in path if not regex.search(x)]
        return path

################################### check-website-spreadsheet-links.ipynb

def _spreadsheet_url_check(csv_link):
    df = pd.read_csv(csv_link+'&format=csv')
    link_status_list = []
    for link in df['Link']:
        r = requests.get(link)
        link_status = r.status_code
        link_status_list.append(link_status)
        if link_status == 200:
            pass
        else:
            print('ERROR:', link_status, link)
    df['Status'] = link_status_list
    if df['Status'].mean() == 200:
        print('No link errors')
    else:
        df[df['Status']!=200]
        
#################################### link-checker.ipynb

## function to parse urls (from geeksforgeeks)
def _url_parse(string): 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string) # find all instances      
    return [x[0] for x in url] # append to list

## search through all directories and parse cells
def url_check(spreadsheet = False, csv = ''):
    if spreadsheet == True:
        _spreadsheet_url_check(csv)
    else:
        for root, dirs, files in os.walk("."):
            for filename in files:
                if filename.endswith('.ipynb'): # select notebooks
                    file = os.path.join(root, filename)
                    notebook = json.load(open(file)) # load notebook json
                    cell_number = 0
                    for cell in notebook['cells']:
                        cell_number += 1 # cell counter for output
                        try:
                            cell_contents = cell['source'][0] # parse json
                        except IndexError: # error handling for json index out of range
                            pass
                        cell_urls = _url_parse(cell_contents) # extract urls into list
                        for url in cell_urls: 
                            http = urllib3.PoolManager() # init pool - req' for request sending
                        try:
                            req = http.request('GET', url, timeout = 5.0, retries = False)
                            if req.status < 400 or req.status == 429: # assess http status code, note 429 means too many requests
                                pass
                            else: # for server errors
                                print("BROKEN URL in",file, ": Cell", cell_number, url, "\n    HTTP Status:", req.status, "\n")
                        except Exception as e: # for timeout urllib errors and bad url formats
                            print("BROKEN URL in",file, ": Cell", cell_number, url, "\n    reason:", e, "\n")
        print(".. CHECK COMPLETE")  
    return    

#################################### cell-langtag.ipynb

# use regex to detect language references
def _cell_tagger(contents): 
    java = r"java|javascript|\.js"
    html = r"html|.(\/\>)"
    ggb = r"ggb|geogebra"
    lib = r"ipython|iplot|qgrid" 
    tagsdict = {"Java": java, #dictionary for more readable tags 
                "HTML": html,
                "Geogebra": ggb, 
                "iPython, iPlot, or qgrid": lib}
    printout = []
    for tag, code in tagsdict.items(): # iterate and search 
        regex = re.compile(code)
        if bool(re.search(code, contents)) == True: # find all instances   
            printout.append(tag)
        else: 
            pass
    return printout

# search through all source code in cells and detect if contains language 
def _langtag_():
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'): # select notebooks
                file = os.path.join(root, filename)
                notebook = json.load(open(file)) # load notebook json
                cell_number = 0
                file_contains = []
                with open("celltag_output.txt", "a") as out: 
                    for cell in notebook['cells']:
                        cell_number += 1 # cell counter for output
                        try:
                            cell_contents = cell['source'][0] # parse json
                            cell_tags = _cell_tagger(cell_contents)
                            if cell_tags:
                                file_contains.append([cell_number, cell_tags])
                            else:
                                pass
                        except:
                            pass
                    if file_contains != []:
                        print(filename, "cell flags", file_contains, "\n", file = out)
                out.close()
                
# clean up output
def _clean_langtag(): 
    unique = set() # place for unique lines
    with open("celltag_output.txt", 'r') as file: 
        for line in file: 
            if line not in unique:
                unique.add(line)
        file.close()
    return unique

# as a clean function
def tag_cells():
    _langtag_()
    _clean_langtag()
    print("Complete, see celltag_output.txt")
    
#################################### delete-ds_store-checkpoints.ipynb
def checkpoints():
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename == '.DS_Store':
                print(os.path.join(root, filename))                
            #if '-checkpoint.ipynb' in filename:
            if 'checkpoints' in root:
                print(os.path.join(root, filename))

def checkpoints_delete():
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename == '.DS_Store':
                print(os.path.join(root, filename))                
                os.remove(os.path.join(root, filename))
            if 'checkpoints' in root:
                print(os.path.join(root, filename))
                try:
                      shutil.rmtree(root)
                except:
                      print('Folder already deleted')
                      
#################################### notebooks-clear-outputs.ipynb

def withoutputs_df():
    df = pd.DataFrame(columns=['Notebook', 'Path', 'Outputs'])
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'):
                if not 'checkpoint' in filename:
                    notebook_name = filename[:-6]
                    file = os.path.join(root, filename)
                    notebook = json.load(open(file))
                    cells_with_outputs = 0
                    for cell in notebook['cells']:
                        if cell['cell_type']=='code':
                            outputs = cell['outputs']
                            if len(outputs) > 0:
                                cells_with_outputs += 1
                    #first_cell = notebook['cells'][0]['source']#[0]
                    #last_cell = notebook['cells'][-1]['source']#[0]
                    df = df.append({'Notebook':notebook_name, 'Path':root, 'Outputs':cells_with_outputs}, ignore_index=True)
    # create length of cell columns
    #df['First Cell Length'] = df['First Cell'].str.len()
    #df['Last Cell Length'] = df['Last Cell'].str.len()
    large_output = df[df['Outputs']>0]
    large_output


def clear_outputs(notebook_name_and_path):
    original_file = open(notebook_name_and_path, 'r')
    notebook_contents = json.load(original_file)
    original_file.close()
    for cell in notebook_contents['cells']:
        if cell['cell_type']=='code':
            cell['outputs'] = []
            cell['execution_count'] = None
    with open(notebook_name_and_path, 'w') as notebook_file:
        json.dump(notebook_contents, notebook_file)
        
        
def clear_all_outputs():
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'):
                if not 'checkpoint' in filename:
                    notebook_name = filename[:-6]
                    notebook_name_and_path = os.path.join(root, filename)
                    notebook_file = open(notebook_name_and_path)
                    notebook_contents = json.load(notebook_file)
                    for cell in notebook_contents['cells']:
                        if cell['cell_type']=='code':
                            outputs = cell['outputs']
                            if len(outputs) > 0:
                                notebook_file.close()
                                clear_outputs(notebook_name_and_path)