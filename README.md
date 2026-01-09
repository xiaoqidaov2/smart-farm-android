# 智绘农芯 - BeeWare Toga版本

基于BeeWare Toga框架的智能农业监控系统，提供原生Android界面体验。

## 功能特性

- 📱 原生Android界面
- 🌡️ 实时环境监测（温度、湿度、光照等）
- 🎛️ 设备控制（风扇、报警灯等）
- 📊 数据可视化
- 🔄 自动刷新
- 🔐 安全登录

## 技术栈

- **UI框架**: BeeWare Toga
- **API通信**: requests
- **数据格式**: JSON
- **平台支持**: Android, iOS, Windows, macOS, Linux

## 项目结构

```
├── src/
│   └── smartfarm/
│       ├── app.py          # 主应用
│       ├── __init__.py
│       └── resources/      # 资源文件
├── pyproject.toml         # BeeWare配置
└── README.md
```

## 开发环境设置

### 1. 安装依赖

```bash
pip install briefcase toga requests python-dateutil
```

### 2. 开发模式运行

```bash
cd src/smartfarm
python -m app
```

### 3. 创建应用包

```bash
briefcase create
briefcase build
briefcase run
```

## Android打包

### 1. 创建Android项目

```bash
briefcase create android
```

### 2. 构建APK

```bash
briefcase build android
```

### 3. 运行测试

```bash
briefcase run android
```

### 4. 发布APK

```bash
briefcase publish android
```

## 配置说明

### 传感器映射

在 `app.py` 中配置传感器类型和图标：

```python
SENSORS_MAP = {
    "temperature": {"name": "温度传感器", "unit": "℃", "icon": "🌡️"},
    "humidity": {"name": "湿度传感器", "unit": "%RH", "icon": "💧"},
    # ... 更多传感器
}
```

### 设备控制

```python
ACTUATORS_MAP = {
    "fun": {"name": "风扇", "icon": "🌀"},
    "bacjingd1": {"name": "报警灯", "icon": "🚨"},
}
```

## API集成

使用 `nle_api.py` 与农业设备API通信：

- 登录认证
- 传感器数据获取
- 设备控制命令

## 界面特性

- **登录界面**: 账号、密码、设备ID、服务器地址
- **监控界面**: 传感器卡片显示、设备控制开关
- **原生体验**: Android Material Design风格
- **响应式布局**: 适配不同屏幕尺寸

## 优势对比

| 特性 | KivyMD | BeeWare Toga |
|------|--------|--------------|
| 界面风格 | Material Design | 原生系统 |
| 性能 | 中等 | 优秀 |
| 打包大小 | 较大 | 较小 |
| 学习成本 | 中等 | 较低 |
| 平台支持 | 多平台 | 多平台 |

## 注意事项

1. **权限配置**: Android需要网络权限
2. **字体支持**: 已内置中文字体支持
3. **自动刷新**: 每5秒自动更新数据
4. **错误处理**: 完善的异常处理机制

## 后续优化

- [ ] 数据图表展示
- [ ] 历史数据查询
- [ ] 推送通知
- [ ] 离线模式
- [ ] 多语言支持