import pandas as pd
import numpy as np
import os
import glob

def cleandata(date):
    x = len(str(date))
    date = str(date)[:4]
    date = date.replace("-","")
    return date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_path = os.path.join(BASE_DIR,'prop_invest_analysis/data')

for name in glob.glob('*.csv'):
    print(name)
    df = pd.read_csv(name, converters={'Code': str})
    df['1_bed'] = 0.0
    df['2_bed'] = 0.0
    df['3_bed'] = 0.0
    df['4_bed'] = 0.0
    df['5_bed'] = 0.0
    df['condo'] = 0.0
    df['single'] = 0.0

    for index, row in df.iterrows():
        current_dir = os.path.join(dir_path, row['County'] + '_' + row['Code'])
        print(current_dir)

        df_1br = pd.read_csv(glob.glob(os.path.join(current_dir, '*1_bed*'))[0])
        df_1br['Date'] = df_1br['Date'].apply(cleandata)
        df_1br.sort_values(by='Date', ascending=False, inplace=True)
        df_1br.set_index(np.arange(len(df_1br.index)), inplace=True)

        df_2br = pd.read_csv(glob.glob(os.path.join(current_dir, '*2_bed*'))[0])
        df_2br['Date'] = df_2br['Date'].apply(cleandata)
        df_2br.sort_values(by='Date', ascending=False, inplace=True)
        df_2br.set_index(np.arange(len(df_2br.index)), inplace=True)

        df_3br = pd.read_csv(glob.glob(os.path.join(current_dir, '*3_bed*'))[0])
        df_3br['Date'] = df_3br['Date'].apply(cleandata)
        df_3br.sort_values(by='Date', ascending=False, inplace=True)
        df_3br.set_index(np.arange(len(df_3br.index)), inplace=True)

        df_4br = pd.read_csv(glob.glob(os.path.join(current_dir, '*4_bed*'))[0])
        df_4br['Date'] = df_4br['Date'].apply(cleandata)
        df_4br.sort_values(by='Date', ascending=False, inplace=True)
        df_4br.set_index(np.arange(len(df_4br.index)), inplace=True)

        df_5br = pd.read_csv(glob.glob(os.path.join(current_dir, '*5_bed_plus*'))[0])
        df_5br['Date'] = df_5br['Date'].apply(cleandata)
        df_5br.sort_values(by='Date', ascending=False, inplace=True)
        df_5br.set_index(np.arange(len(df_5br.index)), inplace=True)

        df_condo = pd.read_csv(glob.glob(os.path.join(current_dir, '*condominiums*'))[0])
        df_condo['Date'] = df_condo['Date'].apply(cleandata)
        df_condo.sort_values(by='Date', ascending=False, inplace=True)
        df_condo.set_index(np.arange(len(df_condo.index)), inplace=True)

        df_single = pd.read_csv(glob.glob(os.path.join(current_dir, '*single_family_res*'))[0])
        df_single['Date'] = df_single['Date'].apply(cleandata)
        df_single.sort_values(by='Date', ascending=False, inplace=True)
        df_single.set_index(np.arange(len(df_single.index)), inplace=True)

        df['1_bed'][index] = df_1br['Value'][0]
        df['2_bed'][index] = df_2br['Value'][0]
        df['3_bed'][index] = df_3br['Value'][0]
        df['4_bed'][index] = df_4br['Value'][0]
        df['5_bed'][index] = df_5br['Value'][0]
        df['condo'][index] = df_condo['Value'][0]
        df['single'][index] = df_single['Value'][0]

    df.to_csv(name[4:],index=False)