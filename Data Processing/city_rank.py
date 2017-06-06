import pandas as pd
import glob, os, csv

dir_path = os.path.dirname(os.path.realpath(__file__))

def calculate_gross_income(dir_path,investment_end_year):

    future_path = os.path.join(dir_path, 'future')

    file = glob.glob(os.path.join(future_path, '*median_rent*'))

    df = pd.read_csv(os.path.join(future_path, file[0]))

    df = df[df['Date'] <= investment_end_year]

    total_rent_accumulated = df['Value'].sum()

    file = glob.glob(os.path.join(future_path, '*all_homes*'))

    df = pd.read_csv(os.path.join(future_path, file[0]))

    df = df[df['Date'] == investment_end_year]

    estimated_price_of_house = df['Value'].max()

    return (total_rent_accumulated*12)+estimated_price_of_house

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.join(BASE_DIR,'prop_invest_analysis/data')

current_year = 2017
ten_year_period_ends = current_year+10

for year in range(current_year+1, ten_year_period_ends+1):
    filename = 'rank_' + str(year) + '.csv'
    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['County', 'Code', 'Value'])
        for subdir, dirs, files in os.walk(CURRENT_DIR):
            if subdir == '/Users/chinmay/Documents/MS/CC/Project/cc_project/prop_invest_analysis/data':
                continue
            if subdir.split("/")[len(subdir.split("/"))-1] == 'future':
                continue
            print(subdir)
            county_combo = subdir.split("/")[len(subdir.split("/"))-1]
            if len(county_combo.split("_")) == 3:
                county_name = county_combo.split("_")[len(county_combo.split("_"))-3] + '_' + county_combo.split("_")[len(county_combo.split("_"))-2]
            else:
                county_name = county_combo.split("_")[len(county_combo.split("_"))-2]

            county_code = county_combo.split("_")[len(county_combo.split("_"))-1]
            inc = calculate_gross_income(subdir, year)
            filewriter.writerow([county_name, county_code, inc])