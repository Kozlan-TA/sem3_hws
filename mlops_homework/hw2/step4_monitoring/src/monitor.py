import requests
import time
import os

def monitor_health(api_url):
    start = time.time()
    try:
        response = requests.get(f'{api_url}/health')
        latency = time.time() - start
        status = response.status_code

        data = response.text
        return {
            "endpoint": "/health",
            "status_code": status,
            "latency": latency,
            "response": data,
            "error": None
        }
    except Exception as e:
        print(f'Ошибка запроса: {e}')


def get_mime_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    elif ext == ".png":
        return "image/png"
    return "application/octet-stream"

def monitor_predict(api_url, img_path):
    start = time.time()
    try:
        with open(img_path, 'rb') as f:
            files = {'file': (img_path, f, 'image/jpeg')}
            response = requests.post(f'{api_url}/predict', files=files)
        latency = time.time() - start
        status = response.status_code
        data = response.json()['result']['prediction']
        return {
            "endpoint": "/predict",
            "status_code": status,
            "latency": latency,
            "response": data,
            "error": None
        }
    except Exception as e:
        latency = time.time() - start
        return {
            "endpoint": "/predict",
            "status_code": None,
            "latency": latency,
            "response": None,
            "error": str(e)
        }

def get_alert_level(value, warning, critical):
    if value is None:
        return "grey"
    elif value >= critical:
        return "red"
    elif value >= warning:
        return "yellow"
    else:
        return "green"
