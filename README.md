<<<<<<< HEAD
# 智慧农场 Android App (Python/KivyMD)

本项目是一个基于 Python 和 KivyMD 的安卓应用，用于连接 NLECloud 平台，实现智慧农场数据的监控与控制。

## 1. 环境搭建

### 依赖安装
请确保安装了 Python 3.x。然后运行以下命令安装所需库：

```bash
pip install -r requirements.txt
```

### 运行应用
在电脑上调试运行：
```bash
python main.py
```

### 打包成 APK (安卓安装包)

#### 方法 1: 使用 CI/CD 自动构建 (推荐)

**GitHub Actions 构建:**
```bash
# 提交代码到 GitHub
git add .
git commit -m "Update app"
git push origin main

# GitHub Actions 将自动构建 APK，可在 Actions > Artifacts 中下载
# 或访问 GitHub Pages: https://your-username.github.io/your-project
```

**GitLab CI/CD 构建:**
```bash
# 提交代码到 GitLab
git add .
git commit -m "Update app"
git push origin main

# GitLab 将自动构建 APK，可在 CI/CD > Pipelines 中下载
```

#### 方法 2: 本地构建
使用 Buildozer 进行打包 (建议在 Linux 或 WSL 环境下进行)：
```bash
pip install buildozer
buildozer init
# 修改 buildozer.spec 配置文件 (添加依赖: kivymd, requests)
buildozer android debug
```

#### 方法 3: 使用 Docker 构建
```bash
# 构建 Docker 镜像
docker build -t smartfarm-builder .

# 运行构建
docker run -v $(pwd):/app smartfarm-builder
```

详细的 CI/CD 配置说明请参考：
- [GitLab CI/CD 说明](GITLAB_CICD_README.md)
- [GitHub Actions 说明](GITHUB_ACTIONS_README.md)

## 2. NLECloud 平台配置说明

为了让 App 正常工作，请在 [NLECloud 官网](http://www.nlecloud.com/) 完成以下配置：

### 第一步：创建项目
1. 登录 NLECloud。
2. 创建一个新项目 (例如：智慧农场)。

### 第二步：添加设备
1. 在项目下添加一个新设备。
2. 记下 **设备ID** (DeviceId)，App 登录时需要用到 (默认代码中为 `372699`)。

### 第三步：添加传感器与执行器
确保设备的传感器标识名 (ApiTag) 与 App 代码 (`main.py`) 中的一致。请按照下表添加：

| 设备名称 | 标识名 (ApiTag) | 类型 | 数据类型 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| 光照传感器 | guangzhao_sum | 传感器 | 整数/浮点 | 只上报 |
| 空气温度 | temperature | 传感器 | 整数/浮点 | 只上报 |
| 空气湿度 | humidity | 传感器 | 整数/浮点 | 只上报 |
| CO2浓度 | CO2 | 传感器 | 整数/浮点 | 只上报 |
| 土壤温度 | Soil_temperture | 传感器 | 整数/浮点 | 只上报 |
| 土壤湿度 | Soil_moisture | 传感器 | 整数/浮点 | 只上报 |
| 土壤盐度 | Soil_sanility | 传感器 | 整数/浮点 | 只上报 |
| 氮含量 | Nhanl | 传感器 | 整数/浮点 | 只上报 |
| 磷含量 | Phanl | 传感器 | 整数/浮点 | 只上报 |
| 钾含量 | jia | 传感器 | 整数/浮点 | 只上报 |
| 土壤PH | PH | 传感器 | 整数/浮点 | 只上报 |
| 光照(Zigbee)| zigbee_fun | 传感器 | 浮点 | 只上报 |
| 风扇 | fun | 执行器 | 布尔/整数 | 上报和下发 (0/1) |
| 康灯 | LVD | 执行器 | 布尔/整数 | 上报和下发 (0/1) |

## 3. 功能说明

- **登录界面**：输入 NLECloud 账号、密码和设备ID进行登录。
- **环境监测**：实时显示各个传感器的数据，每 5 秒自动刷新。
- **设备控制**：点击开关控制风扇和灯的开启/关闭。
- **界面风格**：采用扁平化设计，卡片式布局，清晰直观。
=======
# smart-farm-android



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

* [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
* [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/xiaoqidaozhang/smart-farm-android.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

* [Set up project integrations](https://gitlab.com/xiaoqidaozhang/smart-farm-android/-/settings/integrations)

## Collaborate with your team

* [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
* [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
* [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
* [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
* [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

* [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
* [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
* [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
* [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
* [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
>>>>>>> dd60e1752f9ad98eaa6d13bc0f23b3d2bb077b8e
