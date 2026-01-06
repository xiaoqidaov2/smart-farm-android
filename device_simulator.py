import requests
import time
import random
import sys

# Configuration

# 真实 NLECloud 地址
SERVER_URL = "http://api.nlecloud.com"
# 设备ID (从截图看是 372699)
DEVICE_ID = 1385119

# 请在此处填入您的 NLECloud 账号和密码
USERNAME = "" 
PASSWORD = ""

# 用户提供的 API Key (用于记录，通常只需在平台申请即可，无需在代码中显式调用，除非作为 header)
# 如果 Login 接口仍然返回错误，尝试将此 Key 放入 header
API_KEY = "02CCC87A9D1E4E6E90005D9423EAFADE"

# Global Token
access_token = None

def login():
    global access_token
    print(f"正在登录 NLECloud ({SERVER_URL})...")
    
    # 从命令行参数获取账号密码
    u = USERNAME
    p = PASSWORD
    
    if not u or not p:
        if len(sys.argv) >= 3:
            u = sys.argv[1]
            p = sys.argv[2]
        else:
            print("错误: 未配置账号密码。")
            print("请编辑 device_simulator.py 填入 USERNAME 和 PASSWORD，")
            print("或者通过命令行运行: python device_simulator.py <username> <password>")
            return False

    url = f"{SERVER_URL}/Users/Login"
    data = {
        "Account": u,
        "Password": p
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("Status") == 0:
                token_candidate = res_json["ResultObj"]["AccessToken"]
                
                # 检查 Token 是否包含非法字符
                # NLECloud 的 Token 可能很长，之前的 200 长度限制太短了，这里放宽限制
                # 主要是检查是否包含 APIKEY 这种错误提示关键字
                if not token_candidate or "APIKEY" in token_candidate:
                    print(f"登录返回了异常的 Token: {token_candidate[:50]}...")
                    print("请确保您已在 NLECloud 个人中心申请了 API Key。")
                    return False
                    
                access_token = token_candidate
                print(f"登录成功! Token: {access_token[:10]}...")
                return True
            else:
                print(f"登录失败: {res_json.get('Msg')}")
        else:
            print(f"HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"登录异常: {e}")
        
    return False
    
    
    # Clean up redundant code
    pass

# Data Generation Logic
def get_random_value(tag):
    if tag == "guangzhao_sum":
        return float(random.randint(0, 2000))
    elif tag == "temperature":
        return round(random.uniform(20.0, 35.0), 1)
    elif tag == "humidity":
        return round(random.uniform(40.0, 80.0), 1)
    elif tag == "CO2":
        return float(random.randint(400, 1000))
    elif tag == "Soil_temperture":
        return round(random.uniform(15.0, 25.0), 1)
    elif tag == "Soil_moisture":
        return round(random.uniform(30.0, 60.0), 1)
    elif tag == "Soil_sanility":
        return float(random.randint(100, 500))
    elif tag == "Nhanl":
        return float(random.randint(10, 100))
    elif tag == "Phanl":
        return float(random.randint(10, 100))
    elif tag == "jia":
        return float(random.randint(10, 100))
    elif tag == "PH":
        return round(random.uniform(6.0, 8.0), 1)
    elif tag == "zigbee_fun":
        return round(random.uniform(0, 1000), 1)
    elif tag == "fun":
        return random.choice([0, 1])
    elif tag == "LVD":
        return random.choice([0, 1])
    else:
        return 0

def add_sensors_to_platform():
    """尝试调用API自动添加传感器"""
    if not access_token:
        print("未登录，无法添加传感器")
        return

    print("正在尝试自动添加传感器到平台...")
    url = f"{SERVER_URL}/Devices/{DEVICE_ID}/Sensors"
    # NLECloud 有时使用 AccessToken Header，有时使用 Authorization
    headers = {
        "Authorization": access_token,
        "AccessToken": access_token
    }

    # 如果有 API Key，尝试加入 Header (不确定字段名，尝试常见的)
    if API_KEY:
        headers["ApiKey"] = API_KEY
        headers["ProjectKey"] = API_KEY
    
    # 定义传感器/执行器列表 (根据截图和main.py)
    # TransType: 0=只上报?, 1=上报下发?  (需尝试, 通常 1=Sensor, 0=Actuator? 或反之)
    # 根据经验: 1=只上报(Sensor), 0=上报下发(Control)
    # DataType: 1=数值(Int/Float), 2=布尔(Bool), 4=字符串(String)? (需尝试)
    
    sensors_config = [
        # 传感器 (只上报)
        # DataType: 1=Int?, 2=Double?, 4=String?
        # NLECloud 常见定义: DataType: 1(Int), 2(Double), 3(Bool), 4(String), 5(Enum)
        # TransType: 0(只读/上报), 1(读写/控制) ? 
        # 错误 "参数值不在指定范围内" 可能是 DataType 或 TransType 不对
        
        # 尝试修正: TransType: 0 (Sensor, ReadOnly), DataType: 2 (Float/Double)
        {"ApiTag": "guangzhao_sum", "Name": "光照传感器", "Unit": "Lux", "TransType": 0, "DataType": 2},
        {"ApiTag": "temperature", "Name": "温度传感器", "Unit": "℃", "TransType": 0, "DataType": 2},
        {"ApiTag": "humidity", "Name": "湿度传感器", "Unit": "%RH", "TransType": 0, "DataType": 2},
        {"ApiTag": "CO2", "Name": "CO2浓度", "Unit": "ppm", "TransType": 0, "DataType": 2},
        {"ApiTag": "Soil_temperture", "Name": "土壤温度", "Unit": "℃", "TransType": 0, "DataType": 2},
        {"ApiTag": "Soil_moisture", "Name": "土壤湿度", "Unit": "%", "TransType": 0, "DataType": 2},
        {"ApiTag": "Soil_sanility", "Name": "土壤盐度", "Unit": "mg/L", "TransType": 0, "DataType": 2},
        {"ApiTag": "Nhanl", "Name": "氮含量", "Unit": "mg/kg", "TransType": 0, "DataType": 2},
        {"ApiTag": "Phanl", "Name": "磷含量", "Unit": "mg/kg", "TransType": 0, "DataType": 2},
        {"ApiTag": "jia", "Name": "钾含量", "Unit": "mg/kg", "TransType": 0, "DataType": 2},
        {"ApiTag": "PH", "Name": "土壤PH", "Unit": "", "TransType": 0, "DataType": 2},
        {"ApiTag": "zigbee_fun", "Name": "光照", "Unit": "Lux", "TransType": 0, "DataType": 2},
        
        # # 执行器 (上报和下发)
        # # 尝试: TransType: 0 (Sensor), DataType: 1 (Int) - 降级为传感器以确保能添加成功
        # # 之前的 TransType: 1 均失败，可能是因为缺少 Range 参数或其他约束
        # {"ApiTag": "fun", "Name": "风扇", "Unit": "", "TransType": 1, "DataType": 1}, 
        # {"ApiTag": "LVD", "Name": "爆灯", "Unit": "", "TransType": 1, "DataType": 1},
        # {"ApiTag": "LCD_Show", "Name": "LED显示", "Unit": "", "TransType": 1, "DataType": 4}, 
    ]

    global valid_sensors
    valid_sensors = set()

    for s in sensors_config:
        try:
            # 检查传感器是否存在 (通过获取单个传感器API，或者直接添加看是否报错)
            # 这里直接尝试添加，如果已存在通常会返回错误或忽略
            # 注意: 添加传感器的API可能和上传数据的API路径相同但Method不同，或者Payload不同
            # 尝试使用 POST /Devices/{id}/Sensors 添加
            
            payload = {
                "ApiTag": s["ApiTag"],
                "Name": s["Name"],
                "Unit": s["Unit"],
                "TransType": s["TransType"],
                "DataType": s["DataType"]
            }
            
            # 有些版本API是 POST /Sensors，Body带DeviceId
            # 也有可能是 POST /Devices/{id}/Sensors
            res = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if res.status_code == 200:
                rj = res.json()
                if rj.get("Status") == 0:
                    print(f"成功添加/更新传感器: {s['Name']} ({s['ApiTag']})")
                    valid_sensors.add(s["ApiTag"])
                else:
                    msg = rj.get('Msg')
                    if "已被使用" in msg or "has been used" in msg:
                         print(f"传感器已存在: {s['Name']} ({s['ApiTag']})")
                         valid_sensors.add(s["ApiTag"])
                    else:
                        print(f"添加 {s['ApiTag']} 返回: {msg}")
            else:
                print(f"添加 {s['ApiTag']} HTTP错误: {res.status_code}")
                
        except Exception as e:
            print(f"添加 {s['ApiTag']} 异常: {e}")
            
    print(f"传感器初始化流程结束。有效传感器: {len(valid_sensors)} 个\n")

def upload_sensor_data(data_list):
    """
    批量上传传感器数据
    POST /Devices/{deviceId}/Datas
    Body: {"Datas": [...]}
    """
    if not access_token:
        print("未登录，无法上传数据")
        return

    # 过滤掉无效的传感器
    if 'valid_sensors' in globals() and valid_sensors:
        data_list = [d for d in data_list if d['ApiTag'] in valid_sensors]
    if not data_list:
        print("没有有效的传感器数据可上传")
        return
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    datas_dto = []
    for item in data_list:
        datas_dto.append({
            "ApiTag": item["ApiTag"],
            "PointDTO": [
                {
                    "Value": item["Value"],
                    "RecordTime": current_time
                }
            ]
        })
    url = f"{SERVER_URL}/Devices/{DEVICE_ID}/Datas"
    headers = {
        "AccessToken": access_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"DatasDTO": datas_dto}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            res = response.json()
            if res.get("Status") == 0:
                print(f"[{time.strftime('%H:%M:%S')}] 上传成功: {len(data_list)} 条数据")
                return
            else:
                print(f"上传失败 API: {res.get('Msg')}")
        else:
            print(f"上传失败 HTTP: {response.status_code}")
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            res = response.json()
            if res.get("Status") == 0:
                print(f"[{time.strftime('%H:%M:%S')}] 上传成功: {len(data_list)} 条数据")
                return
            else:
                print(f"上传失败 API: {res.get('Msg')}")
        else:
            print(f"上传失败 HTTP: {response.status_code}")
    except Exception as e:
        print(f"上传异常: {e}")

def upload_data():
    if not access_token:
        print("未获取到 Token，跳过上传")
        return

    sensor_tags = [
        "guangzhao_sum", "temperature", "humidity", "CO2",
        "Soil_temperture", "Soil_moisture", "Soil_sanility",
        "Nhanl", "Phanl", "jia", "PH", "zigbee_fun",
        "fun", "LVD", "LCD_Show"
    ]
    
    data = []
    for tag in sensor_tags:
        data.append({
            "ApiTag": tag,
            "Value": get_random_value(tag)
        })
        
    upload_sensor_data(data)

if __name__ == "__main__":
    print(f"启动 NLECloud 真实设备数据模拟器 (DeviceID: {DEVICE_ID})...")
    print("按 Ctrl+C 停止")
    
    if login():
        # 询问是否自动添加传感器
        print("是否尝试自动添加传感器到平台？(y/n)")
        # 为了方便用户直接运行，这里默认尝试添加，或者等待用户输入
        # 由于在IDE终端运行，可能无法交互，直接执行
        add_sensors_to_platform()
        
        while True:
            upload_data()
            time.sleep(5) # Real server might have rate limits, slightly slower
    else:
        print("程序退出。")
