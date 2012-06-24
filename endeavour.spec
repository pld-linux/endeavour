# Conditional build:
%bcond_with	polish	# build with polish translation
#
%define		pname	endeavour2

Summary:	endeavour2 file browser
Summary(pl):	endeavour2 - przegl�darka plik�w
Name:		endeavour
Version:	2.7.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tgz
# Source0-md5:	3542a1d9b529830a830cda569ea68bfb
Source1:	http://abram.eu.org/EndeavourII/%{name}-icons.tgz
# Source1-md5:	d527e5211cc2858ccdc6de72cc3f3ff7
Source2:	%{name}-mimetypes.ini
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-PLD-polish.patch
URL:		http://wolfpack.twu.net/Endeavour2/
BuildRequires:	gtk+-devel >= 1.2
#BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	imlib-devel
#BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_confdir	/etc/%{pname}
%define		_libdirend	%{_libdir}/%{pname}
%define		_icons		%{_datadir}/%{pname}/icons
%define		_help		%{_datadir}/%{pname}/help

%description
endeavour file browser.

%description -l pl
endeavour - przegl�darka plik�w.

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
Summary(pl):	Pliki nag��wkowe endeavour2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Endeavour2 header files.

%description devel -l pl
Pliki nag��wkowe Endeavour2.

%prep
%setup -q -a1
%patch0 -p1
%if %{with polish}
%patch1 -p1
%endif

%build
./configure \
	PLD

%{__make} \
	CC="%{__cc}"			\
	CPP="%{__cxx}"			\
	OPTCFLAGS="%{rpmcflags} -fPIC"	\
	EDV_LIB_DIR=%{_libdir}		\
	LIB_DIRS="-L%{_prefix}/X11R6/%{_lib}"

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
bzip2 -dc endeavour2.1.bz2 > $RPM_BUILD_ROOT%{_mandir}/man1/endeavour2.1
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
%doc AUTHORS HACKING TODO LANGUAGE README
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
