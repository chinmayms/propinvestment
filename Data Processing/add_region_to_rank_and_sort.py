import pandas as pd
import glob

s3_url = 'YOUR_S3_URL'

county_codes = pd.read_csv('https://' + s3_url + '/propinvana/county_codes.csv',converters={'Code':str})

def match_region(df):
    code = df['Code']
    region = county_codes[county_codes['Code'] == code]['Region'].max()
    return region

def match_state(df):
    code = df['Code']
    region = county_codes[county_codes['Code'] == code]['State'].max()
    return region

for name in glob.glob('*.csv'):
    print(name)
    df = pd.read_csv(name,converters={'Code':str})
    df['Region'] = df.apply(match_region,axis=1)
    df['State'] = df.apply(match_state,axis=1)
    df.sort_values(by=['Value'],ascending=False,inplace=True)
    df.to_csv('new_' + name,index=False)


