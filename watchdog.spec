Name:		watchdog
Version:	4.5
Release:	2
Summary:	A software watchdog
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Vendor:		Michael Meskes <meskes@debian.org>
Icon:		doggy.gif
Source0:	ftp://tsx-11.mit.edu/pub/linux/sources/sbin/%{name}-%{version}.tar.gz
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The watchdog program writes to /dev/watchdog every ten seconds. If the
device is open but not written to within a minute the machine will
reboot. Each write delays the reboot time another minute. The ability
to reboot will depend on the state of the machines and interrupts. To
use this software at least a version 1.3.52 kernel is needed.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{dev,etc/rc.d/init.d}
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install -c -m 755 rc.watchdog.redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/watchdog

%clean
rm -rf $RPM_BUILD_ROOT

%post
rm -f /dev/watchdog /dev/temperature
mknod /dev/watchdog c 10 130
mknod /dev/temperature c 10 131
/sbin/chkconfig --add watchdog

%postun
if [ "$1" = 0 ] ; then
  /sbin/chkconfig --del watchdog
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog examples README NEWS AUTHORS COPYING IAFA-PACKAGE
%doc INSTALL watchdog.lsm
%{_prefix}/man/man?/*
%attr(755, root, root) %{_sbindir}/watchdog
%attr(755, root, root) %config /etc/rc.d/init.d/watchdog
%config %{_sysconfdir}/watchdog.conf
