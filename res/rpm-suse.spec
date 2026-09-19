Name:       kiandesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/kiandesk/
mkdir -p %{buildroot}/usr/share/kiandesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/kiandesk %{buildroot}/usr/bin/kiandesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/kiandesk/libsciter-gtk.so
install $HBB/res/kiandesk.service %{buildroot}/usr/share/kiandesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/kiandesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/kiandesk.svg
install $HBB/res/kiandesk.desktop %{buildroot}/usr/share/kiandesk/files/
install $HBB/res/kiandesk-link.desktop %{buildroot}/usr/share/kiandesk/files/

%files
/usr/bin/kiandesk
/usr/share/kiandesk/libsciter-gtk.so
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
    rm /usr/share/applications/kiandesk.desktop || true
    rm /usr/share/applications/kiandesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
