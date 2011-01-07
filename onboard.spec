Name:           onboard
Version:        0.94.0
Release:        %mkrel 1
Summary:        Simple on-screen Keyboard

Group:          User Interface/Desktops
License:        GPLv2+
URL:            https://launchpad.net/onboard/
Source0:        http://launchpad.net/%{name}/0.94/%{version}/+download/%{name}-%{version}.tar.gz
# This is required to not initialize objects of the required libraries. Otherwise
# the setup needs a running X session
Patch0:         onboard-norequires.patch
# To build the .desktop files. This can be upstreamed:
Patch1:         onboard-setup.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  gnome-python-gconf
BuildRequires:  pygtk2.0-devel
BuildRequires:  python-distutils-extra
BuildRequires:  intltool
BuildRequires:  python-setuptools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libxi-devel

Requires:       hicolor-icon-theme
Requires:       pycairo
Requires:       python-virtkey

BuildRequires:  GConf2
Requires(pre):  GConf2
Requires(post): GConf2
Requires(preun): GConf2


%description
An on-screen keyboard useful on tablet PCs or for mobility impaired users.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot}
#fix wrong permissons
chmod a+x %{buildroot}%{_datadir}/onboard/layoutstrings.py
for file in %{buildroot}%{python_sitelib}/Onboard/{settings,IconPalette,KeyboardSVG,utils}.py; do
   chmod a+x $file
done


mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                                    \
    --remove-category="X-GNOME-PersonalSettings"        \
    --add-category="Utility;"                           \
    --dir=%{buildroot}%{_datadir}/applications          \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install                                    \
    --remove-category="X-GNOME-PersonalSettings"        \
    --add-category="Utility;"                           \
    --dir=%{buildroot}%{_datadir}/applications          \
    %{buildroot}%{_datadir}/applications/%{name}-settings.desktop

mkdir -p %{buildroot}%{_datadir}/locale
cp -a build/mo/* %{buildroot}%{_datadir}/locale
%find_lang %{name}

# Move schemas to the correct location
mkdir %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{_datadir}/gconf/ %{buildroot}/%{_sysconfdir}/


%clean
rm -rf %{buildroot}

%pre
if [ "$1" -gt 1 ] ; then
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule \
%{_sysconfdir}/gconf/schemas/%name.schemas >/dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
%{_sysconfdir}/gconf/schemas/%name.schemas > /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%preun
if [ "$1" -eq 0 ] ; then
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule \
%{_sysconfdir}/gconf/schemas/%name.schemas > /dev/null || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README docs/
%{_bindir}/%{name}
%{_bindir}/%{name}-settings
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-settings.desktop
%{_sysconfdir}/gconf/schemas/onboard.schemas
%{_datadir}/icons/hicolor/scalable/apps/onboard.svg
%{_datadir}/icons/hicolor/scalable/apps/onboard2.svg
%{python_sitelib}/Onboard/
%{python_sitelib}/%{name}*.egg-info


