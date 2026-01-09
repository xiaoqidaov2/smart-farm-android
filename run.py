#!/usr/bin/env python3
"""
SmartFarm App 启动脚本
"""

import os
import sys
import subprocess
import argparse


def check_dependencies():
    """检查依赖是否已安装"""
    print("检查依赖...")
    try:
        import kivy
        import kivymd
        import requests
        print("✓ 所有依赖已安装")
        print(f"  - Kivy版本: {kivy.__version__}")
        print(f"  - KivyMD版本: {kivymd.__version__}")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e.name}")
        return False


def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        print("✓ 依赖安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖安装失败")
        return False


def start_app(debug=False):
    """启动应用"""
    print("启动应用...")
    args = [sys.executable, "main.py"]
    if debug:
        args.append("--debug")
    
    try:
        subprocess.check_call(args)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 应用启动失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="SmartFarm App 启动脚本")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    args = parser.parse_args()
    
    if args.install or not check_dependencies():
        if not install_dependencies():
            sys.exit(1)
    
    if not start_app(args.debug):
        sys.exit(1)


if __name__ == "__main__":
    main()
