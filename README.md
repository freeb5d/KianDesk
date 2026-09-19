<p align="center">
  <img src="res/kiandesk-logo.jpg" alt="KianDesk" width="160"><br>
  <b>KianDesk</b> — Your Remote Desktop, Under Your Control
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-3b63ff">
  <img alt="Built with Rust" src="https://img.shields.io/badge/built%20with-Rust-dea584">
  <img alt="UI" src="https://img.shields.io/badge/UI-Flutter-5ec6ff">
  <a href="LICENCE"><img alt="License" src="https://img.shields.io/badge/license-AGPL--3.0-blue"></a>
  <a href="https://github.com/freeb5d/KianDesk/releases"><img alt="Release" src="https://img.shields.io/github/v/release/freeb5d/KianDesk?include_prereleases&label=release"></a>
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#build">Build</a> •
  <a href="#docker">Docker</a> •
  <a href="#project-structure">Project Structure</a><br>
  [<a href="docs/README-FA.md">فارسی</a>] | [<a href="docs/README-AR.md">العربية</a>] | [<a href="docs/README-ZH.md">中文</a>]
</p>

---

> [!Caution]
> **Misuse Disclaimer:** The developers of KianDesk do not condone or support any unethical or illegal use of this software. Misuse, such as unauthorized access, control, or invasion of privacy, is strictly against our guidelines. The authors are not responsible for any misuse of the application.

## About

KianDesk is a self-hosted remote desktop client for **Windows**. It pairs a high-performance Rust core with a native Flutter interface, giving you fast, low-latency remote control without depending on anyone else's infrastructure.

There's no sign-up, no third-party relay, and no telemetry — KianDesk connects only to a [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server) that you run and control yourself. Your sessions, your data, your server.

## Features

- Fast, low-latency remote control powered by Rust
- Connects exclusively to your own server — no third-party relays
- File transfer, clipboard sync, and audio forwarding
- Native Windows build

## Build

### Dependencies

The desktop UI uses Flutter, backed by a Rust core.

### Quick start

1. Prepare a Rust development environment and a C++ build toolchain.
2. Install [vcpkg](https://github.com/microsoft/vcpkg) and set the `VCPKG_ROOT` environment variable.

   ```sh
   # Windows
   vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static aom:x64-windows-static

   # Linux / macOS
   vcpkg install libvpx libyuv opus aom
   ```

3. Run the project:

   ```sh
   cargo run
   ```

### Building on Linux

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
<summary>Full build steps (install vcpkg, fix libvpx on Fedora, build)</summary>

```sh
# Install vcpkg
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2023.04.15
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus aom
```

```sh
# Fix libvpx (Fedora only)
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
# Build
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone --recurse-submodules https://github.com/freeb5d/KianDesk
cd KianDesk
VCPKG_ROOT=$HOME/vcpkg cargo run
```
</details>

## Docker

Clone the repository and build the Docker image:

```sh
git clone https://github.com/freeb5d/KianDesk
cd KianDesk
git submodule update --init --recursive
docker build -t "kiandesk-builder" .
```

Build the application with:

```sh
docker run --rm -it -v $PWD:/home/user/rustdesk -v kiandesk-git-cache:/home/user/.cargo/git -v kiandesk-registry-cache:/home/user/.cargo/registry -e PUID="$(id -u)" -e PGID="$(id -g)" kiandesk-builder
```

The first build caches dependencies and takes longer; later builds are faster. Append `--release` to the command above for an optimized build. The resulting binary lands in the `target` folder:

```sh
target/debug/rustdesk      # debug build
target/release/rustdesk    # release build
```

Run these commands from the root of the KianDesk repository so the app can find its resources.

## Project Structure

| Path | Description |
| --- | --- |
| [`libs/hbb_common`](libs/hbb_common) | Video codec, config, and TCP/UDP wrapper shared with the server |
| [`libs/base`](libs/base) | Protobuf, file-transfer, and keyboard code used only by this app |
| [`libs/scrap`](libs/scrap) | Screen capture |
| [`libs/enigo`](libs/enigo) | Platform-specific keyboard/mouse control |
| [`libs/clipboard`](libs/clipboard) | File copy/paste for Windows, Linux, macOS |
| [`src/server`](src/server) | Audio/clipboard/input/video services and network connections |
| [`src/client.rs`](src/client.rs) | Peer connection entry point |
| [`src/rendezvous_mediator.rs`](src/rendezvous_mediator.rs) | Communicates with [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server) |
| [`src/platform`](src/platform) | Platform-specific code |
| [`flutter`](flutter) | Flutter desktop UI |

## License

See [LICENCE](LICENCE).
