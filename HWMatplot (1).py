#!/usr/bin/env python
# coding: utf-8

# # Importing Dependencies and reading .csv file

# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ipywidgets import *

import warnings
warnings.filterwarnings('ignore')


mouse_data = "/Users/cla/Desktop/UM Data Science/Homework/05-Matplot/matplotlib-challenge/mouse_drug_data.csv"
clinical_data = "/Users/cla/Desktop/UM Data Science/Homework/05-Matplot/matplotlib-challenge/clinicaltrial_data.csv"

md = pd.read_csv(mouse_data)
cd = pd.read_csv(clinical_data)


# In[3]:


md.head()


# In[4]:


cd.head()


# # Merging the two df

# In[5]:


cd_md = pd.merge(cd, md)


# In[6]:


cd_md.head(5)


# In[7]:


cdmd_df = cd_md.rename(columns={'Mouse ID':'Mouse_ID','Tumor Volume (mm3)':'Tumor_Volume_mm3',
                                   'Metastatic Sites':'Metastatic_Sites'})
cdmd_df.head(5)


# # Mean of the data

# In[8]:


mean_tumorvol = cdmd_df.groupby(['Drug', 'Timepoint']).mean()
del mean_tumorvol['Metastatic_Sites']


# In[9]:


mean_tumorvol.head(10)


# # Sem of the data

# In[10]:


stderr_tumorvol = cdmd_df.groupby(['Drug', 'Timepoint']).sem()
del stderr_tumorvol['Metastatic_Sites']
del stderr_tumorvol['Mouse_ID']


# In[11]:


stderr_tumorvol.head(10)


# # Pivot tables and filtering treatments

# In[12]:


table = pd.pivot_table(mean_tumorvol, values='Tumor_Volume_mm3', index=['Timepoint'],columns=['Drug'])


# In[13]:


table_mean = table[['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']]
table_mean


# In[14]:


table2 = pd.pivot_table(stderr_tumorvol, values='Tumor_Volume_mm3', index=['Timepoint'],columns=['Drug'])


# In[15]:


table_sem = table2[['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']]
table_sem


# # 1 - Error bar: Tumor volume changes over time for each treatment

# In[16]:


capomulin_sem = table_mean['Capomulin'].sem()
infubinol_sem = table_mean['Infubinol'].sem()
ketapril_sem = table_mean['Ketapril'].sem()
placebo_sem = table_mean['Placebo'].sem()

fig,ax = plt.subplots()
ax.errorbar(table_mean.index,table_mean['Capomulin'],yerr=capomulin_sem,label='Capomulin',marker='d',linestyle='-.',markersize=5,capsize=5)
ax.errorbar(table_mean.index,table_mean['Infubinol'],yerr=infubinol_sem,label='Infubinol',marker='.',linestyle=':',markersize=8,capsize=5)
ax.errorbar(table_mean.index,table_mean['Ketapril'],yerr=ketapril_sem,label='Ketapril',marker='.',linestyle='-.',markersize=8,capsize=5)
ax.errorbar(table_mean.index,table_mean['Placebo'],yerr=placebo_sem,label='Placebo',marker='d',linestyle=':',markersize=5,capsize=5)
ax.legend(loc='best')
ax.set_xlim(-0.5, 50)
ax.set_ylim(30, 75)
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Tumor Volume (mm3)')
ax.grid(alpha=0.25)
plt.title('Tumor Volume Response to Treatment')
plt.show()
fig.savefig("Figure1.png")


# # 

# # 2 - Error bar: Metastatic sites changes over time for each treatment.

# In[17]:


mean_metastatic = cdmd_df.groupby(['Drug', 'Timepoint']).mean()
del mean_metastatic['Tumor_Volume_mm3']
mean_metastatic.head(10)


# In[18]:


sem_metastatic = cdmd_df.groupby(['Drug', 'Timepoint']).sem()
del sem_metastatic['Tumor_Volume_mm3']
del sem_metastatic['Mouse_ID']
sem_metastatic.head(10)


# In[19]:


table3 = pd.pivot_table(mean_metastatic, values='Metastatic_Sites', index=['Timepoint'],columns=['Drug'])
table_metastatic_mean = table3[['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']]
table_metastatic_mean


# In[20]:


met_capomulin_sem = table_metastatic_mean['Capomulin'].sem()
met_infubinol_sem = table_metastatic_mean['Infubinol'].sem()
met_ketapril_sem = table_metastatic_mean['Ketapril'].sem()
met_placebo_sem = table_metastatic_mean['Placebo'].sem()

