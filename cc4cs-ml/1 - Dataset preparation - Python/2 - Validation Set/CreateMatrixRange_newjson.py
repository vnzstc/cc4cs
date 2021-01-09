#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Declarations
import glob
import json
import os
import numpy as np
import pandas as pd

from os.path import basename


# In[2]:


# DataFrame name json file
nameFile = []
pathFile = []
rootFile = []

path = os.getcwd()
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            nameFile.append(file)
            pathFile.append(os.path.join(root, file))
            rootFile.append(root)
            
nameFileS = pd.Series(nameFile)
pathFileS = pd.Series(pathFile)
rootFileS = pd.Series(rootFile)

dfNF = pd.concat([nameFileS, pathFileS, rootFileS], axis=1)
dfNF.columns = ['FILE_NAME', 'FILE_PATH', 'FILE_ROOT']


# In[11]:


dfNF


# In[5]:


# .json file loop
df = pd.DataFrame(columns=['DEVICE','FUNCTION','DATA_TYPE',
                           'NUM_S','RANGE_S','NUM_SI','RANGE_SI',
                           'NUM_ARR','RANGE_ARR'])

for i in range(0, len(pathFile)):
#i = 0
    pF = pathFile[i]

    with open(pF, 'r') as jf:
        data = jf.read()
    obj = json.loads(data)

    if os.name == 'nt':
        spR = rootFile[i].split('\\')
    else:
        spR = rootFile[i].split('/')
    function = spR[-2]
    device = spR[-1]

    # Data_type loop
    listData = list()
    dtarr = list(obj.keys())
    for j in range(0, len(dtarr)):
        dataype = dtarr[j]
        lsubNP = (list(obj[dataype].keys()))
        lsubVP = (list(obj[dataype].values()))

        # conto la dimensione della sotto-lista
        ltot = len(lsubNP)

        # conto quanti array ci sono
        na = 0
        fl = 0
        ark = 0
        for k in range(0, ltot):
            if "[" in lsubNP[k]:
                na = na + 1
                if fl == 0:
                    ark = k
                    fl = 1

        # conto quanti scalari index ci sono
        nsi = 0
        for k in range(0, ltot):
            flag = 0
            if not "[" in lsubNP[k]:
                for keysl in lsubNP:
                    if (lsubNP[k] in keysl) and (not lsubNP[k] is keysl) and (flag == 0):          
                        flag = 1
                        nsi = nsi + 1           

        # conto quanti scalari ci sono
        ns = ltot - na - nsi

        # vede se è negativo
        
        if ark != 0:
            newstr = lsubVP[ark].replace("[", "")
            newstr = newstr.replace("]", "")
            newstr = newstr.split(",")[0]
            num = float(newstr)
            ranArr = 0
            if num < 0:
                ranArr = 1
            else:
                ranArr = 0
        else:
            ranArr = 0

        df = df.append({'DEVICE': device, 'FUNCTION': function, 'DATA_TYPE': dataype,
                        'NUM_S': ns, 'RANGE_S': 0,'NUM_SI': nsi,'RANGE_SI': 0,
                        'NUM_ARR': na,'RANGE_ARR': ranArr}, 
                        ignore_index=True)


# In[13]:


lsubVP


# In[6]:


dfS = pd.read_csv("dfS.csv", sep=';')
dfSI = pd.read_csv("dfSI.csv", sep=';')
del dfS['Unnamed: 0']
del dfSI['Unnamed: 0']


# In[7]:


columnsS = ['DEVICE','FUNCTION','DATA_TYPE','RANGE_S']
columnsSI = ['DEVICE','FUNCTION','DATA_TYPE','RANGE_SI']
dfS = dfS[columnsS]
dfSI = dfSI[columnsSI]


# In[8]:


lent = len(dfS['RANGE_S'].tolist())
for i in range(0, lent):
    df.loc[(df['DEVICE'] == dfS['DEVICE'][i]) & 
           (df['FUNCTION'] == dfS['FUNCTION'][i]) & 
           (df['DATA_TYPE'] == dfS['DATA_TYPE'][i]), 'RANGE_S'] = dfS['RANGE_S'][i]


# In[9]:


lent = len(dfSI['RANGE_SI'].tolist())
for i in range(0, lent):
    df.loc[(df['DEVICE'] == dfSI['DEVICE'][i]) & 
           (df['FUNCTION'] == dfSI['FUNCTION'][i]) & 
           (df['DATA_TYPE'] == dfSI['DATA_TYPE'][i]), 'RANGE_SI'] = dfSI['RANGE_SI'][i]


# In[10]:


df.to_csv("RangeValueClassification.csv", sep=';')


# In[ ]:




