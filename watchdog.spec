# TODO:
# - resolve limit of interface traffic:
#   http://bugs.gentoo.org/attachment.cgi?id=80309&action=view
# - check which of these patches can be applied:
#   http://www.christoph-probst.com/technik/software/watchdog/5.2.4/
# - separate package with init-script for wd_keepalive - some parts should
#   be in -common subpackage.
Summary:	A software watchdog
Summary(pl.UTF-8):	Programowy strażnik
Name:		watchdog
Version:	5.16
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://ftp.debian.org/debian/pool/main/w/watchdog/%{name}_%{version}.orig.tar.gz
# Source0-md5:	1b4f51cabc64d1bee2fce7cdd626831f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-foreground.patch
Patch1:		%{name}-config.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The watchdog program writes to /dev/watchdog every ten seconds. If the
device is open but not written to within a minute the machine will
reboot. Each write delays the reboot time another minute. The ability
to reboot will depend on the state of the machines and interrupts.

%description -l pl.UTF-8
Program watchdog zapisuje do /dev/watchdog co 10 sekund. Jeżeli
urządzenie jest otwarte, ale nic nie zostanie zapisane przez minutę,
maszyna się zrebootuje. Każdy zapis opóźnia reboot o minutę. Możliwość
rebootu zależy od stanu maszyny i przerwań.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/watchdog
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/watchdog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add watchdog
%service watchdog restart "watchdog daemon"

%preun
if [ "$1" = 0 ] ; then
	%service watchdog stop
	/sbin/chkconfig --del watchdog
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README NEWS AUTHORS IAFA-PACKAGE TODO examples
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/watchdog.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/watchdog
%attr(754,root,root) /etc/rc.d/init.d/watchdog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
