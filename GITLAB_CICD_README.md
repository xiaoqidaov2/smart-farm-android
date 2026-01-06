# GitLab CI/CD Android 构建指南

本项目已配置 GitLab CI/CD 自动构建 Android APK。

## 🚀 自动构建流程

### 触发条件
- 推送到 `main` 分支
- 推送到 `develop` 分支  
- 创建 Git 标签

### 构建阶段

1. **Build Stage**: 构建 Android APK
   - 安装 Android SDK 和 NDK
   - 安装 Python 依赖
   - 使用 Buildozer 构建 APK

2. **Deploy Stage**: 部署到 GitLab Pages
   - 将 APK 文件发布到 GitLab Pages
   - 提供下载链接

## 📱 获取构建的 APK

### 方法 1: 从 CI/CD Artifacts 下载
1. 进入项目的 **CI/CD > Pipelines**
2. 点击最新的成功构建
3. 在右侧点击 **Download artifacts**
4. APK 文件位于 `bin/` 目录下

### 方法 2: 从 GitLab Pages 下载
1. 访问项目的 Pages URL: `https://your-username.gitlab.io/your-project-name`
2. 点击下载链接

## 🔧 本地构建测试

### 使用 Docker 构建
```bash
# 构建 Docker 镜像
docker build -t smartfarm-builder .

# 运行构建
docker run -v $(pwd):/app smartfarm-builder
```

### 直接使用 Buildozer
```bash
# 安装依赖
pip install buildozer

# 初始化配置（如果需要）
buildozer init

# 构建 APK
buildozer android debug
```

## ⚙️ 配置说明

### buildozer.spec 主要配置
- **应用名称**: 智慧农场
- **包名**: com.smartfarm.app
- **版本**: 1.0
- **目标 Android API**: 33
- **最低 Android API**: 21
- **架构**: arm64-v8a, armeabi-v7a

### 权限配置
- `INTERNET`: 网络访问
- `ACCESS_NETWORK_STATE`: 网络状态检查
- `WRITE_EXTERNAL_STORAGE`: 外部存储写入
- `READ_EXTERNAL_STORAGE`: 外部存储读取

## 🐛 常见问题

### 构建失败
1. **依赖问题**: 检查 `requirements.txt` 中的依赖版本
2. **SDK 版本**: 确保 Android SDK 版本兼容
3. **内存不足**: GitLab Runner 可能需要更多内存

### APK 安装问题
1. **未知来源**: 在 Android 设置中允许安装未知来源应用
2. **架构不兼容**: 确保设备架构支持（arm64-v8a 或 armeabi-v7a）

## 📝 自定义构建

### 修改应用信息
编辑 `buildozer.spec` 文件：
```ini
[app]
title = 你的应用名称
package.name = yourappname
package.domain = com.yourcompany.yourapp
version = 1.1
```

### 添加图标和启动画面
```ini
[app]
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
```

### 修改权限
```ini
[app]
android.permissions = INTERNET,CAMERA,RECORD_AUDIO
```

## 🔄 版本发布

### 创建发布版本
1. 更新 `buildozer.spec` 中的版本号
2. 创建 Git 标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. GitLab CI/CD 将自动构建发布版本

### 签名 APK（生产环境）
1. 生成密钥库文件
2. 在 GitLab CI/CD 变量中添加签名信息
3. 修改 `.gitlab-ci.yml` 使用 `buildozer android release`

## 📊 监控构建

### 查看构建日志
1. 进入 **CI/CD > Pipelines**
2. 点击构建任务查看详细日志
3. 检查错误信息和警告

### 构建缓存
- Android SDK 和构建缓存会被保存
- 后续构建会更快完成

## 🎯 下一步优化

1. **代码签名**: 配置发布版本的代码签名
2. **自动测试**: 添加单元测试和集成测试
3. **多环境**: 配置开发、测试、生产环境
4. **通知**: 配置构建成功/失败通知
5. **版本管理**: 自动化版本号管理