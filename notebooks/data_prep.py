import pandas as pd
import numpy as np

walkability = pd.read_csv('data/walkability.csv')

health_conditions = pd.read_csv('data/health_conditions.csv')

relevant_columns = [
    'CountyFIPS',
    'DIABETES_AdjPrev',
    'OBESITY_AdjPrev',
    'HIGHCHOL_AdjPrev',
    'CHD_AdjPrev',         # Coronary Heart Disease
    'BPHIGH_AdjPrev'     # Hypertension
]

health_conditions_filtered = health_conditions[relevant_columns]
print(health_conditions_filtered.head())

walkability['STATEFP'] = walkability['STATEFP'].astype(str).str.zfill(2)
walkability['COUNTYFP'] = walkability['COUNTYFP'].astype(str).str.zfill(3)

walkability['CountyFIPS'] = walkability['STATEFP'] + walkability['COUNTYFP']

print(walkability[['STATEFP', 'COUNTYFP', 'CountyFIPS']].head())


# Aggregate walkability by county
walkability_county = walkability.groupby('CountyFIPS').agg({
    'NatWalkInd': 'mean'
}).reset_index()


print("Walkability dataset:", walkability_county.shape)
print("Health conditions dataset:", health_conditions_filtered.shape)

walkability_county['CountyFIPS'] = walkability_county['CountyFIPS'].astype(str).str.zfill(5)
health_conditions_filtered['CountyFIPS'] = health_conditions_filtered['CountyFIPS'].astype(str).str.zfill(5)
merged = pd.merge(walkability_county, health_conditions_filtered, on='CountyFIPS', how='inner')
print("Merged dataset:", merged.shape)

merged.info()
merged.describe()
merged.isnull().sum()

merged.to_csv('merged_data.csv', index=False)







