import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import configparser
import csv
from dateutil.parser import parse
from Processors import Processor
import pandas as pd
    
class Config:    
    def read_config (self, file):
        config = configparser.ConfigParser()
        config.read(file)
        return config

class DataSeriesDataset:
        
    def __init__(self, config:configparser, bucket):
        self.bucket=bucket
        self.url = config.get('APP', 'INFLUX_URL')
        self.token='GFdyou7GH1b1Rnduk_Eiueb_zuk6ONC8MKAP4NROKgXAqZyYc8zmVDMbC6b3aDdXyvC9kLngstfNEtOrPw_RSQ=='
        self.org='Horizon_lab'
        self.client = influxdb_client.InfluxDBClient( 
                                                    url=self.url,
                                                    token=self.token,
                                                    org=self.org)
        
        
    def read_csv_file(self, file_path:str, sep:str, time_field:str, dayfirstind:bool, measurment:str, encode:str='utf-8') ->dict:
        with open (file_path, encoding=encode) as data_file:
            data = csv.DictReader(data_file, delimiter=sep)
            result = []
            for row in data:
                row['time'] = parse((row[time_field]), dayfirst=dayfirstind).isoformat() + 'Z'
                del row[time_field]       
                result.append({measurment:row})
        # print(result)
        return result
    
    
        
    def write_data (self,  data:dict):
       write_api = self.client.write_api(write_options=SYNCHRONOUS)
       print(data)
       for key,value in data.items():
           point = Point(key)
           tags = list(filter(lambda tag: True if 'tag' in tag else False, value.keys()))
           fields = list(filter(lambda tag: True if ('tag' not in tag) & ('time' not in tag) else False, value.keys()))
           time_field = list(filter(lambda tag: True if (tag == 'time') else False, value.keys())) 
           point = point.time(value[time_field[0]])
           for tag in tags:
               point = point.tag(tag, value[tag])
           for field in fields:
               point = point.field(field, value[field])
       print(point)
       write_api.write(bucket=self.bucket, org=self.org, record=point)
       time.sleep(1) # separate points by 1 second
       
       
    def df_forming (self, tables):
        data = []
        for table in tables:
            for record in table.records:
                data.append(record.values)
        return pd.DataFrame(data)
        
       
    def query_to_db (self, start, query_api , stop, measurement = '"social"', field = 'all'):
        if field != 'all':
            query = f'''from(bucket: "Horizon")
            |> range(start: {start}, stop:{stop})
            |> filter(fn: (r) => r._measurement == {measurement})
            |> filter(fn: (r) => r._field == {field})'''
            
        else:
            query = f'''from(bucket: "Horizon")
            |> range(start: {start}, stop:{stop})
            |> filter(fn: (r) => r._measurement == {measurement})'''
        tables = query_api.query(query = query, org="Horizon_lab")
        return tables
    
    def dataframe_transform (self, df):
        result_df = df.pivot_table(index=['_time'], columns=['_field'], values='_value', aggfunc='first').reset_index()
        result_df.columns.name = None  # Удаляем имя индекса
        result_df.rename(columns={'_time': 'time'}, inplace=True)
        return result_df
       
def main():
    # data = {'measurment2':{'time':"2024-09-09T10:00:00.123456Z", "field1":4, "field2":5}}
    
    config = Config()
    conf = config.read_config('horizon/config.ini')
    dataset = DataSeriesDataset(conf, 'Horizon')
    
    data = dataset.read_csv_file('horizon/social_data_last.csv', ';', 'Период', True, 'social', 'cp1251')
    data = Processor.dict_value_to_int(data)
    # for item in data:
    #     dataset.write_data(item)

    tables = dataset.query_to_db('2013-01-01T00:00:00Z', dataset.client.query_api(), '2022-10-01T00:00:00Z')
    df = dataset.df_forming(tables)
   

    # Преобразование DataFrame
    result_df = dataset.dataframe_transform(df)
    result_df.to_csv('result.csv')
                
if __name__=='__main__':
    main()