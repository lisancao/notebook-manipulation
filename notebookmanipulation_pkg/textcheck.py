#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:23:52 2020

@author: lisacao
"""
import os
import json
import pandas as pd
import textstat

from markdown import Markdown
from io import StringIO

                      
#################################### notebook-readability-checker.ipynb

def notebookreader():
    def unmark_element(element, stream=None):
        if stream is None:
            stream = StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()
    
    # patching Markdown
    Markdown.output_formats["plain"] = unmark_element
    __md = Markdown(output_format="plain")
    __md.stripTopLevelTags = False
    
    def unmark(text):
        return __md.convert(text)
    
    df = pd.DataFrame(columns=['Notebook', 'Cell Number', 'Readability', 'Text'])
    
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'):
                notebook_name = filename[:-6]
                file = os.path.join(root, filename)
                notebook = json.load(open(file))
                cell_number = 0
                for cell in notebook['cells']:
                    cell_number += 1
                    cell_type = cell['cell_type']
                    if cell_type == 'markdown':
                        #text = cell['source'][0].replace('[', '').replace(']', '').replace('#', '')
                        text = unmark(cell['source'][0])
                        readability = textstat.text_standard(text, float_output=True) # .flesch_kincaid_grade(text)
                        if readability > 0:
                            df = df.append({
                                'Notebook':notebook_name,
                                'Cell Number':cell_number,
                                'Readability':readability,
                                'Text':text},
                                ignore_index=True)
                            
    readability_df = pd.DataFrame()
    for n in df['Notebook'].unique():
        notebook_readabilty = df[df['Notebook']==n]['Readability']
        readability_mean = notebook_readabilty.mean()
        readability_max = notebook_readabilty.max()
        #print(n, readability_mean, readability_max)
        readability_df = readability_df.append({'Notebook':n,'Mean':readability_mean,'Max':readability_max}, ignore_index=True)
    readability_df
    
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.endswith('.ipynb'):
                file = os.path.join(root, filename)
                notebook = json.load(open(file))
                print(file)
                #print(len(notebook['cells']))
                #print(notebook['cells'][0]['source'])
                print(notebook['cells'][-1]['source'])
                print('')