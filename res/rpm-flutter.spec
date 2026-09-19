Name:       kiandesk
Version:    1.0.0
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://github.com/freeb5d/KianDesk
Vendor:     KianDesk
Requires:   gtk3 libxcb libXfixes alsa-lib libva gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/kiandesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/kiandesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/kiandesk.service -t "%{buildroot}/usr/share/kiandesk/files"
install -Dm 644 $HBB/res/kiandesk.desktop -t "%{buildroot}/usr/share/kiandesk/files"
install -Dm 644 $HBB/res/kiandesk-link.desktop -t "%{buildroot}/usr/share/kiandesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/kiandesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/kiandesk.svg"

%files
/usr/share/kiandesk/*
/usr/share/kiandesk/files/kiandesk.service
/usr/share/icons/hicolor/256x256/apps/kiandesk.png
/usr/share/icons/hicolor/scalable/apps/kiandesk.svg
/usr/share/kiandesk/files/kiandesk.desktop
/usr/share/kiandesk/files/kiandesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop kiandesk || true
  ;;
esac

%post
cp /usr/share/kiandesk/files/kiandesk.service /etc/systemd/system/kiandesk.service
cp /usr/share/kiandesk/files/kiandesk.desktop /usr/share/applications/
cp /usr/share/kiandesk/files/kiandesk-link.desktop /usr/share/applications/
ln -sf /usr/share/kiandesk/kiandesk /usr/bin/kiandesk
systemctl daemon-reload
systemctl enable kiandesk
systemctl start kiandesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop kiandesk || true
    systemctl disable kiandesk || true
    rm /etc/systemd/system/kiandesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/kiandesk || true
    rmdir /usr/lib/kiandesk || true
    rmdir /usr/local/kiandesk || true
    rmdir /usr/share/kiandesk || true
    rm /usr/share/applications/kiandesk.desktop || true
    rm /usr/share/applications/kiandesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/kiandesk || true
    rmdir /usr/local/kiandesk || true
  ;;
esac
