from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

SMARTTHINGS_API_URL = "https://api.smartthings.com/v1/devices"  # SmartThings API URL
access_token = 'a92a48b4-62a6-4ce8-b695-bb378f306892'  # 발급받은 Access Token

# 디바이스 ID 목록을 가져오는 함수
def get_device_ids():
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.smartthings+json;v=20170916',
    }

    response = requests.get(SMARTTHINGS_API_URL, headers=headers)

    if response.status_code == 200:
        devices = response.json().get('items', [])
        return devices, response.status_code
    else:
        return None, response.status_code

# 위치 정보를 얻는 함수
def get_device_location(device_id):
    url = f"{SMARTTHINGS_API_URL}/{device_id}/status"
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # 위치 정보를 포함한 데이터를 가져옴
        status_data = response.json()
        latitude = status_data['components']['main']['location']['latitude']
        longitude = status_data['components']['main']['location']['longitude']
        return latitude, longitude
    else:
        return None, None

# 모든 등록된 장치 목록을 가져오는 엔드포인트
@app.route('/', methods=['GET'])
def devices():
    devices, status_code = get_device_ids()
    if devices is not None:
        return render_template('home.html', devices=devices), 200
    else:
        return jsonify({'message': '디바이스 목록 가져오기 실패'}), status_code

@app.route('/device_location/<device_id>')
def device_location(device_id):
    # latitude, longitude = get_device_location(device_id)
    latitude = 37.5665  # 임시 값
    longitude = 126.9780  # 임시 값
    if latitude and longitude:
        return render_template('map.html', latitude=latitude, longitude=longitude)
    else:
        return jsonify({'message': '디바이스 위치 정보를 가져올 수 없습니다.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
