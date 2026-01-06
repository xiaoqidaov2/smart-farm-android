# GitHub Actions CI/CD Android 构建指南

本项目已配置 GitHub Actions 自动构建 Android APK。

## 🚀 自动构建流程

### 触发条件
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request 到 `main` 分支
- 创建 GitHub Release

### 构建阶段

1. **Build Job**: 构建 Android APK
   - 设置 Python 3.9 环境
   - 安装 JDK 11
   - 缓存依赖和 Android SDK
   - 使用 Buildozer 构建 APK
   - 上传构建产物

2. **Deploy Pages Job**: 部署到 GitHub Pages
   - 创建 APK 下载页面
   - 自动部署到 GitHub Pages

## 📱 获取构建的 APK

### 方法 1: 从 GitHub Actions Artifacts 下载
1. 进入项目的 **Actions** 标签页
2. 点击最新的成功构建
3. 在 **Artifacts** 部分下载 `android-apk`
4. 解压后获得 APK 文件

### 方法 2: 从 GitHub Pages 下载
1. 访问项目的 Pages URL: `https://your-username.github.io/your-project-name`
2. 点击下载链接

### 方法 3: 从 GitHub Releases 下载
1. 创建 Git 标签时会自动创建 Release
2. 在项目的 **Releases** 页面下载 APK

## 🔧 GitHub Pages 设置

### 启用 GitHub Pages
1. 进入项目 **Settings** > **Pages**
2. Source 选择 **GitHub Actions**
3. 保存设置

### 自定义域名（可选）
1. 在 **Settings** > **Pages** 中设置自定义域名
2. 添加 CNAME 文件到项目根目录

## ⚙️ 环境变量和密钥

### 自动设置的变量
- `GITHUB_TOKEN`: 自动提供，用于上传到 Releases
- `ANDROID_SDK_ROOT`: Android SDK 路径
- `ANDROID_HOME`: Android Home 路径
- `ANDROID_NDK_ROOT`: Android NDK 路径

### 可选的自定义变量
在 **Settings** > **Secrets and variables** > **Actions** 中添加：

```
# 代码签名（生产环境）
KEYSTORE_FILE: base64 编码的密钥库文件
KEYSTORE_PASSWORD: 密钥库密码
KEY_ALIAS: 密钥别名
KEY_PASSWORD: 密钥密码

# 通知设置
SLACK_WEBHOOK: Slack 通知 Webhook
DISCORD_WEBHOOK: Discord 通知 Webhook
```

## 🔄 工作流程详解

### 构建步骤
1. **Checkout**: 检出代码
2. **Setup Python**: 安装 Python 3.9
3. **Setup JDK**: 安装 Java 11
4. **Cache**: 缓存 pip 依赖和 Android SDK
5. **Install Dependencies**: 安装系统和 Python 依赖
6. **Install Android SDK**: 下载并配置 Android SDK
7. **Build APK**: 使用 Buildozer 构建
8. **Upload Artifacts**: 上传构建产物
9. **Release**: 如果是标签，自动创建 Release

### 缓存策略
- **pip 缓存**: 基于 requirements.txt 哈希
- **Android SDK 缓存**: 基于 buildozer.spec 哈希
- **Buildozer 缓存**: 加速后续构建

## 🐛 常见问题

### 构建失败
1. **依赖问题**: 检查 `requirements.txt` 和 `buildozer.spec`
2. **SDK 下载失败**: 网络问题，重新运行构建
3. **内存不足**: GitHub Actions 提供 7GB 内存，通常足够

### Pages 部署失败
1. **权限问题**: 确保在 Settings > Actions > General 中启用了 Pages 权限
2. **分支保护**: 确保 main 分支允许 Actions 写入

### APK 安装问题
1. **架构不兼容**: 支持 arm64-v8a 和 armeabi-v7a
2. **权限问题**: 允许安装未知来源应用

## 📊 监控和通知

### 查看构建状态
1. 项目主页会显示构建状态徽章
2. **Actions** 标签页查看详细日志
3. 邮件通知构建结果

### 添加状态徽章
在 README.md 中添加：
```markdown
![Build Status](https://github.com/your-username/your-repo/workflows/Build%20Android%20APK/badge.svg)
```

## 🎯 高级配置

### 多环境构建
```yaml
strategy:
  matrix:
    build-type: [debug, release]
    arch: [arm64-v8a, armeabi-v7a]
```

### 条件构建
```yaml
# 仅在特定文件变更时构建
paths:
  - '**.py'
  - 'requirements.txt'
  - 'buildozer.spec'
```

### 并行构建
```yaml
jobs:
  build-debug:
    # 构建调试版本
  build-release:
    # 构建发布版本
```

## 🔐 安全最佳实践

### 代码签名
1. 生成发布密钥库
2. 将密钥库转换为 base64
3. 添加到 GitHub Secrets
4. 修改工作流使用签名

### 依赖安全
1. 使用 Dependabot 自动更新依赖
2. 定期审查依赖漏洞
3. 固定依赖版本

## 📈 性能优化

### 构建时间优化
1. **缓存策略**: 有效缓存减少重复下载
2. **并行构建**: 多个 job 并行执行
3. **增量构建**: 仅构建变更部分

### 资源使用
- **CPU**: 2 核心
- **内存**: 7GB RAM
- **存储**: 14GB SSD
- **网络**: 高速网络连接

## 🔄 版本管理

### 自动版本号
```yaml
- name: Generate version
  run: |
    VERSION=$(date +%Y%m%d%H%M)
    echo "VERSION=$VERSION" >> $GITHUB_ENV
```

### 语义化版本
```yaml
- name: Semantic versioning
  uses: paulhatch/semantic-version@v4
  with:
    tag_prefix: "v"
    major_pattern: "BREAKING CHANGE:"
    minor_pattern: "feat:"
```

## 🚀 部署策略

### 多平台发布
1. **GitHub Releases**: 自动发布
2. **Google Play**: 使用 fastlane
3. **内部分发**: 企业应用商店

### 渐进式部署
1. **Alpha**: 内部测试
2. **Beta**: 公开测试
3. **Production**: 正式发布