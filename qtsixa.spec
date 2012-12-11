%define oname	QtSixA

%define udev_rulesd     /lib/udev/rules.d

Name:		qtsixa
Version:	1.5.1
Release:	3
Summary:	The Sixaxis Joystick Manager
License:	GPLv2
Group:		System/Configuration/Hardware
Url:		http://qtsixa.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{name}/%{oname}%20%{version}/%{oname}-%{version}-src.tar.xz
Source1:	sixad.init
Patch0:		qtsixa-1.5.1-gcc4.7.patch
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dbus-1)
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
%setup -q -n QtSixA-1.5.1
%patch0 -p1

%build
%make

%install
%makeinstall_std
install -d  %{buildroot}%{_initrddir}
install -m 0644 %{SOURCE1} %{buildroot}%{_initrddir}/sixad

#symlink
pushd %{buildroot}%{_datadir}/%{name}
	ln -s %{_sysconfdir}/qtsixa.conf .
popd

%post -n sixad
%_post_service sixad

%preun -n sixad
%_preun_service sixad

%files
%{_bindir}/sixad-*
%{_bindir}/qtsixa
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm

%files -n sixad
%config(noreplace) %{_sysconfdir}/default/sixad
%{_sbindir}/sixad-*
%{_sbindir}/hidraw-dump
%{_sbindir}/sixpair
%{_sbindir}/sixpair-kbd
%{_bindir}/sixad
%{_initrddir}/sixad
%{_sysconfdir}/init.d/sixad
%{_sysconfdir}/logrotate.d/sixad

