"""
Preset Assembler imports Preset_Variables.xlsx and assembles & outputs .xmp files
for each Lightroom/Camera Raw preset.

@author: Jesse Velleu | jvelleu
1-09-24
"""

import pandas as pd

## Read data
read_dir = "Preset_Variables.xlsx"
tones_df = pd.read_excel(read_dir,sheet_name="Tones",index_col=0)
custom_mask_df = pd.read_excel(read_dir,sheet_name="Custom Mask Adj.",index_col=0)
core_mask_df = pd.read_excel(read_dir,sheet_name="Core Mask Adj.",index_col=0)
profiles_df = pd.read_excel(read_dir,sheet_name="Profiles",index_col=0)

## Split Dataframes
tones_adj_df = tones_df.iloc[38:61]
tones_vertSky_df = tones_df.iloc[62:85]
tones_vertSkyLight_df = tones_df.iloc[86:109]
tones_leftSky_df = tones_df.iloc[110:133]
tones_leftSkyLight_df = tones_df.iloc[134:157]
tones_rightSky_df = tones_df.iloc[158:181]
tones_rightSkyLight_df = tones_df.iloc[182:205]
tones_df = tones_df[:37]
mask_adj_df = custom_mask_df.iloc[2:30]
mask_vertSky_df = custom_mask_df.iloc[31:54]
mask_vertSkyLight_df = custom_mask_df.iloc[55:78]

print(mask_vertSkyLight_df)

## Combine Metrics
#test_df =  tones_df['Neutral'] + profiles_df['Kodak Porta 400 N']
#for col in tones_df.columns:
#    print(tones_df)