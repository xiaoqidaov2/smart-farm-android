@echo off
REM 智慧农场 Android App - 统一部署脚本

echo 🌱 智慧农场 Android App 部署工具
echo =====================================

REM 检查 Git 仓库
if not exist ".git" (
    echo ❌ 当前目录不是 Git 仓库
    echo 请先初始化 Git 仓库
    pause
    exit /b 1
)

echo 请选择部署平台：
echo 1. GitHub (使用 GitHub Actions)
echo 2. GitLab (使用 GitLab CI/CD)
echo 3. 两个平台都部署
echo 4. 创建发布版本 (GitHub Release)
echo 5. 退出

set /p choice="请输入选择 (1-5): "

if "%choice%"=="1" goto deploy_github
if "%choice%"=="2" goto deploy_gitlab
if "%choice%"=="3" goto deploy_both
if "%choice%"=="4" goto create_release
if "%choice%"=="5" goto end
echo ❌ 无效选择
pause
exit /b 1

:deploy_github
echo 🚀 部署到 GitHub...
call deploy_to_github.bat
goto end

:deploy_gitlab
echo 🚀 部署到 GitLab...
call deploy_to_gitlab.bat
goto end

:deploy_both
echo 🚀 部署到 GitHub 和 GitLab...
echo.
echo 📝 添加所有文件到 Git...
git add .

echo 💬 提交更改...
set /p commit_message="请输入提交信息: "
if "%commit_message%"=="" set commit_message=Update Android app with CI/CD

git commit -m "%commit_message%"

echo 🌐 推送到 GitHub...
git push origin main

echo 🌐 推送到 GitLab...
git push gitlab main

echo ✅ 代码已推送到两个平台！
goto end

:create_release
echo 🏷️ 创建发布版本...
call create_release.bat
goto end

:end
echo 📋 部署完成！
pause