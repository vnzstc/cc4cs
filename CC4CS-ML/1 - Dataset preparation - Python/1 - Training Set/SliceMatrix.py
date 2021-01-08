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


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


# In[3]:


listfun = ['astar','bankeralgorithm','bellmanford','bfsdfs','binarysearch',
           'bubblesort','dijkstra','floydwarshall','gcd','insertionsort','kruskal','matrixmul',
           'mergesort','quicksort','selectionsort']


# In[4]:


listdt = ['float', 'int8', 'int', 'long']
dicDT = {'DATA_TYPE': listdt}
dfDT = pd.DataFrame(dicDT, columns = ['DATA_TYPE'])
dfDT.to_csv("DataTypeList.csv", sep=';',index=False)


# In[5]:


df = pd.read_csv("TotalParameterMatrix.csv", sep=';')
del df['Unnamed: 0']


# In[6]:


listdev = ['8051', 'atmega328p', 'leon3']
dicDEV = {'DATA_TYPE': listdev}
dfDEV = pd.DataFrame(dicDEV, columns = ['DATA_TYPE'])
dfDEV.to_csv("DeviceList.csv", sep=';',index=False)


# In[7]:


listHeader = list(df.columns.values)


# In[8]:


listHeader = ['DEVICE',
 'FUNCTION',
 'DATA_TYPE',
 'FILE_CSV',
 'PATH',
 'SLOC',
 'SCALAR_INPUT',
 'RANGE_SCALAR_VALUES',
 'SCALAR_INDEX_INPUT',
 'RANGE_SCALAR_INDEX_VALUES',
 'ARRAY_INPUT',
 'RANGE_ARRAY_INPUT',
 'DSTINCT_OPERATORS',
 'TOTAL_OPERANDS',
 'DISTINCT_OPERANDS',
 'VOCABULARY_SIZE',
 'EFFORT',
 'BUGS_DELIVERED',
 'TIME_TO_IMPLEMENT',
 'DIFFICULTY_LEVEL',
 'PROGRAM_LEVEL',
 'GLOBAL VARIABLES',
 'GOTO',
 'ASSIGNMENT',
 'Executed C Instr',
 'Executed Ass Instr',
 'Clock Cycle Effective']


# In[9]:


df = df[listHeader]


# In[10]:


# DEVICE
df.loc[df.DEVICE == 8051, 'DEVICE'] = '8051'
df.loc[df.DEVICE == '8051', 'DEVICE'] = '8051'
df.loc[df.DEVICE == 'atmega328', 'DEVICE'] = 'atmega328p'
df.loc[df.DEVICE == 'sparc_leon3', 'DEVICE'] = 'leon3'


# In[11]:


# FUNCTION
df.loc[df.FUNCTION == 'a_star', 'FUNCTION'] = 'astar'
df.loc[df.FUNCTION == 'banker_algorithm', 'FUNCTION'] = 'bankeralgorithm'
df.loc[df.FUNCTION == 'bellman_ford', 'FUNCTION'] = 'bellmanford'
df.loc[df.FUNCTION == 'bfs_dfs', 'FUNCTION'] = 'bfsdfs'
df.loc[df.FUNCTION == 'floyd_warshall', 'FUNCTION'] = 'floydwarshall'
df.loc[df.FUNCTION == 'matrix_mul', 'FUNCTION'] = 'matrixmul'


# In[13]:


df = df.rename(columns = {'Executed Ass Instr':'assemblyInstr'})
df = df.rename(columns = {'Clock Cycle Effective':'clockCycles'})


# In[17]:


df8051 = df[df['DEVICE'] == '8051']
dfatmega = df[df['DEVICE'] == 'atmega328p']
dfleon3 = df[df['DEVICE'] == 'leon3']

p808051 = int(np.floor(df8051.shape[0]*perc))
p80atmega = int(np.floor(dfatmega.shape[0]*perc))
p80leon3 = int(np.floor(dfleon3.shape[0]*perc))

df8051.iloc[:p808051,:].to_csv("8051.csv", sep=';',index=False)
dfatmega.iloc[:p80atmega,:].to_csv("atmega328p.csv", sep=';',index=False)
dfleon3.iloc[:p80leon3,:].to_csv("leon3.csv", sep=';',index=False)

