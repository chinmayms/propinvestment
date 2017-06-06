import pandas as pd
import glob
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
import os
import shutil
import boto3
from boto3 import client
from io import StringIO

def cleandata(date):
    x = len(str(date))
    date = str(date)[:4]
    date = date.replace("-","")
    return date

def addcolon(df):
    temp = df['Date']
    temp = "1:" + str(temp)
    return temp

def clean_features(input):
    temp = str(input).split(",")

    return int(temp[2][1:5])

spark = SparkSession\
    .builder\
    .appName("LinearRegressionWithElasticNet")\
    .getOrCreate()

dir_path = os.path.dirname(os.path.realpath(__file__))

temp_dir = os.path.join(dir_path,'temp')

s3 = boto3.resource('s3')

s3_url = 'YOUR_S3_URL'

conn = client('s3')

for key in conn.list_objects(Bucket='propinvana')['Contents']:

    print(key['Key'])

    df = pd.read_csv("https://" + s3_url + "/propinvana/" + key['Key'])

    df['Date'] = df['Date'].apply(cleandata)

    df['Date'] = df.apply(addcolon, axis=1)

    df['feature'] = df['Date']

    df.drop('Date', axis=1, inplace=True)

    df.to_csv(os.path.join(dir_path,'temp_' + key['Key']), index=False, sep=' ', header=False)

    data = spark.read.format("libsvm") \
        .load(os.path.join(dir_path,'temp_' + key['Key']))

    test_data = spark.read.format("libsvm").load("final.csv")

    lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

    # Fit the model
    lrModel = lr.fit(data)

    real_preds = lrModel.transform(test_data)

    real_preds = real_preds.select(real_preds['features'], real_preds['prediction'])

    clean = udf(clean_features)

    real_preds = real_preds.select(clean(real_preds['features']).alias('Date'), real_preds['prediction'].alias('Value'))

    real_preds.show()

    real_preds.write.option("header", "false").csv("temp")

    temp_name = glob.glob(os.path.join(temp_dir, '*.csv'))

    df = pd.read_csv(temp_name[0], names=['Date', 'Value'])

    csv_buffer = StringIO()

    df.to_csv(csv_buffer)

    s3.Bucket('propinvanafuture').put_object(Key='future_' + key['Key'], Body=csv_buffer.getvalue(), ACL='public-read-write')

    shutil.rmtree(os.path.join(dir_path,'temp'))

    os.remove(os.path.join(dir_path,'temp_' + key['Key']))