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


# In[12]:


# .json file loop
df = pd.DataFrame(columns=['Function','Device','Data_Type',
                           'Num_Sc','Range_Sc','Num_ScI','Range_ScI',
                           'Num_Arr','Range_Arr'])

listrange = [0, 0]
listrangeI = [0, 0]
listdtI = [' ']
listdt = [' ']
listfunI = [' ']
listfun = [' ']
listdevI = [' ']
listdev = [' ']

for i in range(0, len(pathFile)):
    #i = 6
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
        ltot = len(lsubNP)

        kl = []
        for k in range(0, ltot):
            flag = 0
            if not "[" in lsubNP[k]:
                for keysl in lsubNP:
                    if (lsubNP[k] in keysl) and (not lsubNP[k] is keysl) and (flag == 0):          
                        flag = 1
                        kl.append(k) 

        m = 0
        for item in lsubVP:
            if ';' in item:
                newstr = item.split(";")[0]
                newstr = newstr.replace("[", "")
                newstr = newstr.replace("]", "")
                el1 = float(newstr.split(",")[0])
                el2 = float(newstr.split(",")[1])
                strint = el1
                rangeint = el2 - el1
                lr = np.array([strint, rangeint])
                if m in kl:
                    listrangeI = np.vstack([listrangeI, lr])
                    listdtI.append(dataype)
                    listfunI.append(function)
                    listdevI.append(device)
                else:
                    listrange = np.vstack([listrange, lr])
                    listdt.append(dataype)
                    listfun.append(function)
                    listdev.append(device)
            m = m + 1


# In[13]:


listrangeS = pd.DataFrame(listrange)
listdtS = pd.Series(listdt)
listfunS = pd.Series(listfun)
listdevS = pd.Series(listdev)
dfS = pd.concat([listdevS, listfunS, listdtS, listrangeS], axis=1)
dfS.columns = ['DEVICE', 'FUNCTION', 'DATA_TYPE', 'DATA_START', 'DATA_RANGE']
dfS = dfS.iloc[1:]


# In[14]:


listrangeIS = pd.DataFrame(listrangeI)
listdtIS = pd.Series(listdtI)
listfunIS = pd.Series(listfunI)
listdevIS = pd.Series(listdevI)
dfSI = pd.concat([listdevIS, listfunIS, listdtIS, listrangeIS], axis=1)
dfSI.columns = ['DEVICE', 'FUNCTION', 'DATA_TYPE', 'DATA_START', 'DATA_RANGE']
dfSI = dfSI.iloc[1:]


# In[15]:


serS = dfS.groupby(['DATA_TYPE'])['DATA_RANGE'].max()

n = 3
ws = 10
arrlM = []
for d in range(0, len(serS)):
    arrlimt = []
    ml = 0
    w = (serS.iloc[d] - ml) // n
    for h in range(n):
        arrlimt.append(ml + h*w)
    arrlM.append(arrlimt)
    
for index, row in dfS.iterrows():
    clf = 0
    for p in range(0, len(serS)):
        if row['DATA_TYPE'] == serS.index[p]:
            ind = p
            arrl = arrlM[ind]
            for u in range(0, len(arrl)-1):
                if (row['DATA_RANGE'] > arrl[u]) and (row['DATA_RANGE'] <= arrl[u+1]):
                    clf = u + 1
                elif (row['DATA_RANGE'] > arrl[u+1]):
                    clf = len(arrl)            
    dfS['RANGE_S'] = clf      


# In[16]:


serSI = dfSI.groupby(['DATA_TYPE'])['DATA_RANGE'].max()

n = 3
ws = 10
arrlM = []
for d in range(0, len(serSI)):
    arrlimt = []
    ml = 0
    w = (serSI.iloc[d] - ml) // n
    for h in range(n):
        arrlimt.append(ml + h*w)
    arrlM.append(arrlimt)
    
for index, row in dfSI.iterrows():
    clf = 0
    for p in range(0, len(serSI)):
        if row['DATA_TYPE'] == serSI.index[p]:
            ind = p
            arrl = arrlM[ind]
            for u in range(0, len(arrl)-1):
                if (row['DATA_RANGE'] > arrl[u]) and (row['DATA_RANGE'] <= arrl[u+1]):
                    clf = u + 1
                elif (row['DATA_RANGE'] > arrl[u+1]):
                    clf = len(arrl)            
    dfSI['RANGE_SI'] = clf    


# In[17]:


dfS.to_csv("dfS.csv", sep=';')
dfSI.to_csv("dfSI.csv", sep=';')


# In[ ]:




