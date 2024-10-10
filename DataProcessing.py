
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

token = os.environ.get("INFLUXDB_TOKEN")
org = "Horizon"
url = "http://localhost:8086"


bucket="Horizon-data"

client = influxdb_client.InfluxDBClient( 
  url=config.get('APP', 'INFLUX_URL'),
  token=config.get('APP','INFLUXDB_TOKEN'),
  org=config.get('APP','INFLUX_ORG')

)
write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    
    .field("field1", value)
  )
  
  point = point.tag("tagname2", "tagvalue2")
  write_api.write(bucket=bucket, org=org, record=point)
  time.sleep(1) # separate points by 1 second


query_api = client.query_api()

query = """from(bucket: "Horizon-data")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query = query, org="Horizon")

for table in tables:
  for record in table.records:
    print(type(record.values))
    
