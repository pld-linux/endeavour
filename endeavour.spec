%define		pname	endeavour2

Summary:	endeavour2 file browser
Summary(pl):	endeavour2 - przegl±darka plików
Name:		endeavour
Version:	2.5.6
Release:	0.7
License:	GPL
Group:		X11/Applications
Source0:	http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tgz
# Source-md5:	14a03e7eb47d7434520cd024df695935
Source1:	http://abram.eu.org/EndeavourII/%{name}-icons.tgz
# Source-md5:	d527e5211cc2858ccdc6de72cc3f3ff7
Source2:	%{name}-mimetypes.ini
Patch0:		%{name}-PLD.patch
URL:		http://wolfpack.twu.net/Endeavour2/
BuildRequires:	gtk+-devel
BuildRequires:	imlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_confdir	/etc/%{pname}
%define		_libdirend	%{_libdir}/%{pname}
%define		_icons		%{_datadir}/%{pname}/icons
%define		_help		%{_datadir}/%{pname}/help

%description
endeavour file browser.

%description -l pl
endeavour - przegl±darka plików.

%package libs
Summary:	Endeavour2 library
Summary(pl):	Bibloteka Endeavour2
Group:		X11/Applications

%description libs
Endeavour2 library.

%description libs -l pl
Biblioteka Endeavour2.

%package devel
Summary:	Header files for endeavour2
Summary(pl):	Pliki nag³ówkowe endeavour2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Endeavour2 header files.

%description devel -l pl
Pliki nag³ówkowe Endeavour2.

%prep
%setup -q -a1
%patch0 -p1

%build
./configure \
	PLD

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_confdir},%{_libdirend},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_icons},%{_mandir}/man1,%{_help}} \
	$RPM_BUILD_ROOT%{_includedir}/%{pname}

# add xpm icons for OO type
install icons/{ooo_calc.xpm,ooo_impress.xpm,ooo_writer.xpm,sdc.xpm,sdw.xpm} $RPM_BUILD_ROOT%{_icons}
# instalation from package is ugly so I decide to put files by my self
cd endeavour2
install %{pname} $RPM_BUILD_ROOT%{_bindir}
install download.front/download.front $RPM_BUILD_ROOT%{_libdirend}
install fsck.front/fsck.front $RPM_BUILD_ROOT%{_libdirend}
install format.front/format.front $RPM_BUILD_ROOT%{_libdirend}
install images/* $RPM_BUILD_ROOT%{_icons}
install data/help/* $RPM_BUILD_ROOT%{_help}
install endeavour2.1.bz2 $RPM_BUILD_ROOT%{_mandir}/man1
# devel
install lib/*.h $RPM_BUILD_ROOT%{_includedir}/%{pname}
install lib/libendeavour2.so $RPM_BUILD_ROOT%{_libdir}
install lib/endeavour2-config $RPM_BUILD_ROOT%{_bindir}

# mime types by abram@
install %{SOURCE2} $RPM_BUILD_ROOT%{_confdir}/mimetypes.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING INSTALL LICENSE TODO LANGUAGE README
%attr(755,root,root) %{_bindir}/%{pname}
%attr(755,root,root) %{_libdirend}
%{_mandir}/man1/*
%dir %{_datadir}/%{pname}
%{_icons}
%{_help}
%{_confdir}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libendeavour2.so

%files devel
%defattr(644,root,root,755)
%doc endeavour2/lib/INTERPS
%attr(755,root,root) %{_bindir}/endeavour2-config
%{_includedir}/%{pname}
