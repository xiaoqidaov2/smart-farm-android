# Dockerfile for building Android APK locally
FROM ubuntu:20.04

# 避免交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update -qq && apt-get install -y -qq \
    git wget curl unzip python3 python3-pip python3-venv \
    build-essential libssl-dev libffi-dev python3-dev \
    openjdk-11-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置 Java 环境
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY buildozer.spec .
COPY *.py .

# 安装 Python 依赖
RUN python3 -m pip install --upgrade pip && \
    pip3 install buildozer cython && \
    pip3 install -r requirements.txt

# 安装 Android SDK
ENV ANDROID_SDK_TOOLS=9477386
ENV ANDROID_COMPILE_SDK=33
ENV ANDROID_BUILD_TOOLS=33.0.0

RUN wget --quiet --output-document=android-sdk.zip \
    https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_TOOLS}_latest.zip && \
    unzip -q android-sdk.zip -d android-sdk-linux && \
    rm android-sdk.zip

ENV ANDROID_SDK_ROOT=/app/android-sdk-linux
ENV ANDROID_HOME=$ANDROID_SDK_ROOT
ENV PATH=$PATH:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools

RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    mv ${ANDROID_SDK_ROOT}/cmdline-tools/* ${ANDROID_SDK_ROOT}/cmdline-tools/latest/ 2>/dev/null || true

# 接受许可证并安装 SDK 组件
RUN yes | sdkmanager --licenses >/dev/null 2>&1 || true && \
    sdkmanager "platforms;android-${ANDROID_COMPILE_SDK}" "build-tools;${ANDROID_BUILD_TOOLS}" && \
    sdkmanager "ndk;21.4.7075529"

ENV ANDROID_NDK_ROOT=${ANDROID_SDK_ROOT}/ndk/21.4.7075529

# 构建命令
CMD ["buildozer", "android", "debug"]