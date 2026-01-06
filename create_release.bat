@echo off
REM 创建 GitHub Release 脚本

echo 🏷️ 创建 GitHub Release...

REM 获取当前版本号
set /p version="请输入版本号 (例如: v1.0.0): "
if "%version%"=="" (
    echo ❌ 版本号不能为空
    pause
    exit /b 1
)

REM 检查版本号格式
echo %version% | findstr /r "^v[0-9]\+\.[0-9]\+\.[0-9]\+$" >nul
if errorlevel 1 (
    echo ❌ 版本号格式错误，请使用 vX.Y.Z 格式 (例如: v1.0.0)
    pause
    exit /b 1
)

echo 📝 创建 Git 标签...
git tag %version%

echo 🌐 推送标签到 GitHub...
git push origin %version%

echo ✅ 标签已创建并推送！
echo 🔄 GitHub Actions 将自动构建并创建 Release
echo 📱 构建完成后，Release 将包含：
echo    - Android APK 文件
echo    - 自动生成的更新日志
echo    - 下载和安装说明

echo.
echo 🔍 查看 Release 状态：
echo https://github.com/your-username/your-project/releases

echo.
echo 📋 Release 创建流程：
echo 1. GitHub Actions 开始构建 APK
echo 2. 构建完成后自动创建 Release
echo 3. APK 文件自动上传到 Release
echo 4. 用户可以直接下载安装

pause