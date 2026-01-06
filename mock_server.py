from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# 模拟数据库 - 存储执行器状态
# 0: 关, 1: 开
device_state = {
    "fun": 0,        # 风扇
    "LVD": 0,        # 爆灯 (Lamp)
}

# 模拟传感器数据缓存 (用于接收上传的数据)
sensor_cache = {}

# 模拟传感器数据生成 (当没有上传数据时使用)
def get_random_sensor_value(tag):
    if tag == "guangzhao_sum":
        return random.randint(0, 2000)
    elif tag == "temperature":
        return random.randint(20, 35)
    elif tag == "humidity":
        return random.randint(40, 80)
    elif tag == "CO2":
        return random.randint(400, 1000)
    elif tag == "Soil_temperture":
        return random.randint(15, 25)
    elif tag == "Soil_moisture":
        return random.randint(30, 60)
    elif tag == "Soil_sanility":
        return random.randint(100, 500)
    elif tag == "Nhanl":
        return random.randint(10, 100)
    elif tag == "Phanl":
        return random.randint(10, 100)
    elif tag == "jia":
        return random.randint(10, 100)
    elif tag == "PH":
        return random.randint(6, 8)
    elif tag == "zigbee_fun":
        return round(random.uniform(0, 1000), 1)
    else:
        return 0

@app.route('/')
def home():
    return "<h1>NLECloud 本地模拟服务器已启动</h1><p>API 地址: http://127.0.0.1:5000</p>"

# 1. 登录接口
@app.route('/Users/Login', methods=['POST'])
def login():
    data = request.json
    print(f"收到登录请求: {data}")
    # 模拟任意账号登录成功
    return jsonify({
        "Status": 0,
        "Msg": "登录成功",
        "ResultObj": {
            "AccessToken": "mock_token_123456789",
            "UserID": 123
        }
    })

# 2. 获取设备传感器数据
@app.route('/Devices/<device_id>/Sensors', methods=['GET'])
def get_sensors(device_id):
    # 构造返回数据
    # NLECloud 返回格式通常是一个列表
    result_obj = []
    
    # 添加传感器数据
    sensor_tags = [
        "guangzhao_sum", "temperature", "humidity", "CO2",
        "Soil_temperture", "Soil_moisture", "Soil_sanility",
        "Nhanl", "Phanl", "jia", "PH", "zigbee_fun"
    ]
    
    for tag in sensor_tags:
        # 优先使用缓存的上传数据，否则使用模拟生成的随机数据
        val = sensor_cache.get(tag, get_random_sensor_value(tag))
        result_obj.append({
            "ApiTag": tag,
            "Value": val,
            "RecordTime": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    # 添加执行器状态回读
    for tag, val in device_state.items():
        result_obj.append({
            "ApiTag": tag,
            "Value": val,
            "RecordTime": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "Status": 0,
        "Msg": "成功",
        "ResultObj": result_obj
    })

# 3. 模拟设备上传数据 (新增接口)
@app.route('/Devices/<device_id>/Sensors', methods=['POST'])
def upload_sensors(device_id):
    data = request.json
    print(f"收到设备 {device_id} 上传的数据: {data}")
    
    # 支持列表或单个对象
    items = data if isinstance(data, list) else [data]
    
    for item in items:
        tag = item.get('ApiTag')
        val = item.get('Value')
        if tag is not None:
            sensor_cache[tag] = val
            
    return jsonify({
        "Status": 0,
        "Msg": "数据上传成功",
        "ResultObj": None
    })

# 4. 控制设备 (发送命令)
@app.route('/Cmds', methods=['POST'])
def send_cmd():
    data = request.json
    device_id = None
    api_tag = None
    value = None
    if data and isinstance(data, dict):
        device_id = data.get('DeviceId')
        api_tag = data.get('ApiTag')
        value = data.get('Value')
    else:
        device_id = request.args.get('deviceId')
        api_tag = request.args.get('apiTag')
        raw = request.data
        try:
            value = int(raw.decode('utf-8')) if raw else None
        except:
            try:
                value = raw.decode('utf-8')
            except:
                value = None
    
    print(f"收到控制命令: 设备={device_id}, 标识={api_tag}, 值={value}")
    
    if api_tag in device_state:
        # 更新状态
        try:
            if api_tag == "LCD_Show":
                device_state[api_tag] = str(value)
            else:
                device_state[api_tag] = int(value)
                
            return jsonify({
                "Status": 0,
                "Msg": "命令发送成功",
                "ResultObj": None
            })
        except:
            return jsonify({
                "Status": 1,
                "Msg": "值格式错误",
                "ResultObj": None
            })
    else:
        # 即使不是预定义的执行器，也返回成功以便测试
        return jsonify({
            "Status": 0,
            "Msg": "命令已发送(模拟)",
            "ResultObj": None
        })

if __name__ == '__main__':
    # 监听所有IP，方便局域网手机测试
    print("启动本地 NLECloud 模拟服务器...")
    print("请在 App 登录界面点击 '切换服务器' 或手动输入 IP")
    app.run(host='0.0.0.0', port=5000, debug=True)
