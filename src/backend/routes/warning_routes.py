from flask import Blueprint, request, jsonify
from influxdb_client import InfluxDBClient
from src.backend.utils.warnings import check_lux_warning, get_thresholds, set_thresholds

warning_bp = Blueprint('warning', __name__)

@warning_bp.route('/check_warning', methods=['GET'])
def check_warning():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    low, high = get_thresholds(user_id)

    client = InfluxDBClient(url="http://influxdb:8086", token="mds-token", org="mds")
    query_api = client.query_api()
    query = f'''
    from(bucket: "lumina")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "lumina")
      |> filter(fn: (r) => r._field == "lux")
      |> filter(fn: (r) => r.user_id == "{user_id}")
      |> last()
    '''
    tables = query_api.query(query, org="mds")
    lux = None
    for table in tables:
        for record in table.records:
            lux = record.get_value()
    client.close()

    if lux is None:
        return jsonify({'warning': 'No lux data available.'})

    warning_msg = check_lux_warning(lux, low, high)
    return jsonify({'warning': warning_msg, 'lux': lux, 'low': low, 'high': high})

@warning_bp.route('/set_threshold', methods=['POST'])
def set_threshold():
    data = request.get_json()
    user_id = data.get('user_id')
    low = data.get('low_threshold')
    high = data.get('high_threshold')
    if not user_id or low is None or high is None:
        return jsonify({'error': 'Missing parameters'}), 400
    success = set_thresholds(user_id, low, high)
    if success:
        return jsonify({'message': 'Thresholds updated!'})
    else:
        return jsonify({'error': 'User not found'}), 404

@warning_bp.route('/api/thresholds', methods=['GET'])
def api_thresholds():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    low, high = get_thresholds(user_id)
    try:
        low_val = float(low) if low not in (None, "", "None") else None
    except ValueError:
        low_val = None
    try:
        high_val = float(high) if high not in (None, "", "None") else None
    except ValueError:
        high_val = None
    return jsonify({'low_threshold': low_val, 'high_threshold': high_val})