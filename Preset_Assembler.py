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
    'Main' : profiles_df.loc[:'Adjustments'].iloc[:-1],
    'Adj' : profiles_df.loc['Adjustments':'Vertical Sky'].iloc[1:-1],
    'Vert Sky' : profiles_df.loc['Vertical Sky':'Vertical Sky Light'].iloc[1:-1],
    'Vert Sky Light' : profiles_df.loc['Vertical Sky Light':'Left Sky'].iloc[1:-1],
    'Left Sky' : profiles_df.loc['Left Sky':'Left Sky Light'].iloc[1:-1],
    'Left Sky Light' : profiles_df.loc['Left Sky Light':'Right Sky'].iloc[1:-1],
    'Right Sky' : profiles_df.loc['Right Sky':'Right Sky Light'].iloc[1:-1],
    'Right Sky Light' : profiles_df.loc['Right Sky Light':].iloc[1:]
}

tones_dict = {
    'Main' : tones_df.loc[:'Adjustments'].iloc[:-1],
    'Adj' : tones_df.loc['Adjustments':'Vertical Sky'].iloc[1:-1],
    'Vert Sky' : tones_df.loc['Vertical Sky':'Vertical Sky Light'].iloc[1:-1],
    'Vert Sky Light' : tones_df.loc['Vertical Sky Light':'Left Sky'].iloc[1:-1],
    'Left Sky' : tones_df.loc['Left Sky':'Left Sky Light'].iloc[1:-1],
    'Left Sky Light' : tones_df.loc['Left Sky Light':'Right Sky'].iloc[1:-1],
    'Right Sky' : tones_df.loc['Right Sky':'Right Sky Light'].iloc[1:-1],
    'Right Sky Light' : tones_df.loc['Right Sky Light':].iloc[1:]
}

styles_dict = {
    'Main' : styles_df.loc['Combo Type':'Adjustments'].iloc[1:-1],
    'Adj' : styles_df.loc['Adjustments':'Vertical Sky'].iloc[1:-1],
    'Vert Sky' : styles_df.loc['Vertical Sky':'Vertical Sky Light'].iloc[1:-1],
    'Vert Sky Light' : styles_df.loc['Vertical Sky Light':'Left Sky'].iloc[1:-1],
    'Left Sky' : styles_df.loc['Left Sky':'Left Sky Light'].iloc[1:-1],
    'Left Sky Light' : styles_df.loc['Left Sky Light':'Right Sky'].iloc[1:-1],
    'Right Sky' : styles_df.loc['Right Sky':'Right Sky Light'].iloc[1:-1],
    'Right Sky Light' : styles_df.loc['Right Sky Light':].iloc[1:]
}

'''
#print(styles_dict['Main']['Vignette'])
#print(tones_dict['Main']['Neutral'].astype(int))
#print(profiles_dict['Main']['Kodak Porta 400 N'].loc['Red Hue':'Balance'])
#df = tones_dict['Main']['Neutral'].add(styles_dict['Main']['Vignette'], fill_value=0)
#df = tones_dict['Main']['Neutral'] + styles_dict['Main']['Vignette']
#print(df)

#df = profiles_dict['Main']['Kodak Porta 400 N'] + tones_dict['Main']['Neutral'] + styles_dict['Main']['Vignette']
with pd.option_context('future.no_silent_downcasting', True):
    df = df.fillna(0).infer_objects(copy=False)
    #print(df)
'''
#print(profiles_dict['Main'])
#print(profiles_dict['Main'][profiles_dict['Main']['Kodak Porta 400 N'].apply(lambda x: isinstance(x, str))])

## Find unique combinations of styles according to combo type
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

'''
## Assemble master presets dict
def combine_styles(base_df, style_lst, mask_df, tone_df, profile_df):
    comb_df = base_df
    for style in style_lst:
       comb_df = comb_df + mask_df[style]
    comb_df = comb_df + tone_df + profile_df
    return comb_df
'''

## Assemble master presets dict
def combine_styles(base_df, style_lst, mask_df, tone_df, profile_df):
    comb_df = base_df
    for style in style_lst:
        #comb_df = comb_df + mask_df[style]
        comb_df = comb_df.add(mask_df[style], fill_value=0)
    comb_df = comb_df.add(tone_df, fill_value=0).add(profile_df, fill_value=0)
    return comb_df

def combine_light_dir(style_name, num_lst, df,df_l=None, df_r=None):
    comb_df = pd.DataFrame()
    comb_df[num_lst[0] + style_name] = df
    if df_l is None: comb_df[num_lst[1] + style_name] = df
    else: comb_df[num_lst[1] + style_name] = df_l
    if df_r is None: comb_df[num_lst[2] + style_name] = df
    else: comb_df[num_lst[2] + style_name] = df_r
    return comb_df

preset_dict = {}
for profile in profiles_df.columns:
    preset_dict[profile] = {}

    # Break up profile dict into int & str
    profile_df_int = profiles_dict['Main'][profiles_dict['Main'][profile].apply(lambda x: isinstance(x, int))]
    profile_df_str = profiles_dict['Main'][profiles_dict['Main'][profile].apply(lambda x: isinstance(x, str))]

    # Initialize empty series
    init_df = profile_df_int
    for col in init_df.columns:
        init_df[col].values[:] = 0
    init_df = init_df[profile].astype(float)

    for tone in tones_df.columns:
        assem_tones_dict = {}
        prof_tone_df = profiles_dict['Main'][profile]+tones_dict['Main'][tone]
        edits_lst = []
        for i in range(len(combo_list)):
            edits_dict = {}
            style_name = " ["+" | ".join(combo_list[i])+"]"     # Style name
            num = str(i+1).zfill(2)                             # Index number
            num_lst = [num, num+"L", num+"R"]                   # Light direction

            # Combine Styles
                # Main
            partial_main_df = combine_styles(init_df,combo_list[i], styles_dict['Main'], tones_dict['Main'][tone], profile_df_int[profile])
            main_df = pd.concat([partial_main_df, profile_df_str[profile]])

                # Masks
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
            edits_dict['Main'] = combine_light_dir(style_name, num_lst, main_df)
            edits_dict['Adj'] = combine_light_dir(style_name, num_lst, adj_df)
            edits_dict['Sky'] = combine_light_dir(style_name, num_lst, vertSky_df, leftSky_df, rightSky_df)
            edits_dict['Sky Lights'] = combine_light_dir(style_name, num_lst, vertSkyLight_df, leftSkyLight_df)
            edits_lst.append(edits_dict)

        # Add edits to master preset dict
        preset_dict[profile][tone] = edits_lst


print(preset_dict['Kodak Porta 400 N']['Orange'])

