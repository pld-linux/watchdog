%define name	watchdog
%define version	4.5
%define release	2
%define prefix	/usr

Name: %{name}
Version: %{version}
Release: %{release}
Summary: A software watchdog
Copyright: GPL
Group: Applications/System
Vendor: Michael Meskes <meskes@debian.org>
Distribution: Should be part of RedHat Linux
Icon: doggy.gif
Source: ftp://tsx-11.mit.edu/pub/linux/sources/sbin/%{name}-%{version}.tar.gz
Buildroot: /tmp/%{name}-%{version}-%{release}-root
Packager: jorgens+rpm@pvv.org

%description
The watchdog program writes to /dev/watchdog every ten seconds.
If the device is open but not written to within a minute the machine
will reboot.  Each write delays the reboot time another minute.
The ability to reboot will depend on the state of the machines
and interrupts.  To use this software at least a version 1.3.52
kernel is needed.

%prep
%setup

%build
./configure --prefix=%{prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{dev,etc/rc.d/init.d}
make install DESTDIR=$RPM_BUILD_ROOT
install -c -m 755 rc.watchdog.redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/watchdog

%clean
rm -rf $RPM_BUILD_ROOT

%post
rm -f /dev/watchdog /dev/temperature
mknod /dev/watchdog c 10 130
mknod /dev/temperature c 10 131
%chkconfig_add

%preun
%chkconfig_del

%files
%defattr(0644, root, root, 0755)
%doc ChangeLog examples README NEWS AUTHORS COPYING IAFA-PACKAGE
%doc INSTALL watchdog.lsm
/usr/man/man?/*
%attr(755, root, root) /usr/sbin/watchdog
%attr(755, root, root) %config /etc/rc.d/init.d/watchdog
%config /etc/watchdog.conf

%changelog
* Mon Jul 19 1999 Peter Soos <sp@osb.hu>
- Modify the spec file to build the package as an ordinary user
- Added %changelog
- Added %config and %attr macros
- Rebuilt under RedHat Linux 6.0
