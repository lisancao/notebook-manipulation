#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:02:08 2020

@author: lisacao
"""


import pandas as pd  
import os 
import re
import json
import urllib3


################################### dataframe stuff


#create datafames
import pandas as pd
maintenancedf = pd.DataFrame(columns=['cell', 'Javascript', 'Extension Needed', 'Geogebra', 'HTML'], index =["Notebook"])



################################### notebookpaths.py

def notebookpaths():
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


#################################### link-checker.ipynb

## function to parse urls (from geeksforgeeks)
def url_parse(string): 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string) # find all instances      
    return [x[0] for x in url] # append to list

## search through all directories and parse cells
def url_check():
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
                    cell_urls = url_parse(cell_contents) # extract urls into list
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
def cell_tagger(contents): 
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
def langtag():
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
                            cell_tags = cell_tagger(cell_contents)
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
def clean_langtag(): 
    unique = set() # place for unique lines
    with open("celltag_output.txt", 'r') as file: 
        for line in file: 
            if line not in unique:
                unique.add(line)
        file.close()
    return unique

# as a clean function
def tag_cells():
    langtag()
    clean_langtag()
    print("Complete, see celltag_output.txt")