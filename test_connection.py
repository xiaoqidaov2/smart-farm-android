import requests
import json
import getpass

# 颜色代码，用于美化输出
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def test_nle_connection():
    print(f"{GREEN}=== NLECloud 对接测试工具 ==={RESET}")
    print("本工具用于测试您的账号和设备ID是否配置正确，以及网络连接是否通畅。\n")

    base_url = "http://api.nlecloud.com"
    
    # 1. 输入账号信息
    username = input("请输入 NLECloud 账号 (手机号/用户名): ").strip()
    if not username:
        print(f"{RED}错误: 账号不能为空{RESET}")
        return

    password = input("请输入密码: ").strip()
    if not password:
        print(f"{RED}错误: 密码不能为空{RESET}")
        return
        
    device_id = input("请输入设备ID (例如 372699): ").strip()
    
    # 2. 测试登录
    print(f"\n{GREEN}[1/3] 正在尝试登录...{RESET}")
    login_url = f"{base_url}/Users/Login"
    login_data = {"Account": username, "Password": password}
    
    token = None
    try:
        resp = requests.post(login_url, json=login_data, timeout=10)
        if resp.status_code == 200:
            res_json = resp.json()
            if res_json.get("Status") == 0:
                token = res_json["ResultObj"]["AccessToken"]
                print(f"{GREEN}✔ 登录成功! Token获取正常。{RESET}")
            else:
                print(f"{RED}✘ 登录失败: {res_json.get('Msg')}{RESET}")
                return
        else:
            print(f"{RED}✘ HTTP请求失败: 状态码 {resp.status_code}{RESET}")
            return
    except Exception as e:
        print(f"{RED}✘ 连接异常: {e}{RESET}")
        return

    # 3. 测试获取设备数据
    if not device_id:
        print(f"\n{GREEN}[2/3] 未提供设备ID，跳过传感器数据测试。{RESET}")
    else:
        print(f"\n{GREEN}[2/3] 正在获取设备 [{device_id}] 的传感器数据...{RESET}")
        sensors_url = f"{base_url}/Devices/{device_id}/Sensors"
        headers = {"Authorization": token}
        
        try:
            resp = requests.get(sensors_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                res_json = resp.json()
                if res_json.get("Status") == 0:
                    data = res_json["ResultObj"]
                    print(f"{GREEN}✔ 获取数据成功! 共找到 {len(data)} 个传感器数据点:{RESET}")
                    for point in data:
                        print(f"   - 标识名: {point.get('ApiTag'):<15} 值: {point.get('Value')}")
                else:
                    print(f"{RED}✘ 获取数据失败: {res_json.get('Msg')}{RESET}")
            else:
                print(f"{RED}✘ HTTP请求失败: 状态码 {resp.status_code}{RESET}")
        except Exception as e:
            print(f"{RED}✘ 连接异常: {e}{RESET}")

    print(f"\n{GREEN}=== 测试结束 ==={RESET}")
    print("如果以上步骤都成功，说明您的 nle_api.py 和 main.py 可以正常工作。")
    print("如果获取数据为空，请检查 NLECloud 平台上是否已为该设备添加了传感器。")

if __name__ == "__main__":
    try:
        test_nle_connection()
    except KeyboardInterrupt:
        print("\n已取消测试。")
