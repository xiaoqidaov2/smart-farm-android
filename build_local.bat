@echo off
REM 本地构建脚本 - 智慧农场 Android App (Windows)

echo 🚀 开始构建智慧农场 Android App...

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装 Python 3.x
    pause
    exit /b 1
)

REM 检查 pip 是否安装
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip 未安装，请检查 Python 安装
    pause
    exit /b 1
)

echo 📦 安装 Python 依赖...
pip install --upgrade pip
pip install buildozer cython
pip install -r requirements.txt

REM 检查是否已初始化 buildozer
if not exist "buildozer.spec" (
    echo ⚙️ 初始化 Buildozer 配置...
    buildozer init
)

echo 🔨 开始构建 APK...
echo 注意：在 Windows 上构建 Android APK 建议使用 WSL 或 Docker
echo 如果遇到问题，请使用 Docker 构建：
echo docker build -t smartfarm-builder .
echo docker run -v %cd%:/app smartfarm-builder

buildozer android debug

REM 检查构建结果
if exist "bin\*.apk" (
    echo ✅ 构建成功！APK 文件位于 bin\ 目录
    dir bin\*.apk
) else (
    echo ❌ 构建失败，建议使用 Docker 或 WSL 环境构建
)

echo 🎉 构建完成！
pause