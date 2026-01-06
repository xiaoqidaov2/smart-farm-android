@echo off
REM GitHub 部署脚本 - 智慧农场 Android App

echo 🚀 准备提交到 GitHub 并触发 Actions 构建...

REM 检查是否在 Git 仓库中
if not exist ".git" (
    echo ❌ 当前目录不是 Git 仓库
    echo 请先初始化 Git 仓库：
    echo git init
    echo git remote add origin https://github.com/your-username/your-project.git
    pause
    exit /b 1
)

echo 📝 添加所有文件到 Git...
git add .

echo 💬 提交更改...
set /p commit_message="请输入提交信息 (默认: Update Android app with GitHub Actions): "
if "%commit_message%"=="" set commit_message=Update Android app with GitHub Actions

git commit -m "%commit_message%"

echo 🌐 推送到 GitHub...
git push origin main

echo ✅ 代码已推送到 GitHub！
echo 🔄 GitHub Actions 将自动开始构建 Android APK
echo 📱 构建完成后，你可以在以下位置找到 APK：
echo    1. GitHub 项目页面 Actions 最新构建 Artifacts
echo    2. GitHub Pages: https://your-username.github.io/your-project
echo    3. GitHub Releases (如果创建了标签)

echo.
echo 🔍 查看构建状态：
echo https://github.com/your-username/your-project/actions

echo.
echo 📋 下一步操作：
echo 1. 在 GitHub 项目设置中启用 Pages (Settings Pages)
echo 2. 创建标签发布版本: git tag v1.0.0 然后 git push origin v1.0.0
echo 3. 查看构建日志排查问题

p