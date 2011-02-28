%define name	qtsixa
%define version	1.4.96
%define rel	1

%define udev_rulesd     /lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	The Sixaxis Joystick Manager
Url:		http://qtsixa.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{name}/%{oname}%20%{version}/%{name}-%{version}.tar.xz
Source1:	sixad.init
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
# %patch0 -p0
# %patch1 -p1 -b .initrddir

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
# rm -rf %{buildroot}

%makeinstall_std
install -d  %{buildroot}%{_initrddir}
install -m 0644 %{SOURCE1} %{buildroot}%{_initrddir}/sixad


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
%{_sysconfdir}/init.d/sixad
%{_sysconfdir}/logrotate.d/sixad