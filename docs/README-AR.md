<p align="center">
  <img src="../res/kiandesk-logo.jpg" alt="KianDesk" width="160"><br>
  <b>KianDesk</b> — سطح مكتبك البعيد، تحت سيطرتك الكاملة
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-3b63ff">
  <img alt="Built with Rust" src="https://img.shields.io/badge/built%20with-Rust-dea584">
  <img alt="UI" src="https://img.shields.io/badge/UI-Flutter-5ec6ff">
  <a href="../LICENCE"><img alt="License" src="https://img.shields.io/badge/license-AGPL--3.0-blue"></a>
  <a href="https://github.com/freeb5d/KianDesk/releases"><img alt="Release" src="https://img.shields.io/github/v/release/freeb5d/KianDesk?include_prereleases&label=release"></a>
</p>

<p align="center" dir="rtl">
  <a href="#نبذة-عن-المشروع">نبذة عن المشروع</a> •
  <a href="#المميزات">المميزات</a> •
  <a href="#البناء">البناء</a> •
  <a href="#docker">Docker</a> •
  <a href="#هيكل-المشروع">هيكل المشروع</a><br>
  [<a href="../README.md">English</a>] | [<a href="README-FA.md">فارسی</a>] | [<a href="README-ZH.md">中文</a>]
</p>

---

> [!Caution]
> **إخلاء مسؤولية سوء الاستخدام:** لا يوافق مطورو KianDesk ولا يدعمون أي استخدام غير أخلاقي أو غير قانوني لهذا البرنامج. إن سوء الاستخدام، مثل الوصول غير المصرح به أو التحكم أو انتهاك الخصوصية، يتعارض تمامًا مع إرشاداتنا. المطورون غير مسؤولين عن أي سوء استخدام للتطبيق.

## نبذة عن المشروع

KianDesk هو عميل سطح مكتب بعيد مستضاف ذاتيًا لأنظمة **Windows وmacOS وLinux**. يجمع بين نواة Rust عالية الأداء وواجهة Flutter أصلية، ليمنحك تحكمًا بعيدًا سريعًا ومنخفض زمن الاستجابة دون الاعتماد على بنية تحتية لأي طرف آخر.

لا تسجيل، لا ترحيل من طرف ثالث، ولا تتبع — يتصل KianDesk فقط بخادم [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server) الذي تديره وتتحكم فيه بنفسك. جلساتك، بياناتك، خادمك.

## المميزات

- تحكم بعيد سريع ومنخفض زمن الاستجابة بفضل Rust
- الاتصال حصريًا بخادمك الخاص — بلا ترحيل من طرف ثالث
- نقل الملفات، مزامنة الحافظة، وتوجيه الصوت
- إصدارات أصلية لـ Windows وmacOS وLinux

## البناء

### المتطلبات

تستخدم واجهة سطح المكتب Flutter، مدعومة بنواة Rust.

### البدء السريع

١. جهّز بيئة تطوير Rust وأدوات بناء ++C.

٢. ثبّت [vcpkg](https://github.com/microsoft/vcpkg) واضبط متغير البيئة `VCPKG_ROOT`.

```sh
# Windows
vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static aom:x64-windows-static

# Linux / macOS
vcpkg install libvpx libyuv opus aom
```

٣. شغّل المشروع:

```sh
cargo run
```

### البناء على لينكس

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
<summary>خطوات البناء الكاملة (تثبيت vcpkg، إصلاح libvpx على Fedora، البناء)</summary>

```sh
# تثبيت vcpkg
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2023.04.15
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus aom
```

```sh
# إصلاح libvpx (لفيدورا فقط)
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
# البناء
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone --recurse-submodules https://github.com/freeb5d/KianDesk
cd KianDesk
VCPKG_ROOT=$HOME/vcpkg cargo run
```
</details>

## Docker

استنسخ المستودع وابنِ صورة Docker:

```sh
git clone https://github.com/freeb5d/KianDesk
cd KianDesk
git submodule update --init --recursive
docker build -t "kiandesk-builder" .
```

ابنِ التطبيق بالأمر التالي:

```sh
docker run --rm -it -v $PWD:/home/user/rustdesk -v kiandesk-git-cache:/home/user/.cargo/git -v kiandesk-registry-cache:/home/user/.cargo/registry -e PUID="$(id -u)" -e PGID="$(id -g)" kiandesk-builder
```

يقوم البناء الأول بتخزين التبعيات مؤقتًا ويستغرق وقتًا أطول؛ ستكون عمليات البناء اللاحقة أسرع. أضف `--release` في نهاية الأمر أعلاه للحصول على بناء محسّن. سيكون الملف التنفيذي الناتج في مجلد `target`:

```sh
target/debug/rustdesk      # بناء التصحيح
target/release/rustdesk    # بناء الإصدار
```

شغّل هذه الأوامر من جذر مستودع KianDesk حتى يجد التطبيق الموارد المطلوبة.

## هيكل المشروع

| المسار | الوصف |
| --- | --- |
| [`libs/hbb_common`](../libs/hbb_common) | كودك الفيديو، الإعدادات، وغلاف tcp/udp المشترك مع الخادم |
| [`libs/base`](../libs/base) | protobuf، ونقل الملفات، وكود لوحة المفاتيح الخاص بهذا التطبيق |
| [`libs/scrap`](../libs/scrap) | التقاط الشاشة |
| [`libs/enigo`](../libs/enigo) | التحكم بلوحة المفاتيح/الماوس الخاص بالمنصة |
| [`libs/clipboard`](../libs/clipboard) | نسخ/لصق الملفات لـ Windows وLinux وmacOS |
| [`src/server`](../src/server) | خدمات الصوت/الحافظة/الإدخال/الفيديو واتصالات الشبكة |
| [`src/client.rs`](../src/client.rs) | نقطة بدء اتصال النظير |
| [`src/rendezvous_mediator.rs`](../src/rendezvous_mediator.rs) | التواصل مع [KianDesk-Server](https://github.com/freeb5d/KianDesk-Server) |
| [`src/platform`](../src/platform) | كود مخصص للمنصة |
| [`flutter`](../flutter) | واجهة سطح المكتب Flutter |

## الترخيص

راجع [LICENCE](../LICENCE).
