#!/usr/bin/env python
# coding: utf-8

# In[206]:


# Declarations
import glob
import json
import os
import numpy as np
import pandas as pd

from os.path import basename


# In[207]:


dfRVC = pd.read_csv("RangeValueClassification.csv", sep=';')
dfNB = pd.read_csv("newBench.csv", sep=',')


# In[208]:


del dfRVC['Unnamed: 0']
del dfNB['Var1']


# In[209]:


dfRVC['DEVICE'] = dfRVC['DEVICE'].str.strip()
dfNB['DEVICE'] = dfNB['DEVICE'].str.strip()

dfRVC['DATA_TYPE'] = dfRVC['DATA_TYPE'].str.strip()
dfNB['DATA_TYPE'] = dfNB['DATA_TYPE'].str.strip()

dfRVC['FUNCTION'] = dfRVC['FUNCTION'].str.strip()
dfNB['FUNCTION'] = dfNB['FUNCTION'].str.strip()

dfRVC['DEVICE'] = dfRVC['DEVICE'].str.replace('Atmega328p', 'atmega328')
dfRVC['DEVICE'] = dfRVC['DEVICE'].str.replace('Leon3', 'sparc_leon3')
dfRVC['FUNCTION'] = dfRVC['FUNCTION'].str.replace('viterbi_register_lenght', 'viterbi_reg')
dfRVC['FUNCTION'] = dfRVC['FUNCTION'].str.replace('viterbi_getn', 'viterbi_getN')


# In[210]:


del dfNB['NUM_S']
del dfNB['RANGE_S']
del dfNB['NUM_SI']
del dfNB['RANGE_SI']
del dfNB['NUM_ARR']
del dfNB['RANGE_ARR']


# In[211]:


dfNB.head()


# In[212]:


dfRVC.head()


# In[213]:


dfTot = pd.merge(dfNB,dfRVC,how='left',on=['DEVICE','FUNCTION','DATA_TYPE'])


# In[214]:


dfTot.head()


# In[215]:


dfNB.shape


# In[216]:


dfTot.shape


# In[217]:


columnsTot = ['DEVICE', 'FUNCTION', 'DATA_TYPE', 
              'DifficultyLevel',
              'DistinctOperands', 'DistinctOperators', 'Effort', 'ProgramLength',
              'ProgramLevel', 'ProgramVolume', 
              'TotalOperators',
              'Total_Operands', 'VocabularySize', 'Sloc', 'DecisionPoint',
              'GlobalVariables', 'If', 'Loop', 'Goto', 'Assignment', 'ExitPoint',
              'Function', 'FunctionCall', 'PointerDereferencing',
              'CyclomaticComplexity', 'SyntacticallyReachableFunctions',
              'SemanticallyReachedFunctions', 'CoverageEstimation', 
              'NUM_S', 'RANGE_S', 'NUM_SI',
              'RANGE_SI', 'NUM_ARR', 'RANGE_ARR', 'cInstr', 'assemblyInstr',
              'clockCycles', 'CC4CS']
dfTot = dfTot[columnsTot]


# In[218]:


dfTot


# In[221]:


dfTot.to_csv("newBenchMerge.csv", sep=';')


# In[222]:


df8051 = dfTot[dfTot['DEVICE'] == '8051']
dfatmega = dfTot[dfTot['DEVICE'] == 'atmega328']
dfleon3 = dfTot[dfTot['DEVICE'] == 'sparc_leon3']


# In[223]:


df8051.to_csv("nB8051.csv", sep=';',index=False)
dfatmega.to_csv("nBatmega328p.csv", sep=';',index=False)
dfleon3.to_csv("nBleon3.csv", sep=';',index=False)


# In[235]:


columnsTot2 = ['DEVICE', 'FUNCTION', 'DATA_TYPE', 
              'DifficultyLevel',
              'DistinctOperands', 'DistinctOperators', 'Effort', 'ProgramLength',
              'ProgramLevel', 'ProgramVolume', 
              'TotalOperators',
              'Total_Operands', 'VocabularySize', 'Sloc', 'DecisionPoint',
              'GlobalVariables', 'If', 'Loop', 'Goto', 'Assignment', 
              #'ExitPoint',
              #'Function', 'FunctionCall', 'PointerDereferencing',
              #'CyclomaticComplexity', 'SyntacticallyReachableFunctions',
              #'SemanticallyReachedFunctions', 'CoverageEstimation', 
              'NUM_S', 'RANGE_S', 'NUM_SI',
              'RANGE_SI', 'NUM_ARR', 'RANGE_ARR', 
              'cInstr', 'clockCycles', 'CC4CS']
dfTot2 = dfTot[columnsTot2]


# In[236]:


dfTot2[dfTot2.isnull().any(axis=1)]


# In[ ]:




