<p align="center">
  <img src="../res/kiandesk-logo.jpg" alt="KianDesk" width="160"><br>
  <b>KianDesk</b> — 您的远程桌面，完全掌控在您手中
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-3b63ff">
  <img alt="Built with Rust" src="https://img.shields.io/badge/built%20with-Rust-dea584">
  <img alt="UI" src="https://img.shields.io/badge/UI-Flutter-5ec6ff">
  <a href="../LICENCE"><img alt="License" src="https://img.shields.io/badge/license-AGPL--3.0-blue"></a>
  <a href="https://github.com/freeb5d/KianDesk/releases"><img alt="Release" src="https://img.shields.io/github/v/release/freeb5d/KianDesk?include_prereleases&label=release"></a>
</p>

<p align="center">
  <a href="#关于">关于</a> •
  <a href="#特性">特性</a> •
  <a href="#构建">构建</a> •
  <a href="#docker">Docker</a> •
  <a href="#项目结构">项目结构</a><br>
  [<a href="../README.md">English</a>] | [<a href="README-FA.md">فارسی</a>] | [<a href="README-AR.md">العربية</a>]
</p>

---

> [!Caution]
> **滥用免责声明：** KianDesk 的开发者不认可也不支持以任何不道德或非法的方式使用本软件。诸如未经授权的访问、控制或侵犯隐私等滥用行为，严重违反我们的准则。作者对本应用程序的任何滥用行为不承担责任。

## 关于

KianDesk 是一款适用于 **Windows、macOS 和 Linux** 的自托管远程桌面客户端。它将高性能的 Rust 内核与原生 Flutter 界面相结合，带来快速、低延迟的远程控制体验，无需依赖任何第三方基础设施。

无需注册，没有第三方中继，也没有遥测 —— KianDesk 只连接到您自己运行和掌控的 [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server)。您的会话，您的数据，您的服务器。

## 特性

- 基于 Rust 的快速、低延迟远程控制
- 仅连接您自己的服务器 —— 没有第三方中继
- 文件传输、剪贴板同步与音频转发
- 为 Windows、macOS、Linux 提供原生构建

## 构建

### 依赖项

桌面界面使用 Flutter 构建，后端由 Rust 内核驱动。

### 快速开始

1. 准备好 Rust 开发环境和 C++ 构建工具链。
2. 安装 [vcpkg](https://github.com/microsoft/vcpkg) 并设置 `VCPKG_ROOT` 环境变量。

   ```sh
   # Windows
   vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static aom:x64-windows-static

   # Linux / macOS
   vcpkg install libvpx libyuv opus aom
   ```

3. 运行项目：

   ```sh
   cargo run
   ```

### 在 Linux 上构建

<details>
<summary>Ubuntu 18 (Debian 10)</summary>

```sh
sudo apt install -y zip g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxdo-dev \
        libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake make \
        libclang-dev ninja-build libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```
</details>

<details>
<summary>openSUSE Tumbleweed</summary>

```sh
sudo zypper install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libXfixes-devel cmake alsa-lib-devel gstreamer-devel gstreamer-plugins-base-devel xdotool-devel
```
</details>

<details>
<summary>Fedora 28 (CentOS 8)</summary>

```sh
sudo yum -y install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libxdo-devel libXfixes-devel pulseaudio-libs-devel cmake alsa-lib-devel gstreamer1-devel gstreamer1-plugins-base-devel
```
</details>

<details>
<summary>Arch (Manjaro)</summary>

```sh
sudo pacman -Syu --needed unzip git cmake gcc curl wget yasm nasm zip make pkg-config clang gtk3 xdotool libxcb libxfixes alsa-lib pipewire
```
</details>

<details>
<summary>完整构建步骤（安装 vcpkg、修复 Fedora 上的 libvpx、构建）</summary>

```sh
# 安装 vcpkg
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2023.04.15
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus aom
```

```sh
# 修复 libvpx（仅限 Fedora）
cd vcpkg/buildtrees/libvpx/src
cd *
./configure
sed -i 's/CFLAGS+=-I/CFLAGS+=-fPIC -I/g' Makefile
sed -i 's/CXXFLAGS+=-I/CXXFLAGS+=-fPIC -I/g' Makefile
make
cp libvpx.a $HOME/vcpkg/installed/x64-linux/lib/
cd
```

```sh
# 构建
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone --recurse-submodules https://github.com/freeb5d/KianDesk
cd KianDesk
VCPKG_ROOT=$HOME/vcpkg cargo run
```
</details>

## Docker

克隆仓库并构建 Docker 镜像：

```sh
git clone https://github.com/freeb5d/KianDesk
cd KianDesk
git submodule update --init --recursive
docker build -t "kiandesk-builder" .
```

使用以下命令构建应用程序：

```sh
docker run --rm -it -v $PWD:/home/user/rustdesk -v kiandesk-git-cache:/home/user/.cargo/git -v kiandesk-registry-cache:/home/user/.cargo/registry -e PUID="$(id -u)" -e PGID="$(id -g)" kiandesk-builder
```

首次构建会缓存依赖项，耗时较长；后续构建会更快。在上面的命令末尾加上 `--release` 即可构建优化版本。生成的可执行文件位于 `target` 文件夹：

```sh
target/debug/rustdesk      # 调试版本
target/release/rustdesk    # 发布版本
```

请在 KianDesk 仓库根目录下运行这些命令，以便应用程序能找到所需的资源。

## 项目结构

| 路径 | 说明 |
| --- | --- |
| [`libs/hbb_common`](../libs/hbb_common) | 视频编解码器、配置，以及与服务器共享的 tcp/udp 封装 |
| [`libs/base`](../libs/base) | protobuf、文件传输及仅供本应用使用的键盘代码 |
| [`libs/scrap`](../libs/scrap) | 屏幕捕获 |
| [`libs/enigo`](../libs/enigo) | 平台相关的键盘/鼠标控制 |
| [`libs/clipboard`](../libs/clipboard) | 适用于 Windows、Linux、macOS 的文件复制粘贴 |
| [`src/server`](../src/server) | 音频/剪贴板/输入/视频服务及网络连接 |
| [`src/client.rs`](../src/client.rs) | 对等连接入口 |
| [`src/rendezvous_mediator.rs`](../src/rendezvous_mediator.rs) | 与 [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server) 通信 |
| [`src/platform`](../src/platform) | 平台相关代码 |
| [`flutter`](../flutter) | Flutter 桌面界面 |

## 许可证

参见 [LICENCE](../LICENCE)。
