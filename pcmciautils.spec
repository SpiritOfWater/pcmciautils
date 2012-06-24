#
# Conditional build:
%bcond_without	startup		# build without resource database initiallization
%bcond_without	udev		# build with hotplug instead of udev
#
Summary:	PCMCIA initialization utils for kernels >= 2.6.13
Summary(pl):	Narz�dzia startowe pcmcia dla kerneli >= 2.6.13
Name:		pcmciautils
Version:	010
Release:	0.1
License:	GPL v2
Group:		Base
Source0:	http://kernel.org/pub/linux/utils/kernel/pcmcia/%{name}-%{version}.tar.bz2
# Source0-md5:	ff3cb012fd1a8801e912054b45420ac2
#Patch0:		%{name}-DESTDIR.patch
URL:		http://kernel.org/pub/linux/utils/kernel/pcmcia/pcmcia.html
BuildRequires:	flex
BuildRequires:	sysfsutils-devel >= 1.3.0
BuildRequires:	sed >= 4.0
Requires:	udev
Requires:	module-init-tools >= 3.2-0.pre4.1
#if kernel used >= 2.6.13
#Obsoletes:	pcmcia-cs
#else
#BuildRequires:	useless
#endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PCMCIA initialization utils to be used with kernels >= 2.6.13.
They are designed for new PCMCIA subsystem and are replacement for old
pcmcia-cs package.

%description -l pl
Narz�dzia startowe pcmcia dla kerneli >= 2.6.13. Zosta�y stworzone dla
nowego podsystemu PCMCIA i zast�puj� stary pakiet pcmcia-cs.

%prep
%setup -q

%build
%if %{without startup}
sed -i -e "s#STARTUP =.*#STARTUP = false#g" Makefile
%endif
%if %{with udev}
sed -i -e "s#UDEV =.*#UDEV = true#g" Makefile
%endif

%{__make}
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if %{with startup}
%dir %{_sysconfdir}/pcmcia
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/config.opts
%endif
%if %{with udev}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/60-pcmcia.rules
%else
%{_sysconfdir}/hotplug/*
%endif
%attr(755,root,root) /sbin/pccardctl
%attr(755,root,root) /sbin/pcmcia-check-broken-cis
%if %{with startup}
%attr(755,root,root) /sbin/pcmcia-socket-startup
%endif
