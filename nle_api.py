import requests
import json

class NLECloudAPI:
    def __init__(self, base_url="http://api.nlecloud.com", username=None, password=None):
        self.BASE_URL = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None

    def login(self, username, password):
        """登录获取Token"""
        url = f"{self.BASE_URL}/users/login"
        data = {
            "Account": username,
            "Password": password
        }
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("Status") == 0:
                    self.token = res_json["ResultObj"]["AccessToken"]
                    self.username = username
                    self.password = password
                    return True, "登录成功"
                else:
                    return False, res_json.get("Msg", "登录失败")
            else:
                return False, f"HTTP Error: {response.status_code}"
        except Exception as e:
            return False, str(e)

    def get_sensor_data(self, device_id):
        if not self.token:
            return None, "未登录"
        import datetime
        headers = {"AccessToken": self.token, "Accept": "application/json"}
        try:
            end = datetime.datetime.now()
            start = end - datetime.timedelta(minutes=15)
            url1 = f"{self.BASE_URL}/devices/{int(device_id)}/datas/grouping"
            params1 = {
                "GroupBy": 2,
                "Func": "MAX",
                "StartDate": start.strftime("%Y-%m-%d %H:%M:%S"),
                "EndDate": end.strftime("%Y-%m-%d %H:%M:%S")
            }
            response = requests.get(url1, headers=headers, params=params1, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("Status") == 0:
                    result = res_json.get("ResultObj") or {}
                    points = result.get("DataPoints") or []
                    latest = []
                    for p in points:
                        tag = p.get("ApiTag")
                        dto = p.get("PointDTO") or []
                        val = None
                        if dto:
                            val = dto[-1].get("Value")
                        latest.append({"ApiTag": tag, "Value": val})
                    return latest, None
                else:
                    return None, res_json.get("Msg", "获取数据失败")
            else:
                return None, f"HTTP Error: {response.status_code}"
        except Exception as e:
            return None, str(e)

    def control_device(self, device_id, api_tag, value):
        """控制设备"""
        if not self.token:
            return False, "未登录"
        headers = {"AccessToken": self.token}
        url = f"{self.BASE_URL}/cmds?deviceId={int(device_id)}&apiTag={api_tag}"
        try:
            response = requests.post(url, json=value, headers=headers, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("Status") == 0:
                    return True, "命令发送成功"
                else:
                    return False, res_json.get("Msg", "命令发送失败")
            else:
                return False, f"HTTP Error: {response.status_code}"
        except Exception as e:
            return False, str(e)
