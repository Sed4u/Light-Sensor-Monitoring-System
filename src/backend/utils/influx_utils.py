from influxdb_client import InfluxDBClient

def delete_luxdata_for_user(user_id):
    client = InfluxDBClient(url="http://influxdb:8086", token="mds-token", org="mds")
    delete_api = client.delete_api()
    start = "1970-01-01T00:00:00Z"
    stop = "2100-01-01T00:00:00Z"
    predicate = f'_measurement="lumina" AND user_id="{user_id}"'
    delete_api.delete(start, stop, predicate, bucket="lumina", org="mds")
    client.close()