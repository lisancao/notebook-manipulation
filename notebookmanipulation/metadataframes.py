#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:01:50 2020

@author: lisancao
"""


import pandas as pd
import notebookchecks

################################### dataframe stuff
def metadata(formatdf = True, checkdf = True, maintenancedf = True):
    maintenancedf = pd.DataFrame(columns=['cell', 'Javascript', 'Extension Needed', 'Geogebra', 'HTML'], index =["Notebook"])
    checkdf = pd.DataFrame(columns=['NotebookPath', ])
    formatdf = pd.DataFrame(columns=['NotebookPath', ])
    checkdf['NotebookPath'] = 
