####################################################

#FILE         : notebookpaths.py
#DESCRIPTION  : Generates list of all notebook paths in directory 

#OPTIONS      : ---
#REQUIREMENTS : ---
#BUGS         : ---
#NOTES        : for .csv output see the .ipynb

#AUTHOR       : LNC
#CONTACT      : lisa.cao@cybera.ca
#DATE CREATED : 06/24/2020
#LAST REVISION: --- 

####################################################

import pandas as pd  
import os 
import re

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
