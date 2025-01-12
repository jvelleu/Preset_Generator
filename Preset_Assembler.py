"""
Preset Assembler imports Preset_Variables.xlsx and assembles & outputs .xmp files
for each Lightroom/Camera Raw preset.

@author: Jesse Velleu | jvelleu
1-09-24
"""

import pandas as pd
from itertools import combinations
import random

## Read data
read_dir = "preset_variables.xlsx"
profiles_df = pd.read_excel(read_dir,sheet_name="Profiles",index_col=0)
tones_df = pd.read_excel(read_dir,sheet_name="Tones",index_col=0)
styles_df = pd.read_excel(read_dir,sheet_name="Style Masks",index_col=0)
core_df = pd.read_excel(read_dir,sheet_name="Core Masks",index_col=0)

## Split profiles, tones, and styles df into main edits & masks
profiles_dict = {
    'Main' : profiles_df.iloc[:72],
    'Adj' : profiles_df.iloc[73:96],
    'Vert Sky' : profiles_df.iloc[97:120],
    'Vert Sky Light' : profiles_df.iloc[121:144],
    'Left Sky' : profiles_df.iloc[145:168],
    'Left Sky Light' : profiles_df.iloc[169:192],
    'Right Sky' : profiles_df.iloc[193:216],
    'Right Sky Light' : profiles_df.iloc[217:240]
}

tones_dict = {
    'Main' : tones_df.iloc[:37],
    'Adj' : tones_df.iloc[38:61],
    'Vert Sky' : tones_df.iloc[62:85],
    'Vert Sky Light' : tones_df.iloc[86:109],
    'Left Sky' : tones_df.iloc[110:133],
    'Left Sky Light' : tones_df.iloc[134:157],
    'Right Sky' : tones_df.iloc[158:181],
    'Right Sky Light' : tones_df.iloc[182:205]
}

styles_dict = {
    'Main' : tones_df.iloc[25:30],  # Vignette
    'Adj' : styles_df.iloc[2:25],
    'Vert Sky' : styles_df.iloc[31:54],
    'Vert Sky Light' : styles_df.iloc[55:78],
    'Left Sky' : styles_df.iloc[79:102],
    'Left Sky Light' : styles_df.iloc[103:126],
    'Right Sky' : styles_df.iloc[127:150],
    'Right Sky Light' : styles_df.iloc[151:174]
}

'''
tones_adj_df = tones_df.iloc[38:61]
tones_vertSky_df = tones_df.iloc[62:85]
tones_vertSkyLight_df = tones_df.iloc[86:109]
tones_leftSky_df = tones_df.iloc[110:133]
tones_leftSkyLight_df = tones_df.iloc[134:157]
tones_rightSky_df = tones_df.iloc[158:181]
tones_rightSkyLight_df = tones_df.iloc[182:205]
tones_df = tones_df.iloc[:37]
styles_adj_df = styles_df.iloc[2:25]
styles_vertSky_df = styles_df.iloc[31:54]
styles_vertSkyLight_df = styles_df.iloc[55:78]
styles_leftSky_df = styles_df.iloc[79:102]
styles_leftSkyLight_df = styles_df.iloc[103:126]
styles_rightSky_df = styles_df.iloc[127:150]
styles_rightSkyLight_df = styles_df.iloc[151:174]
vignette_df = styles_df.iloc[25:30]
profiles_adj_df = profiles_df.iloc[73:96]
profiles_vertSky_df = profiles_df.iloc[97:120]
profiles_vertSkyLight_df = profiles_df.iloc[121:144]
profiles_df = profiles_df.iloc[:72]
'''

## Create unique combinations of styles according to combo type
def find_unique_combinations(df):
    valid_combinations = []
    # Iterate through combinations of 1 to 4 columns
    for r in range(1, 5):
        for cols in combinations(df.columns, r):
            # Check if any row in the subset has duplicate strings
            subset = df[list(cols)]
            if all(subset.nunique(axis=1) == subset.shape[1]):
                valid_combinations.append(cols)
    return valid_combinations

combos_df = styles_df.iloc[:1]
combo_list = find_unique_combinations(combos_df)
# Add in Base
combo_list.insert(0,tuple(['Base']))

## Assemble master presets dict
def combine_styles(base_df, style_lst, mask_df, tone_df, profile_df):
    comb_df = base_df
    for style in style_lst:
       comb_df = comb_df + mask_df[style]
    comb_df = comb_df + tone_df + profile_df
    return comb_df

def combine_lightDir(style_name, num_lst, df,df_L=None, df_R=None):
    comb_df = pd.DataFrame()
    comb_df[num_lst[0] + style_name] = df
    if df_L is None: comb_df[num_lst[1] + style_name] = df
    else: comb_df[num_lst[1] + style_name] = df_L
    if df_R is None: comb_df[num_lst[2] + style_name] = df
    else: comb_df[num_lst[2] + style_name] = df_R
    return comb_df

preset_dict = {}
for profile in profiles_df.columns:
    preset_dict[profile] = {}
    for tone in tones_df.columns:
        edits_dict = {}
        mask_adj_lst = []
        for i in range(len(combo_list)):
            style_name = " ["+" | ".join(combo_list[i])+"]"     # Style name
            num = str(i+1).zfill(2)                             # Index number
            num_lst = [num, num+"L", num+"R"]                   # Light direction
            # Base Edits

            # Style Masks
            # Combine Styles
            base_df = styles_dict['Adj']['Base']
            adj_df = combine_styles(base_df,combo_list[i], styles_dict['Adj'], tones_dict['Adj'][tone], profiles_dict['Adj'][profile])
            vertSky_df = combine_styles(base_df,combo_list[i], styles_dict['Vert Sky'], tones_dict['Vert Sky'][tone],
                                        profiles_dict['Vert Sky'][profile])
            leftSky_df = combine_styles(base_df,combo_list[i], styles_dict['Left Sky'], tones_dict['Left Sky'][tone],
                                        profiles_dict['Left Sky'][profile])
            rightSky_df = combine_styles(base_df,combo_list[i], styles_dict['Right Sky'], tones_dict['Right Sky'][tone],
                                        profiles_dict['Right Sky'][profile])
            vertSkyLight_df = combine_styles(base_df, combo_list[i], styles_dict['Vert Sky Light'], tones_dict['Vert Sky Light'][tone],
                                        profiles_dict['Vert Sky Light'][profile])
            leftSkyLight_df = combine_styles(base_df, combo_list[i], styles_dict['Left Sky Light'], tones_dict['Left Sky Light'][tone],
                                        profiles_dict['Left Sky Light'][profile])
            rightSkyLight_df = combine_styles(base_df, combo_list[i], styles_dict['Right Sky Light'], tones_dict['Right Sky Light'][tone],
                                        profiles_dict['Right Sky Light'][profile])

            # Combine Light Directions & add to dict
            edits_dict['Adj'] = combine_lightDir(style_name, num_lst, adj_df)
            edits_dict['Sky'] = combine_lightDir(style_name, num_lst, vertSky_df, leftSky_df, rightSky_df)
            edits_dict['Sky Lights'] = combine_lightDir(style_name, num_lst, vertSkyLight_df, leftSkyLight_df)

        # Add edits to master preset dict
        preset_dict[profile][tone] = edits_dict

print(preset_dict['Kodak Porta 400 N']['Neutral']['Sky'])

