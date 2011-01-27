%define name	qtsixa
%define version	1.4.95
%define rel	1

%define udev_rulesd     /lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	The Sixaxis Joystick Manager
Url:		http://qtsixa.sourceforge.net/
Source:		http://downloads.sourceforge.net/project/%{name}/%{oname}%20%{version}/%{name}_%{version}.tar.gz
Patch0:		qtsixa-fstat.patch
Patch1:		qtsixa-initrddir.patch
License:	GPLv2
Group:		System/Configuration/Hardware
BuildRequires:	bluez-devel libjack-devel
BuildRequires:	libusb-devel
BuildRequires:	glib2-devel
BuildRequires:	dbus-devel
BuildRequires:	python-qt4-devel
Requires:	sixad = %{version}-%{release}
Requires:	python-qt4
Requires:	python-dbus
Requires:	libnotify
Requires:	bluez
Requires:	bluez-hcidump
Requires:	xdg-utils
Requires:	x11-driver-input-joystick

%description
This package provides a useful GUI to control the sixad modules.

QtSixA is written in PyQt.

%package -n sixad
Summary:	[Qt]SixA Daemon
Group:		Development/C
Requires(post):		rpm-helper
Requires(preun):	rpm-helper

%description -n sixad
This package provides the modules (called 'sixad') for connecting PS3 hardware
(Sixaxis/DualShock3 and Keypads) to a Linux-compatible machine.

Currently sixad supports:
 - Sixaxis buttons, axis, accelerometers and LEDs
 - PS3 Keypads

sixad also registers the Sixaxis and Keypad's MAC/ID in the joystick name
(ex: "PLAYSTATION(R)3 Controller (00:XX:X0:0X:XX)".

sixad is triggered by udev, making it super easy to connect new devices
(you just need to press the PS button).

%prep
%setup -q -n qtsixa-1.5.0
%patch0 -p0
%patch1 -p1 -b .initrddir

#fix rights
#chmod a-x qtsixa/manual/* qtsixa/doc/* TODO

#fix build flags
sed -i -e 's|-Wall -O2|%{optflags}|g' utils/Makefile
sed -i -e 's|-g -O2 -g -Wall -O2 -D_FORTIFY_SOURCE=2|%{optflags}|g' utils/hcid/Makefile

#fix build
sed -i -e 's|/usr/lib/libbluetooth.so|/%{_lib}/libbluetooth.so|g' utils/hcid/Makefile
sed -i -e 's|/usr/lib/|%{_libdir}/|g' utils/hcid/Makefile

%build
%make

%install
rm -rf %{buildroot}

# sixa, binaries
install -Dp -m0755 sixad/sixad %{buildroot}%{_bindir}/sixad
mkdir -p %{buildroot}%{_sbindir}/
install -Dp -m0755 sixad/bins/* %{buildroot}%{_sbindir}/

# sixa, misc files
install -Dp -m0644 sixad/98-sixad.rules %{buildroot}%{udev_rulesd}/98-sixad.rules
install -d %{buildroot}/etc/default/
install -d %{buildroot}/etc/init.d/
install -d %{buildroot}}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/lib/sixad/
install -m 644 sixad.default %{buildroot}/etc/default/sixad
install -m 655 sixad/sixad.init %{buildroot}/etc/init.d/sixad
install -m 655 sixad %{buildroot}%{_bindir}
install -m 655 bins/sixad-bin %{buildroot}%{_sbindir}
install -m 655 bins/sixad-sixaxis %{buildroot}%{_sbindir}
install -m 655 bins/sixad-raw %{buildroot}%{_sbindir}


# qtsixa
install -d -m0755 %{buildroot}%{_datadir}/qtsixa/{game-profiles,gui,pics,lang,icons,sixaxis-profiles}
install -Dp -m0644 qtsixa/game-profiles/* %{buildroot}%{_datadir}/qtsixa/game-profiles/
install	-Dp -m0644 qtsixa/gui/* %{buildroot}%{_datadir}/qtsixa/gui/
install -Dp -m0644 qtsixa/pics/* %{buildroot}%{_datadir}/qtsixa/pics/
install -Dp -m0644 qtsixa/lang/* %{buildroot}%{_datadir}/qtsixa/lang/
install -Dp -m0644 qtsixa/icons/* %{buildroot}%{_datadir}/qtsixa/icons/
install -Dp -m0644 qtsixa/sixaxis-profiles/* %{buildroot}%{_datadir}/qtsixa/sixaxis-profiles/
install -Dp -m0755 qtsixa/sixa %{buildroot}%{_bindir}
install	-Dp -m0755 qtsixa/sixa-lq %{buildroot}%{_bindir}
install	-Dp -m0755 qtsixa/sixa-notify %{buildroot}%{_bindir}
install	-Dp -m0755 qtsixa/qtsixa %{buildroot}%{_bindir}
install	-Dp -m0644 qtsixa/qtsixa.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -Dp -m0644 qtsixa/qtsixa.desktop %{buildroot}%{_datadir}/applications/qtsixa.desktop
install -Dp -m0644 qtsixa/qtsixa.xpm %{buildroot}%{_datadir}/pixmaps/qtsixa.xpm
install -Dp -m0644 qtsixa/profiles.list.bu %{buildroot}%{_datadir}/%{name}/
install -Dp -m0644 qtsixa/features.html %{buildroot}%{_datadir}/%{name}/
install -Dp -m0644 qtsixa/sixa-notify.desktop %{buildroot}%{_datadir}/%{name}/
install -Dp -m0644 qtsixa/profiles.list.bu %{buildroot}%{_datadir}/%{name}/profiles.list

#symlink
pushd %{buildroot}%{_datadir}/%{name}
	ln -s %{_sysconfdir}/qtsixa.conf .
popd

%clean
rm -rf %{buildroot}

%post -n sixad
%_post_service sixad

%preun -n sixad
%_preun_service sixad

%files
%defattr(-,root,root)
%doc qtsixa/manual/
%doc README TODO
%{_bindir}/sixpair
%{_bindir}/sixpair-kbd
%{_bindir}/sixad-*
%{_bindir}/qtsixa
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm

%files -n sixad
%defattr(-,root,root)
%doc sixad/README
%config(noreplace) %{_sysconfdir}/default/sixad
%{_bindir}/sixad
%{_sbindir}/*
%{udev_rulesd}/*
%{_initrddir}/sixad

