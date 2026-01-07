#!/usr/bin/env python3
"""
简化的本地构建脚本 - 智慧农场 Android App
使用 Python 脚本来更好地控制构建过程
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """运行命令并显示输出"""
    print(f"🔧 Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=False, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False

def check_requirements():
    """检查构建要求"""
    print("🔍 Checking build requirements...")
    
    # 检查 Python
    if not shutil.which("python3"):
        print("❌ Python 3 not found")
        return False
    
    # 检查 pip
    if not shutil.which("pip3"):
        print("❌ pip3 not found")
        return False
        
    print("✅ Basic requirements satisfied")
    return True

def install_dependencies():
    """安装 Python 依赖"""
    print("📦 Installing Python dependencies...")
    
    # 升级 pip
    if not run_command("python3 -m pip install --upgrade pip"):
        return False
    
    # 安装 buildozer
    if not run_command("pip3 install buildozer cython"):
        return False
    
    # 安装项目依赖
    if not run_command("pip3 install -r requirements.txt"):
        return False
        
    return True

def prepare_buildozer():
    """准备 buildozer 配置"""
    print("⚙️ Preparing buildozer configuration...")
    
    # 检查 buildozer.spec 是否存在
    if not Path("buildozer.spec").exists():
        print("📝 Initializing buildozer...")
        if not run_command("buildozer init"):
            return False
    
    # 简化配置以提高成功率
    spec_content = Path("buildozer.spec").read_text()
    
    # 修改为单架构构建
    spec_content = spec_content.replace(
        "android.archs = arm64-v8a, armeabi-v7a",
        "android.archs = arm64-v8a"
    )
    
    # 简化依赖
    spec_content = spec_content.replace(
        "requirements = python3,kivy,kivymd,requests,urllib3,certifi,charset-normalizer,idna",
        "requirements = python3,kivy,kivymd,requests"
    )
    
    Path("buildozer.spec").write_text(spec_content)
    print("✅ Buildozer configuration updated")
    return True

def build_apk():
    """构建 APK"""
    print("🔨 Building Android APK...")
    print("⚠️  This may take 15-30 minutes on first build...")
    
    # 设置环境变量
    env = os.environ.copy()
    env["BUILDOZER_WARN_ON_ROOT"] = "0"
    
    # 构建 APK
    cmd = "buildozer android debug"
    print(f"🚀 Executing: {cmd}")
    
    try:
        process = subprocess.Popen(
            cmd, shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=env
        )
        
        # 实时显示输出
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        return process.returncode == 0
        
    except KeyboardInterrupt:
        print("\n⚠️ Build interrupted by user")
        process.terminate()
        return False

def check_result():
    """检查构建结果"""
    print("📋 Checking build results...")
    
    bin_dir = Path("bin")
    if not bin_dir.exists():
        print("❌ No bin directory found")
        return False
    
    apk_files = list(bin_dir.glob("*.apk"))
    if not apk_files:
        print("❌ No APK files found")
        return False
    
    for apk in apk_files:
        size_mb = apk.stat().st_size / (1024 * 1024)
        print(f"✅ Found APK: {apk.name} ({size_mb:.1f} MB)")
    
    return True

def main():
    """主函数"""
    print("🌱 智慧农场 Android App - 本地构建工具")
    print("=" * 50)
    
    # 检查要求
    if not check_requirements():
        print("❌ Requirements check failed")
        return 1
    
    # 安装依赖
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # 准备 buildozer
    if not prepare_buildozer():
        print("❌ Failed to prepare buildozer")
        return 1
    
    # 构建 APK
    if not build_apk():
        print("❌ APK build failed")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure you have enough disk space (>5GB)")
        print("2. Check your internet connection")
        print("3. Try running: buildozer android clean")
        print("4. For Windows users, consider using WSL or Docker")
        return 1
    
    # 检查结果
    if not check_result():
        print("❌ Build completed but no APK found")
        return 1
    
    print("\n🎉 Build completed successfully!")
    print("📱 You can now install the APK on your Android device")
    return 0

if __name__ == "__main__":
    sys.exit(main())