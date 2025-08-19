import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import geopandas as gpd

sns.set(style="whitegrid")

merged = pd.read_csv("data/merged_data.csv")

numeric_cols = merged.select_dtypes(include=['float64', 'int64']).columns

for col in numeric_cols:
    median_val = merged[col].median()
    merged[col].fillna(median_val, inplace=True)

missing = merged.isnull().sum()

merged.rename(columns={
    'DIABETES_AdjPrev': 'Diabetes',
    'OBESITY_AdjPrev': 'Obesity',
    'BPHIGH_AdjPrev': 'Hypertension',
    'CHD_AdjPrev': 'CoronaryHeartDisease',
    'HIGHCHOL_AdjPrev': 'HighCholesterol',
}, inplace=True)
print(merged.head())


# merged.hist(figsize=(12, 10))
# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.heatmap(merged.corr(), annot=True, cmap='coolwarm')
# plt.title('Correlation matrix')
# plt.show()

variables = ['Diabetes', 'Obesity', 'Hypertension', 'CoronaryHeartDisease', 'HighCholesterol']

# for var in variables:
#     plt.figure(figsize=(8, 5))
#     sns.regplot(data=merged, x='NatWalkInd', y=var, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
#     plt.title(f'Walkability vs {var} (Adjusted Prevalence)')
#     plt.xlabel('National Walkability Index')
#     plt.ylabel(var)
#     plt.show()

for var in variables:
    corr_coef, p_value = pearsonr(merged['NatWalkInd'], merged[var])
    print(f"{var}: Pearson r = {corr_coef:.3f}, p-value = {p_value:.3g}")

# data = {
#     "Variable": ["Diabetes", "Obesity", "Hypertension", "Coronary Heart Disease", "High Cholesterol"],
#     "Pearson r": [-0.262, -0.443, -0.385, -0.461, -0.212],
#     "p-value": ["2.55e-50", "1.45e-150", "2.91e-111", "1.59e-164", "3.74e-33"]
# }
# df = pd.DataFrame(data)

# # Plot table
# fig, ax = plt.subplots(figsize=(10, 2.5))
# ax.axis('off')
# table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
# table.auto_set_font_size(False)
# table.set_fontsize(12)
# table.scale(1.2, 1.5)

# plt.show()



# ---------------------------------------------------------------
# Normal Distribution
# ---------------------------------------------------------------

new_variables = ['NatWalkInd', 'Diabetes', 'Obesity', 'Hypertension', 'CoronaryHeartDisease', 'HighCholesterol']
for var in new_variables:
    plt.figure(figsize=(10,6))
    sns.histplot(merged[var], kde=True, color="skyblue")
    plt.title(f"Distribution of {var} Across Counties", fontsize=18)
    plt.xlabel(var)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"output/distribution_{var}.png", dpi=300)
    plt.close()