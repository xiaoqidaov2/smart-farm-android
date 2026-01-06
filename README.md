# 智慧农场 Android App (Python/KivyMD)

本项目是一个基于 Python 和 KivyMD 的安卓应用，用于连接 NLECloud 平台，实现智慧农场数据的监控与控制。

## 1. 环境搭建

### 依赖安装
请确保安装了 Python 3.x。然后运行以下命令安装所需库：

```bash
pip install -r requirements.txt
```

### 运行应用
在电脑上调试运行：
```bash
python main.py
```

### 打包成 APK (安卓安装包)

#### 方法 1: 使用 CI/CD 自动构建 (推荐)

**GitHub Actions 构建:**
```bash
# 提交代码到 GitHub
git add .
git commit -m "Update app"
git push origin main

# GitHub Actions 将自动构建 APK，可在 Actions > Artifacts 中下载
# 或访问 GitHub Pages: https://your-username.github.io/your-project
```

**GitLab CI/CD 构建:**
```bash
# 提交代码到 GitLab
git add .
git commit -m "Update app"
git push origin main

# GitLab 将自动构建 APK，可在 CI/CD > Pipelines 中下载
```

#### 方法 2: 本地构建
使用 Buildozer 进行打包 (建议在 Linux 或 WSL 环境下进行)：
```bash
pip install buildozer
buildozer init
# 修改 buildozer.spec 配置文件 (添加依赖: kivymd, requests)
buildozer android debug
```

#### 方法 3: 使用 Docker 构建
```bash
# 构建 Docker 镜像
docker build -t smartfarm-builder .

# 运行构建
docker run -v $(pwd):/app smartfarm-builder
```

详细的 CI/CD 配置说明请参考：
- [GitLab CI/CD 说明](GITLAB_CICD_README.md)
- [GitHub Actions 说明](GITHUB_ACTIONS_README.md)

## 2. NLECloud 平台配置说明

为了让 App 正常工作，请在 [NLECloud 官网](http://www.nlecloud.com/) 完成以下配置：

### 第一步：创建项目
1. 登录 NLECloud。
2. 创建一个新项目 (例如：智慧农场)。

### 第二步：添加设备
1. 在项目下添加一个新设备。
2. 记下 **设备ID** (DeviceId)，App 登录时需要用到 (默认代码中为 `372699`)。

### 第三步：添加传感器与执行器
确保设备的传感器标识名 (ApiTag) 与 App 代码 (`main.py`) 中的一致。请按照下表添加：

| 设备名称 | 标识名 (ApiTag) | 类型 | 数据类型 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| 光照传感器 | guangzhao_sum | 传感器 | 整数/浮点 | 只上报 |
| 空气温度 | temperature | 传感器 | 整数/浮点 | 只上报 |
| 空气湿度 | humidity | 传感器 | 整数/浮点 | 只上报 |
| CO2浓度 | CO2 | 传感器 | 整数/浮点 | 只上报 |
| 土壤温度 | Soil_temperture | 传感器 | 整数/浮点 | 只上报 |
| 土壤湿度 | Soil_moisture | 传感器 | 整数/浮点 | 只上报 |
| 土壤盐度 | Soil_sanility | 传感器 | 整数/浮点 | 只上报 |
| 氮含量 | Nhanl | 传感器 | 整数/浮点 | 只上报 |
| 磷含量 | Phanl | 传感器 | 整数/浮点 | 只上报 |
| 钾含量 | jia | 传感器 | 整数/浮点 | 只上报 |
| 土壤PH | PH | 传感器 | 整数/浮点 | 只上报 |
| 光照(Zigbee)| zigbee_fun | 传感器 | 浮点 | 只上报 |
| 风扇 | fun | 执行器 | 布尔/整数 | 上报和下发 (0/1) |
| 康灯 | LVD | 执行器 | 布尔/整数 | 上报和下发 (0/1) |

## 3. 功能说明

- **登录界面**：输入 NLECloud 账号、密码和设备ID进行登录。
- **环境监测**：实时显示各个传感器的数据，每 5 秒自动刷新。
- **设备控制**：点击开关控制风扇和灯的开启/关闭。
- **界面风格**：采用扁平化设计，卡片式布局，清晰直观。
