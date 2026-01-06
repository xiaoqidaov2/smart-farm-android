#!/bin/bash

# 本地构建脚本 - 智慧农场 Android App

echo "🚀 开始构建智慧农场 Android App..."

# 检查是否安装了必要工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安装，请先安装"
        exit 1
    fi
}

echo "🔍 检查构建环境..."
check_command python3
check_command pip3

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install --upgrade pip
pip3 install buildozer cython
pip3 install -r requirements.txt

# 检查是否已初始化 buildozer
if [ ! -f "buildozer.spec" ]; then
    echo "⚙️ 初始化 Buildozer 配置..."
    buildozer init
fi

# 构建 APK
echo "🔨 开始构建 APK..."
buildozer android debug

# 检查构建结果
if [ -f "bin/*.apk" ]; then
    echo "✅ 构建成功！APK 文件位于 bin/ 目录"
    ls -la bin/*.apk
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi

echo "🎉 构建完成！"