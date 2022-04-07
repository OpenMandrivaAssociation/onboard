Name:           onboard
Version:        1.4.1
Release:        2
Summary:        Simple on-screen Keyboard

Group:          System/X11
License:        GPLv2+
URL:            https://launchpad.net/onboard/
Source0:        http://launchpad.net/%{name}/%{vmaj}/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:         linking.patch
Patch1:         0001-Port-to-Ayatana-AppIndicator.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(python)
BuildRequires:  python3dist(python-distutils-extra)
BuildRequires:  python3dist(setuptools)

Requires:       at-spi2-atk
Requires:       fonts-ttf-dejavu
Requires:       hicolor-icon-theme
Requires:       mousetweaks
Requires:       python3dist(pycairo)
Requires:       python-dbus
Requires:       python3dist(pygobject)
Requires:       iso-codes

%description
An on-screen keyboard useful on tablet PCs or for mobility impaired users.


%package -n gnome-shell-extensions-%{name}
Summary:        Shell extension for gnome
Conflicts:      onboard < 1.2

%description -n gnome-shell-extensions-%{name}
Shell extension for gnome.

%prep
%setup -q
%autopatch -p1

%build
%py3_build

%install
%py3_install

# Use example default configuration file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp %{buildroot}%{_datadir}/%{name}/%{name}-defaults.conf.example %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Swich to full keyboard
sed -i 's/#layout=Full Keyboard/layout=Full Keyboard/' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
sed -i 's/layout=Compact/#layout=Compact/' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Use superkey label
sed -i 's/superkey-label=.*$/superkey-label=/' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Switch font to DejaVu-Sans
sed -i 's/^key-label-font=.*$/key-label-font=DejaVu Sans/' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Configuration change for patch0 (StatusIconProvider.patch)
sed -i '/\[main\]/a status-icon-provider=GtkStatusIcon' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Enable icon-palette for gnome3 or on closing keyboard there is no visible activation method
sed -i '/\[icon-palette\]/a in-use=True' %{buildroot}%{_sysconfdir}/%{name}/%{name}-defaults.conf
# Remove Ubuntu icons
rm -rf %{buildroot}%{_iconsdir}/ubuntu*
# Desktop files
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                                    \
    --remove-category="X-GNOME-PersonalSettings"        \
    --add-category="Utility;"                           \
    --dir=%{buildroot}%{_datadir}/applications          \
    %{_builddir}/%{name}-%{version}/build/share/applications/%{name}.desktop

desktop-file-install                                    \
    --remove-category="X-GNOME-PersonalSettings"        \
    --remove-category="Settings"                        \
    --add-category="Utility;"                           \
    --dir=%{buildroot}%{_datadir}/applications          \
    %{_builddir}/%{name}-%{version}/build/share/applications/%{name}-settings.desktop

# Desktop files autostart
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
desktop-file-install                                    \
    --add-category="Utility;"                           \
    --dir=%{buildroot}%{_sysconfdir}/xdg/autostart                  \
    %{_builddir}/%{name}-%{version}/build/share/autostart/%{name}-autostart.desktop

mkdir -p %{buildroot}%{_datadir}/locale
cp -a build/mo/* %{buildroot}%{_datadir}/locale

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/%{name}
%{_bindir}/%{name}-settings
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-settings.desktop
%{_datadir}/glib-2.0/schemas/org.%{name}.gschema.xml
%{_datadir}/dbus-1/services/org.%{name}.Onboard.service
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_iconsdir}/HighContrast/scalable/apps/%{name}.svg
%{_iconsdir}/hicolor/22x22/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/24x24/apps/%{name}.png
%{_iconsdir}/hicolor/28x28/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_datadir}/%{name}/
%{_datadir}/sounds/freedesktop/stereo/%{name}-key-feedback.oga
%{python_sitearch}/%{name}*.egg-info
%{python_sitearch}/Onboard/
%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-defaults.conf
%{_mandir}/man1/onboard*


%files -n gnome-shell-extensions-%{name}
%{_datadir}/gnome-shell/extensions/Onboard_Indicator@onboard.org/




%changelog
* Fri Jan 07 2011 Antoine Ginies <aginies@mandriva.com> 0.94.0-1mdv2011.0
+ Revision: 629470
- fix group
- import onboard

