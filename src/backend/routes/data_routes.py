from flask import Blueprint, jsonify, request
from influxdb_client import InfluxDBClient
from datetime import datetime

data_bp = Blueprint('data', __name__)

@data_bp.route('/lux/average', methods=['GET'])
def get_average_lux():
    user_id = request.args.get('user_id', type=int)
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not user_id or not start_time or not end_time:
        return jsonify({'error': 'Missing parameters'}), 400

    client = InfluxDBClient(url="http://influxdb:8086", token="mds-token", org="mds")
    query_api = client.query_api()
    query = f'''
    from(bucket: "lumina")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "lumina")
      |> filter(fn: (r) => r._field == "lux")
      |> filter(fn: (r) => r.user_id == "{user_id}")
      |> mean()
    '''
    tables = query_api.query(query, org="mds")
    avg = None
    for table in tables:
        for record in table.records:
            avg = record.get_value()
    client.close()
    return jsonify({'average_lux': avg})