# TODO:
# - resolve limit of interface traffic:
#   http://bugs.gentoo.org/attachment.cgi?id=80309&action=view
# - check which of these patches can be applied:
#   http://www.christoph-probst.com/technik/software/watchdog/5.2.4/
Summary:	A software watchdog
Summary(pl):	Programowy stra¿nik
Name:		watchdog
Version:	5.2.6
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.debian.org/debian/pool/main/w/watchdog/%{name}_%{version}.orig.tar.gz
# Source0-md5:	43c33708ac07d458bdbd416812481bab
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-foreground.patch
Patch1:		%{name}-debian.patch
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
to reboot will depend on the state of the machines and interrupts. To
use this software at least a version 1.3.52 kernel is needed.

%description -l pl
Program watchdog zapisuje do /dev/watchdog co 10 sekund. Je¿eli
urz±dzenie jest otwarte, ale nic nie zostanie zapisane przez minutê,
maszyna siê zrebootuje. Ka¿dy zapis opó¼nia reboot o minutê. Mo¿liwo¶æ
rebootu zale¿y od stanu maszyny i przerwañ. Do tego programu potrzebne
jest j±dro w wersji co najmniej 1.3.52.

%prep
%setup -q -n %{name}-%{version}.orig
%patch0 -p1
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
%{_mandir}/man?/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/watchdog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/watchdog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/watchdog.conf
