import pandas as pd
import numpy as np

file_path = "/Users/lukaslaskowski/Documents/SAP/Data/blazegraph (1)/RBA and RSA 2306 Release Excel V1.4.xlsx"
xls = pd.ExcelFile(file_path)
df_SCM = pd.read_excel(xls, 'Solution Capability Model')

df_SCM_sar = df_SCM[['Object ID SC','Solution Capability Reference Architecture Hybrid','Solution Capability Reference Architecture Cloud']]
df_SCM_sar = df_SCM_sar.melt(id_vars=["Object ID SC"], var_name="SAR", value_name="Value")
df_SCM_sar.replace('Solution Capability Reference Architecture Cloud', 'Reference Architecture Cloud', inplace=True)
df_SCM_sar.replace('Solution Capability Reference Architecture Hybrid', 'Reference Architecture Hybrid', inplace=True)
filter = df_SCM_sar["Value"]==1.0
df_SCM_sar.where(filter, inplace = True)
df_SCM_sar = df_SCM_sar.dropna()
print(df_SCM_sar[df_SCM_sar['Object ID SC'] == 'SC3444'])
#print(df_SAR.head())

sar_title_list = ['Reference Architecture Hybrid', 'Reference Architecture Cloud','Whitespaces - Reference Architecture Hybrid','Whitespaces - Reference Architecture Cloud']

sar_co = pd.DataFrame(columns=['Title','Description','Identifier','Name','isInstanceOfType','UniformName'])
sar_co['Title'] = sar_title_list
sar_co['Identifier'] = ((sar_co.index+1).astype(str)).str.zfill(3)
sar_co['Description'] = ''
sar_co['Name'] = sar_co['Title']
#print(sar_co)

sar_dict = dict(zip(sar_co['Title'], sar_co['Identifier']))