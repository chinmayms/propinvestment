from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import json, requests
import pandas as pd

# Create your views here.
s3 = 'YOUR_S3_URL'
df_all_homes = pd.read_csv('https://' + s3 + '/propinvanarank/combined_all_homes.csv', converters={'Code': str})
df_all_homes_future = pd.read_csv('https://' + s3 + '/propinvanarank/combined_all_homes_future.csv', converters={'Code': str})
df_rent = pd.read_csv('https://' + s3 + '/propinvanarank/combined_median_rent.csv', converters={'Code': str})
df_rent_future = pd.read_csv('https://' + s3 + '/propinvanarank/combined_median_rent_future.csv', converters={'Code': str})

def home(request):
	return render(request, "index.html", {})

def about(request):
	return render(request, "about.html", {})

def contact(request):
	return render(request, "contact.html", {})

def getlocation(loc):
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=YOUR_API_KEY' % loc) #YOUR_API_KEY = Google Maps API Key
	resp_json_payload = response.json()
	return resp_json_payload['results'][0]['geometry']['location']

def getRentGraphData(code):
	df = df_rent[df_rent['Code']==code]
	df['Date'] = df['Date'].apply(cleandata)
	df1 = df_rent_future[df_rent_future['Code']==code]
	df = df.groupby('Date', as_index=False).mean()
	df = pd.concat([df,df1])
	df.reset_index(inplace=True,drop=True)
	a = []
	b= []
	arr = []
	arr.append(a)
	arr.append(b)
	for index, row in df.iterrows():
		arr[0].append(row['Date'])
		arr[1].append( row['Value'])
	return arr

def getHouseGraphData(code):
	df = df_all_homes[df_all_homes['Code']==code]
	df['Date'] = df['Date'].apply(cleandata)
	df1 = df_all_homes_future[df_all_homes_future['Code']==code]
	df = df.groupby('Date', as_index=False).mean()
	df = pd.concat([df,df1])
	df1.reset_index(inplace=True,drop=True)
	a = []
	b= []
	arr = []
	arr.append(a)
	arr.append(b)
	for index, row in df.iterrows():
		arr[0].append(row['Date'])
		arr[1].append( row['Value'])
	return arr

def getGraphData1(code):
	df = df_all_homes_future[df_all_homes_future['Code']==code]
	df1 = df_all_homes[df_all_homes['Code']==code]
	df1['Date'] = df1['Date'].apply(cleandata)
	df1 = df1.groupby('Date', as_index=False).mean()
	df1 = pd.concat([df1,df])
	df1.reset_index(inplace=True,drop=True)
	df2 = df_rent_future[df_rent_future['Code']==code]
	df3 = df_rent[df_rent['Code']==code]
	df3['Date'] = df3['Date'].apply(cleandata)
	df3 = df3.groupby('Date', as_index=False).mean()
	df3 = pd.concat([df3,df2])
	df3.reset_index(inplace=True,drop=True)
	df3.rename(columns={'Value':'rent_value'})
	df4 = pd.merge(df1,df3,on='Date')
	a = []
	b= []
	arr = []
	arr.append(a)
	arr.append(b)
	for index, row in df4.iterrows():
		arr[0].append(row['Value_x'])
		arr[1].append( row['Value_y'])
	return arr

def cleandata(date):
    x = len(str(date))
    date = str(date)[:4]
    date = date.replace("-","")
    return date

@csrf_protect
def map(request):
	budget = int(str(request.POST.get('budget')))
	years = int(str(request.POST.get('years')))
	state = str(request.POST.get('state'))
	df = pd.read_csv('https://' + s3 + '/propinvanarank/rank_' + str(2017 + years)+ '.csv', converters={'Code': str})
	print(df_rent.head())
	i=1
	pass_list = {}
	for index, row in df.iterrows():
		try:
			if i > 50:
				break
			elif state == 'ALL':
				doc = {
					'County': row['County'].replace('_', ' '),
					'Region': row['Region'],
					'State': row['State']
				}
				YOUR_LOCATION = row['County'].replace('_', ' ') + ', ' + row['Region'] + ', ' + row['State']
				if budget >= int(row['5_bed']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '5_bed_plus'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['4_bed']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '4_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['single']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = 'single'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['3_bed']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '3_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['2_bed']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '2_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['1_bed']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '1_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['condo']):
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = 'condo'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
			else:
				doc = {
					'County': row['County'].replace('_', ' '),
					'Region': row['Region'],
					'State': row['State']
				}
				YOUR_LOCATION = row['County'].replace('_', ' ') + ', ' + row['Region'] + ', ' + row['State']
				if budget >= int(row['5_bed']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '5_bed_plus'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['4_bed']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '4_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['single']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = 'single'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['3_bed']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '3_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['2_bed']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '2_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['1_bed']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = '1_bed'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
				elif budget >= int(row['condo']) and row['State'] == state:
					location = getlocation(YOUR_LOCATION)
					doc['Property'] = 'condo'
					doc['location'] = location
					doc['medianHouseValue'] = getHouseGraphData(row['Code'])
					doc['medianRentValue'] = getRentGraphData(row['Code'])
					doc['medianHouseToRentValue'] = getGraphData1(row['Code'])
					pass_list[i] = doc
					i+=1
		except Exception as e:
			print(e)
	return render(request, "map.html", {'list': json.dumps(pass_list)})