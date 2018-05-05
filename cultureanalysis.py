'''
Behavioral analysis to see whether the mouse-tracking (MT) and conceptual DMs for two cultures
were reliably different. Could be adapted to any similar between-groups analysis.
Average conceptual and MT DMs are computed for each culture. Looping through each subject,
the script re-computes the average for that subject's culture, leaving them out. The subject's
DM is then correlated with their culture's average and the other culture's average.
The resulting arrays of Spearman correlation coefficients undergo a paired samples t-test.
'''

import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr,ttest_rel
from scipy.spatial.distance import squareform

#Create a dictionary of Japanese subjects
#Each dictionary entry will have diagonalized versions of their concept and MT DMs
JP_keys = ['sub-JP01','sub-JP02','sub-JP03','sub-JP04','sub-JP05','sub-JP06','sub-JP07','sub-JP08','sub-JP09','sub-JP10','sub-JP11','sub-JP12','sub-JP13','sub-JP14','sub-JP15','sub-JP16','sub-JP17','sub-JP18','sub-JP19','sub-JP20']
JP = {}
for key in JP_keys:
    JP[key] = []
JPfolder = '/Users/jeffreybrooks/Desktop/EmoCulture/DMs/JP/'
JPMT = os.listdir(JPfolder + 'MT_DMs/')
JPconcept = os.listdir(JPfolder + 'concept_DMs/')
for key in JP_keys:
    for MT in JPMT:
        if key in MT:
            mtDM = pd.read_csv(JPfolder + 'MT_DMS/' + MT,delimiter=',',header=None,index_col=False)
            mtDM = mtDM.as_matrix(columns=None)
            JP[key].append(list(squareform(mtDM)))     
        else: pass
    for concept in JPconcept:
        if key in concept:
            cDM = pd.read_csv(JPfolder + 'concept_DMS/' + concept,delimiter=',',header=None,index_col=False)
            cDM = cDM.as_matrix(columns=None)
            JP[key].append(list(squareform(cDM)))     
        else: pass

#Create a dictionary of US subjects
#Each dictionary entry will have diagonalized versions of their concept and MT DMs
US_keys = ['sub-US02','sub-US03','sub-US04','sub-US05','sub-US06','sub-US07','sub-US10','sub-US11','sub-US12','sub-US13','sub-US14','sub-US15','sub-US16','sub-US17','sub-US18','sub-US19','sub-US20','sub-US21','sub-US22','sub-US23']
US = {}
for key in US_keys:
    US[key] = []
USfolder = '/Users/jeffreybrooks/Desktop/EmoCulture/DMs/US/'
USMT = os.listdir(USfolder + 'MT_DMs/')
USconcept = os.listdir(USfolder + 'concept_DMs/')
for key in US_keys:
    for MT in USMT:
        if key in MT:
            mtDM = pd.read_csv(USfolder + 'MT_DMS/' + MT,delimiter=',',header=None,index_col=False)
            mtDM = mtDM.as_matrix(columns=None)
            US[key].append(list(squareform(mtDM)))     
        else: pass
    for concept in USconcept:
        if key in concept:
            cDM = pd.read_csv(USfolder + 'concept_DMS/' + concept,delimiter=',',header=None,index_col=False)
            cDM = cDM.as_matrix(columns=None)
            US[key].append(list(squareform(cDM)))     
        else: pass

#Create average concept and MT DM for both Japan and US
JP_MTDMs = []
JP_cDMs = []
US_MTDMs = []
US_cDMs = []
for key in JP:
    JP_MTDMs.append(JP[key][0])
    JP_cDMs.append(JP[key][1])
for key in US:
    US_MTDMs.append(US[key][0])
    US_cDMs.append(US[key][1])
avgJPMT = np.mean(JP_MTDMs,axis=0)
avgJPconcept = np.mean(JP_cDMs,axis=0)
avgUSMT = np.mean(US_MTDMs,axis=0)
avgUSconcept = np.mean(US_cDMs,axis=0)

JP_MT_spearmans = []
JP_concept_spearmans = []
#Loop through subjects
#On each loop, re-compute the average DM without the current subject in it
for key in JP:
    temp_JPMTDMs = []
    temp_JPcDMs = []
    temp_MT_correlations = []
    temp_concept_correlations = []
    for key2 in JP:
        if key2 != key:
            temp_JPMTDMs.append(JP[key2][0])
            temp_JPcDMs.append(JP[key2][1])
        else: pass
    temp_JPavgMT = np.mean(temp_JPMTDMs,axis=0)
    temp_JPavgconcept = np.mean(temp_JPcDMs,axis=0)
    #Get Spearman r between current subject's DM and leave-them-out average
    temp_MT_correlations.append(spearmanr(JP[key][0],temp_JPavgMT)[0])
    temp_concept_correlations.append(spearmanr(JP[key][1],temp_JPavgconcept)[0])
    #Get Spearman r between current subject's DM and other-country average
    temp_MT_correlations.append(spearmanr(JP[key][0],avgUSMT)[0])
    temp_concept_correlations.append(spearmanr(JP[key][1],avgUSconcept)[0])
    
    JP_MT_spearmans.append(temp_MT_correlations)
    JP_concept_spearmans.append(temp_concept_correlations)
    
US_MT_spearmans = []
US_concept_spearmans = []
#Loop through subjects
#On each loop, re-compute the average DM without the current subject in it
for key in US:
    temp_USMTDMs = []
    temp_UScDMs = []
    temp_MT_correlations = []
    temp_concept_correlations = []
    for key2 in US:
        if key2 != key:
            temp_USMTDMs.append(US[key2][0])
            temp_UScDMs.append(US[key2][1])
        else: pass
    temp_USavgMT = np.mean(temp_USMTDMs,axis=0)
    temp_USavgconcept = np.mean(temp_UScDMs,axis=0)
    #Get Spearman r between current subject's DM and leave-them-out average
    temp_MT_correlations.append(spearmanr(US[key][0],temp_USavgMT)[0])
    temp_concept_correlations.append(spearmanr(US[key][1],temp_USavgconcept)[0])
    #Get Spearman r between current subject's DM and other-country average
    temp_MT_correlations.append(spearmanr(US[key][0],avgJPMT)[0])
    temp_concept_correlations.append(spearmanr(US[key][1],avgJPconcept)[0])
    
    US_MT_spearmans.append(temp_MT_correlations)
    US_concept_spearmans.append(temp_concept_correlations)

#Compute t-tests
JP_concept_tstat = ttest_rel(JP_concept_spearmans[0],JP_concept_spearmans[1])
print(JP_concept_tstat)
US_concept_tstat = ttest_rel(US_concept_spearmans[0],US_concept_spearmans[1])
print(US_concept_tstat)
JP_MT_tstat = ttest_rel(JP_MT_spearmans[0],JP_MT_spearmans[1])
print(JP_MT_tstat)
US_MT_tstat = ttest_rel(US_MT_spearmans[0],US_MT_spearmans[1])
print(US_MT_tstat)