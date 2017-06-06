import quandl
import pandas as pd
import os
import time

key = ["u3tavysA_FXPPykmn46q", "hetDNix7grwmddPzbwr5", "sonBFeMcfzBxcyEkUc3G", "Aigs_vLuXpEesKwWj4vV", "9aa_p2CBRzRrSF5ah-wD", "T5rcU6W-BwM8Ny7gueiq", "c5yNDDWgtq1SsyFKnufA", "K395GbX_gnTHxvj2yk2D", "yexpCnJcZhDSuVoHsXHG", "zDpwFtyUskiCK3qkGoLH", "z9r5DWs3T4EDrvgygR-e", "8CS4E2yQ-SbDkg-hkmuq", "GW2QBq7S3xspyxp345Ce", "qrTzGKq_BhJDXY5gdnXs", "2HuehuxVgciBWJmBnfzv", "BDZjzpotcrnXnGjPqH_M", "G9SZzoSTRyaihQZFDzuf"]
i = 0
quandl.ApiConfig.api_key = key[i]
n = 0
print(key[i])

attributes = ['A','SF', 'C', 'MVSF', '1B', '2B', '3B', '4B', '5B', 'BT', 'MT', 'TT', 'RMP', 'RAH', 'RZSF', 'PRR', 'MLP', 'MSP', 'MLPSF', 'MSPSF', 'LPC', 'MPC', 'SLPR', 'SFL', 'SFG', 'IV', 'DV', 'SPY', 'HR', 'HF', 'FR']
att = {
	'A': 'all_homes',
	'SF': 'single_family_res',
	'C': 'condominiums',
	'MVSF': 'price_per_sq_foot',
	'1B': '1_bed',
	'2B': '2_bed',
	'3B': '3_bed',
	'4B': '4_bed',
	'5B': '5_bed_plus',
	'BT': 'bottom_tier',
	'MT': 'middle_tier',
	'TT': 'top_tier',
	'RMP': 'median_rent',
	'RAH': 'estimated_rent',
	'RZSF': 'estimated_rent_per_sq_foot',
	'PRR': 'price_to_rent_ratio',
	'MLP': 'median_lp',
	'MSP': 'median_sp',
	'MLPSF': 'median_lp_per_sq_foot',
	'MSPSF': 'median_sp_per_sq_foot',
	'LPC': 'listings_with_price_cut',
	'MPC': 'median_price_cut',
	'SLPR': 'ratio_of_sp_to_lp',
	'SFL': 'sold_for_loss',
	'SFG': 'sold_for_gain',
	'IV': 'increasing_values',
	'DV': 'decreasing_values',
	'SPY': 'turnover_in_housing_market',
	'HR': 'number_of_homes_for_rent',
	'HF': 'monthly_foreclosures',
	'FR': 'percentage_of_sales_that_were_foreclosures'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.join(BASE_DIR,'prop_invest_analysis/data')
df = pd.read_csv('example.csv')
for index,row in df.iterrows():
	print(row['Code'])
	for a in attributes:
		if(n % 300 == 0 and n):
			time.sleep(10)
		if(n % 2000 == 0 and n):
			time.sleep(600)
		if(n % 50000 == 0 and n):
			i = i + 1
			quandl.ApiConfig.api_key = key[i]
			print(key[i])
		link = "ZILL/C" + row['Code'][1:] + "_" + a
		try:
			n = n + 1
			mydata = quandl.get(link)
			if not os.path.exists(CURRENT_DIR + '/' + row['County'] + '_' + row['Code'][1:]):
				os.makedirs(CURRENT_DIR + '/' + row['County'] + '_' + row['Code'][1:],777)
				CURR_DIR = os.path.join(CURRENT_DIR, row['County'] + '_' + row['Code'][1:])
				os.chmod(CURR_DIR, 0777)
			filename = row['County']+'_' + att[a] + '.csv'
			file_path = os.path.join(CURR_DIR,filename)
			mydata.to_csv(file_path)
		except Exception as e:
			print(e)