fig,ax = plt.subplots()
ax.errorbar(table_metastatic_mean.index,table_metastatic_mean['Capomulin'],yerr=met_capomulin_sem,label='Capomulin',marker='d',linestyle='-.',markersize=5,capsize=5)
ax.errorbar(table_metastatic_mean.index,table_metastatic_mean['Infubinol'],yerr=met_infubinol_sem,label='Infubinol',marker='.',linestyle=':',markersize=8,capsize=5)
ax.errorbar(table_metastatic_mean.index,table_metastatic_mean['Ketapril'],yerr=met_ketapril_sem,label='Ketapril',marker='.',linestyle='-.',markersize=8,capsize=5)
ax.errorbar(table_metastatic_mean.index,table_metastatic_mean['Placebo'],yerr=met_placebo_sem,label='Placebo',marker='d',linestyle=':',markersize=5,capsize=5)
ax.legend(loc='best')
ax.set_xlim(-0.5, 50)
ax.set_ylim(0, 4)
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Metastatic Sites')
ax.grid(alpha=0.25)
plt.title('Metastatic Response to Treatments')
plt.show()
fig.savefig("Figure2.png")


# # 3 -Error bar: Number of mice still alive through the course of treatment (Survival Rate)

# In[21]:


survival_rate = cdmd_df.groupby(['Drug', 'Timepoint']).Mouse_ID.count()
survival_rate_df = survival_rate.to_frame()
survival_rate_df.head(5)


# In[22]:


table4 = pd.pivot_table(survival_rate_df, values='Mouse_ID', index=['Timepoint'],columns=['Drug'])
table_survival_mean = table4[['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']]
table_survival_mean


# In[23]:


surv_capomulin_sem = table_survival_mean['Capomulin'].sem()
surv_infubinol_sem = table_survival_mean['Infubinol'].sem()
surv_ketapril_sem = table_survival_mean['Ketapril'].sem()
surv_placebo_sem = table_survival_mean['Placebo'].sem()

fig,ax = plt.subplots()
ax.errorbar(table_survival_mean.index,table_survival_mean['Capomulin'],yerr=surv_capomulin_sem,label='Capomulin',marker='d',linestyle='-.',markersize=5,capsize=5)
ax.errorbar(table_survival_mean.index,table_survival_mean['Infubinol'],yerr=surv_infubinol_sem,label='Infubinol',marker='.',linestyle=':',markersize=8,capsize=5)
ax.errorbar(table_survival_mean.index,table_survival_mean['Ketapril'],yerr=surv_ketapril_sem,label='Ketapril',marker='.',linestyle='-.',markersize=8,capsize=5)
ax.errorbar(table_survival_mean.index,table_survival_mean['Placebo'],yerr=surv_placebo_sem,label='Placebo',marker='d',linestyle=':',markersize=5,capsize=5)
ax.legend(loc='best')
ax.set_xlim(-0.5, 50)
ax.set_ylim(0, 30)
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Mouse Count')
ax.grid(alpha=0.25)
plt.title('Survival Rate of Mouse through the course of treatment')
plt.show()
fig.savefig("Figure3.png")


# # 4

# In[24]:


table_mean


# In[25]:


difference = (table.iloc[[0, 9]].diff()/ 45*100).round(6)
difference = difference.drop([0], axis=0)
difference 


# In[29]:



capomulin_sem = table_mean['Capomulin'].sem()
infubinol_sem = table_mean['Infubinol'].sem()
ketapril_sem = table_mean['Ketapril'].sem()
placebo_sem = table_mean['Placebo'].sem()



#plot with errors graph
fig,ax = plt.subplots()

ax.errorbar(table_mean.index,table_mean['Capomulin'],yerr=capomulin_sem,label='Capomulin',marker='d',linestyle='-.',markersize=5,capsize=5)
ax.errorbar(table_mean.index,table_mean['Infubinol'],yerr=infubinol_sem,label='Infubinol',marker='.',linestyle=':',markersize=8,capsize=5)
ax.errorbar(table_mean.index,table_mean['Ketapril'],yerr=ketapril_sem,label='Ketapril',marker='.',linestyle='-.',markersize=8,capsize=5)
ax.errorbar(table_mean.index,table_mean['Placebo'],yerr=placebo_sem,label='Placebo',marker='d',linestyle=':',markersize=5,capsize=5)

ax.legend(loc='best')
ax.set_xlim(-0.5, 50)
ax.set_ylim(30, 75)
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Tumor Volume (mm3)')
ax.grid(alpha=0.25)

plt.title('Tumor Volume Response to Treatment')
plt.show()

fig.savefig("Figure1.png")


# In[ ]:





# In[ ]:





# In[ ]:




