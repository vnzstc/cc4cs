#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import sys
import ntpath

from os.path import basename


# In[2]:


dfRDC = pd.read_csv("RangeValueClassification.csv", sep=';')
del dfRDC['Unnamed: 0']


# In[3]:


nameFileH = []
pathFileH = []
rootFileH = []
nameFileM = []
pathFileM = []
rootFileM = []
nameFileC = []
pathFileC = []
rootFileC = []

path = os.getcwd()
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith("Halsted.csv"):
            nameFileH.append(file)
            pathFileH.append(os.path.join(root, file))
            rootFileH.append(root)
        elif file.endswith("McCabe.csv"):
            nameFileM.append(file)
            pathFileM.append(os.path.join(root, file))
            rootFileM.append(root)
        elif file.endswith("Values.csv"):
            nameFileC.append(file)
            pathFileC.append(os.path.join(root, file))
            rootFileC.append(root)


# In[4]:


for i in range(0, len(pathFileH)):
    path = pathFileH[i]
    try:
        dfHTemp = pd.read_csv(path, sep=',',engine='python')
    except:
        print(path)
        
    if os.name == 'nt':
        spR = rootFileH[i].split('\\')
    else:
        spR = rootFileH[i].split('/')
    datatype = spR[-1]
    device = spR[-3]
    function = spR[-4]
    dfHTemp['DEVICE'] = device
    dfHTemp['FUNCTION'] = function
    dfHTemp['DATA_TYPE'] = datatype
    dfHTemp['inputNumber'] = dfHTemp['inputNumber'].map(lambda x: x.lstrip('values_'))
    dfHTemp['inputNumber'] = dfHTemp['inputNumber'].astype(int)
    dfHTemp.sort_values('inputNumber')
    
    if i == 0:
        dfHTot = dfHTemp
    else:
        frames = [dfHTot, dfHTemp]
        dfHTot = pd.concat(frames)


# In[5]:


for i in range(0, len(pathFileM)):
    path = pathFileM[i]
    dfMTemp = pd.read_csv(path, sep=',',engine='python')

    if os.name == 'nt':
        spR = rootFileM[i].split('\\')
    else:
        spR = rootFileM[i].split('/')
    datatype = spR[-1]
    device = spR[-3]
    function = spR[-4]
    dfMTemp['DEVICE'] = device
    dfMTemp['FUNCTION'] = function
    dfMTemp['DATA_TYPE'] = datatype
    dfMTemp['inputNumber'] = dfMTemp['inputNumber'].map(lambda x: x.lstrip('values_'))
    dfMTemp['inputNumber'] = dfMTemp['inputNumber'].astype(int)
    dfMTemp.sort_values('inputNumber')
    
    if i == 0:
        dfMTot = dfMTemp
    else:
        frames = [dfMTot, dfMTemp]
        dfMTot = pd.concat(frames)


# In[6]:


for i in range(0, len(pathFileC)):
    path = pathFileC[i]
    dfCTemp = pd.read_csv(path, sep=',',engine='python')
    
    if os.name == 'nt':
        spR = rootFileC[i].split('\\')
    else:
        spR = rootFileC[i].split('/')
    datatype = spR[-1]
    device = spR[-3]
    function = spR[-4]
    dfCTemp['DEVICE'] = device
    dfCTemp['FUNCTION'] = function
    dfCTemp['DATA_TYPE'] = datatype
    dfCTemp['id'] = dfCTemp['id'].map(lambda x: x.lstrip('values_'))
    dfCTemp['id'] = dfCTemp['id'].astype(int)
    dfCTemp.sort_values('id')
    
    if i == 0:
        dfCTot = dfCTemp
    else:
        frames = [dfCTot, dfCTemp]
        dfCTot = pd.concat(frames)


# In[7]:


dfHTot = dfHTot.reset_index(drop=True)
dfMTot = dfMTot.reset_index(drop=True)
dfCTot = dfCTot.reset_index(drop=True)


# In[8]:


columnsH = ['DEVICE', 'FUNCTION', 'DATA_TYPE',# 'BugsDelivered', 
            'DifficultyLevel', 'DistinctOperands', 
            'DistinctOperators', 'Effort', 'ProgramLength', 'ProgramLevel', 'ProgramVolume', 
            #'TimeToImplement', 
            'TotalOperators', 'Total_Operands', 'VocabularySize']
columnsM = ['DEVICE', 'FUNCTION', 'DATA_TYPE', 'Sloc', 'DecisionPoint', 'GlobalVariables', 
            'If', 'Loop', 'Goto', 'Assignment', 'ExitPoint', 'Function', 'FunctionCall', 
            'PointerDereferencing', 'CyclomaticComplexity', 'SyntacticallyReachableFunctions', 
            'SemanticallyReachedFunctions', 'CoverageEstimation']
columnsC = ['DEVICE', 'FUNCTION', 'DATA_TYPE','cInstr', 'clockCycles', 'assemblyInstr', 'cc4cs']


# In[9]:


dfHTot = dfHTot[columnsH]
dfMTot = dfMTot[columnsM]
dfCTot = dfCTot[columnsC]


# In[10]:


dfPar1 = dfHTot.assign(**dfMTot)
dfPar2 = dfPar1.assign(**dfCTot)


# In[11]:


dfTot = pd.merge(dfPar2,dfRDC,how='left',on=['DEVICE','FUNCTION','DATA_TYPE'])
columnsTot = ['DEVICE', 'FUNCTION', 'DATA_TYPE',# 'BugsDelivered', 
              'DifficultyLevel',
       'DistinctOperands', 'DistinctOperators', 'Effort', 'ProgramLength',
       'ProgramLevel', 'ProgramVolume', #'TimeToImplement', 
       'TotalOperators',
       'Total_Operands', 'VocabularySize', 'Sloc', 'DecisionPoint',
       'GlobalVariables', 'If', 'Loop', 'Goto', 'Assignment', 'ExitPoint',
       'Function', 'FunctionCall', 'PointerDereferencing',
       'CyclomaticComplexity', 'SyntacticallyReachableFunctions',
       'SemanticallyReachedFunctions', 'CoverageEstimation', 'NUM_S', 'RANGE_S', 'NUM_SI',
       'RANGE_SI', 'NUM_ARR', 'RANGE_ARR', 'cInstr', 'assemblyInstr',
       'clockCycles', 'cc4cs']
dfTot = dfTot[columnsTot]


# In[12]:


dfTot.to_csv("TotalParameterMatrix.csv", sep=';')


# In[14]:


if os.name == 'nt':
    dfTot.to_csv("C:\\Users\\User\\Desktop\\Dataset Lavoro\\CC4CS\\CC4CS_Analysis\\Matlab\\Workspaces\\Dataset\\TotalParameterMatrix.csv", sep=';')
else:
    dfTot.to_csv("/home/dews/Dataset Ricerca/CC4CS/CC4CS_Analysis/Matlab/Workspaces/Dataset/TotalParameterMatrix.csv", sep=';')


# In[ ]:




