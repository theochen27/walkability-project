import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# === 1. Load merged dataset ===
df = pd.read_csv("data/merged_data.csv", dtype={"CountyFIPS": str})
df["CountyFIPS"] = df["CountyFIPS"].str.zfill(5)  # ensure proper FIPS format

# === 2. Load U.S. counties shapefile ===
gdf = gpd.read_file("resources/cb_2022_us_county_20m.shp")
gdf["FIPS"] = (gdf["STATEFP"] + gdf["COUNTYFP"]).astype(str).str.zfill(5)

# === 3. Merge health/walkability data with geometry ===
# Keep only the 48 contiguous states + DC
continental_states = [
    '01','04','05','06','08','09','10','11','12','13','16','17','18','19','20',
    '21','22','23','24','25','26','27','28','29','30','31','32','33','34','35',
    '36','37','38','39','40','41','42','44','45','46','47','48','49','50','51',
    '53','54','55','56'
]
gdf = gdf[gdf["STATEFP"].isin(continental_states)]

merged = gdf.merge(df, left_on="FIPS", right_on="CountyFIPS")

# === 4. Variables to map ===
merged.rename(columns={
    'DIABETES_AdjPrev': 'Diabetes',
    'OBESITY_AdjPrev': 'Obesity',
    'BPHIGH_AdjPrev': 'Hypertension',
    'CHD_AdjPrev': 'CoronaryHeartDisease',
    'HIGHCHOL_AdjPrev': 'HighCholesterol',
}, inplace=True)
print(merged.head())

variables = ["NatWalkInd", "Obesity", "Diabetes", "Hypertension", "CoronaryHeartDisease", "HighCholesterol"]

# === 5. Output directory ===
os.makedirs("output", exist_ok=True)

# === 6. Generate and save maps ===
for var in variables:
    fig, ax = plt.subplots(figsize=(12, 8))

    merged.plot(
        column=var,
        cmap="OrRd",
        linewidth=0.2,
        edgecolor="white",
        ax=ax,
        legend=True,
        legend_kwds={
            'label': f"{var}",
            'shrink': 0.6,
            'orientation': "vertical"
        }
    )

    ax.axis("off")
    ax.set_title(f"{var} by County", fontsize=20, weight='bold')

    # Crop tightly to the map extent
    ax.set_xlim(merged.total_bounds[[0, 2]])
    ax.set_ylim(merged.total_bounds[[1, 3]])

    # Save as PNG
    plt.savefig(f"output/choropleth_{var}.png", dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close()

