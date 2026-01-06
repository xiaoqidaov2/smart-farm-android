@echo off
REM GitLab 部署脚本 - 智慧农场 Android App

echo 🚀 准备提交到 GitLab 并触发 CI/CD 构建...

REM 检查是否在 Git 仓库中
if not exist ".git" (
    echo ❌ 当前目录不是 Git 仓库
    echo 请先初始化 Git 仓库：
    echo git init
    echo git remote add origin https://gitlab.com/your-username/your-project.git
    pause
    exit /b 1
)

echo 📝 添加所有文件到 Git...
git add .

echo 💬 提交更改...
set /p commit_message="请输入提交信息 (默认: Update Android app with CI/CD): "
if "%commit_message%"=="" set commit_message=Update Android app with CI/CD

git commit -m "%commit_message%"

echo 🌐 推送到 GitLab...
git push origin main

echo ✅ 代码已推送到 GitLab！
echo 🔄 GitLab CI/CD 将自动开始构建 Android APK
echo 📱 构建完成后，你可以在以下位置找到 APK：
echo    1. GitLab 项目页面 > CI/CD > Pipelines > 下载 Artifacts
echo    2. GitLab Pages (如果配置了): https://your-username.gitlab.io/your-project

echo.
echo 🔍 查看构建状态：
echo https://gitlab.com/your-username/your-project/-/pipelines

pause