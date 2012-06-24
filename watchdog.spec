Summary:	A software watchdog
Summary(pl):	Programowy stra�nik
Name:		watchdog
Version:	5.2.4
Release:	1
License:	GPL
Group:		Applications/System
Vendor:		Michael Meskes <meskes@debian.org>
Source0:	ftp://ftp.debian.org/debian/pool/main/w/watchdog/%{name}_%{version}.orig.tar.gz
# Source0-md5:	c6ac132d92110eb2c4670d4f684105c3
Source1:	%{name}.init
Source2:	%{name}.sysconfig
# ftp://ftp.debian.org/debian/pool/main/w/watchdog/
Patch0:		%{name}_%{version}-1.diff.gz
BuildRequires:	autoconf
BuildRequires:	automake
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The watchdog program writes to /dev/watchdog every ten seconds. If the
device is open but not written to within a minute the machine will
reboot. Each write delays the reboot time another minute. The ability
to reboot will depend on the state of the machines and interrupts. To
use this software at least a version 1.3.52 kernel is needed.

%description -l pl
Program watchdog zapisuje do /dev/watchdog co 10 sekund. Je�eli
urz�dzenie jest otwarte, ale nic nie zostanie zapisane przez minut�,
maszyna si� zrebootuje. Ka�dy zapis op�nia reboot o minut�. Mo�liwo��
rebootu zale�y od stanu maszyny i przerwa�. Do tego programu potrzebne
jest j�dro w wersji co najmniej 1.3.52.

%prep
%setup -q -n %{name}-%{version}.orig
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/watchdog
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/watchdog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add watchdog
if [ -f /var/lock/subsys/watchdog ]; then
	/etc/rc.d/init.d/watchdog restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/watchdog start\" to start watchdog daemon."
fi

%preun
if [ "$1" = 0 ] ; then
	if [ -f /var/lock/subsys/watchdog ]; then
		/etc/rc.d/init.d/watchdog stop 1>&2
	fi
	/sbin/chkconfig --del watchdog
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README NEWS AUTHORS IAFA-PACKAGE TODO examples
%{_mandir}/man?/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %config /etc/rc.d/init.d/watchdog
%attr(755,root,root) %config /etc/sysconfig/watchdog
%config(noreplace) %{_sysconfdir}/watchdog.conf
