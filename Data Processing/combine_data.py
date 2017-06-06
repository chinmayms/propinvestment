import os
import pandas as pd
import glob

def cleandata(df):
    date = str(df['Date'])[:4]
    date = date.replace("-","")
    return date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.join(BASE_DIR,'prop_invest_analysis/data')

count = 0
df = None

for subdir, dirs, files in os.walk(CURRENT_DIR):
    print(subdir)
    if subdir == '/Users/chinmay/Documents/MS/CC/Project/cc_project/prop_invest_analysis/data':
        continue
    code = subdir[62:].split("_")[len(subdir[62:].split("_"))-1]
    code = code.split("/")[0]
    file_name = glob.glob(os.path.join(subdir,'*median_rent*'))[0]
    if 'future' in file_name:
    	if count==0:
	    	df = pd.read_csv(file_name)
	    	df['Code'] = code
	    	count+=1
    	else:
	    	df_temp = pd.read_csv(file_name)
	    	df_temp['Code'] = code
	    	df = pd.concat([df,df_temp])

    else:
    	pass

df.to_csv('combined_median_rent_future.csv',index=False)
    