df8051.iloc[p808051:,:].to_csv("8051Val.csv", sep=';',index=False)
dfatmega.iloc[p80atmega:,:].to_csv("atmega328pVal.csv", sep=';',index=False)
dfleon3.iloc[p80leon3:,:].to_csv("leon3Val.csv", sep=';',index=False)


# In[28]:


for i in range(0, len(listfun)):
    dfPar = df[(df['DEVICE'] == '8051') & (df['FUNCTION'] == listfun[i])]
    p80Par = int(np.floor(dfPar.shape[0]*perc))
    if (dfPar.shape[0] != 0):
        dfPar.iloc[:p80Par,:].to_csv("8051_"+listfun[i]+".csv", sep=';',index=False)
        dfPar.iloc[p80Par:,:].to_csv("8051_"+listfun[i]+"Val.csv", sep=';',index=False)


# In[29]:


for i in range(0, len(listfun)):
    dfPar = df[(df['DEVICE'] == 'atmega328p') & (df['FUNCTION'] == listfun[i])]
    p80Par = int(np.floor(dfPar.shape[0]*perc))
    if (dfPar.shape[0] != 0):
        dfPar.iloc[:p80Par,:].to_csv("atmega328p_"+listfun[i]+".csv", sep=';',index=False)
        dfPar.iloc[p80Par:,:].to_csv("atmega328p_"+listfun[i]+"Val.csv", sep=';',index=False)


# In[30]:


for i in range(0, len(listfun)):
    dfPar = df[(df['DEVICE'] == 'leon3') & (df['FUNCTION'] == listfun[i])]
    p80Par = int(np.floor(dfPar.shape[0]*perc))
    if (dfPar.shape[0] != 0):
        dfPar.iloc[:p80Par,:].to_csv("leon3_"+listfun[i]+".csv", sep=';',index=False)
        dfPar.iloc[p80Par:,:].to_csv("leon3_"+listfun[i]+"Val.csv", sep=';',index=False)


# In[31]:


for i in range(0, len(listfun)):
    for j in range(0, len(listdt)):
        dfPar = df[(df['DEVICE'] == '8051') & (df['FUNCTION'] == listfun[i]) & (df['DATA_TYPE'] == listdt[j])]
        p80Par = int(np.floor(dfPar.shape[0]*perc))
        if (dfPar.shape[0] != 0):
            dfPar.iloc[:p80Par,:].to_csv("8051_"+listfun[i]+"_"+listdt[j]+".csv", sep=';',index=False)
            dfPar.iloc[p80Par:,:].to_csv("8051_"+listfun[i]+"_"+listdt[j]+"Val.csv", sep=';',index=False)


# In[32]:


for i in range(0, len(listfun)):
    for j in range(0, len(listdt)):
        dfPar = df[(df['DEVICE'] == 'atmega328p') & (df['FUNCTION'] == listfun[i]) & (df['DATA_TYPE'] == listdt[j])]
        p80Par = int(np.floor(dfPar.shape[0]*perc))
        if (dfPar.shape[0] != 0):
            dfPar.iloc[:p80Par,:].to_csv("atmega328p_"+listfun[i]+"_"+listdt[j]+".csv", sep=';',index=False)
            dfPar.iloc[p80Par:,:].to_csv("atmega328p_"+listfun[i]+"_"+listdt[j]+"Val.csv", sep=';',index=False)


# In[33]:


for i in range(0, len(listfun)):
    for j in range(0, len(listdt)):
        dfPar = df[(df['DEVICE'] == 'leon3') & (df['FUNCTION'] == listfun[i]) & (df['DATA_TYPE'] == listdt[j])]
        p80Par = int(np.floor(dfPar.shape[0]*perc))
        if (dfPar.shape[0] != 0):
            dfPar.iloc[:p80Par,:].to_csv("leon3_"+listfun[i]+"_"+listdt[j]+".csv", sep=';',index=False)
            dfPar.iloc[p80Par:,:].to_csv("leon3_"+listfun[i]+"_"+listdt[j]+"Val.csv", sep=';',index=False)

