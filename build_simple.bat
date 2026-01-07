@echo off
REM 简化的本地构建脚本 - Windows 版本

echo 🌱 智慧农场 Android App - 本地构建工具
echo ==================================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装 Python 3.x
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 运行 Python 构建脚本
echo 🚀 启动构建过程...
python build_simple.py

if errorlevel 1 (
    echo.
    echo ❌ 构建失败！
    echo.
    echo 💡 Windows 用户建议：
    echo 1. 使用 WSL (Windows Subsystem for Linux)
    echo 2. 使用 Docker Desktop
    echo 3. 使用 GitHub Actions (已配置)
    echo.
    echo 🔗 GitHub Actions 构建状态:
    echo https://github.com/xiaoqidaov2/smart-farm-android/actions
) else (
    echo.
    echo 🎉 构建成功完成！
    echo 📱 APK 文件位于 bin\ 目录
    echo.
    echo 📋 安装说明：
    echo 1. 将 APK 文件传输到 Android 设备
    echo 2. 在设置中允许安装未知来源应用
    echo 3. 点击 APK 文件进行安装
)

echo.
pause