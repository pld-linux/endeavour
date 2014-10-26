#
# Conditional build:
%bcond_with	gtk2	# GTK+ 2.x port (incomplete)
%bcond_with	polish	# build with Polish translation [outdated patch]
#
Summary:	Endeavour Mark II file management suite
Summary(pl.UTF-8):	Oprogramowanie do zarządzania plikami Endeavour Mark II
Name:		endeavour
Version:	3.1.4
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
# Source0-md5:	1952cf9ef05b75abe48b45cb4068427f
Source1:	http://abram.eu.org/EndeavourII/%{name}-icons.tgz
# Source1-md5:	d527e5211cc2858ccdc6de72cc3f3ff7
Source2:	%{name}-mimetypes.ini
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-fixes.patch
Patch2:		%{name}-giflib.patch
Patch3:		%{name}-verbose.patch
Patch4:		%{name}-libmng.patch
Patch5:		%{name}-libpng.patch
Patch6:		%{name}-PLD-polish.patch
URL:		http://freecode.com/projects/endeavour2
BuildRequires:	bzip2-devel
BuildRequires:	giflib-devel
BuildRequires:	glib-devel >= 1.2
%{!?with_gtk2:BuildRequires:	gtk+-devel >= 1.2}
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2.0}
BuildRequires:	imlib-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtar-devel
BuildRequires:	libtiff-devel
BuildRequires:	libzip-devel
%{?with_gtk2:BuildRequires:	pkgconfig}
BuildRequires:	xar-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pname		endeavour2
%define		pkgconfdir	/etc/%{pname}
%define		pkglibdir	%{_libdir}/%{pname}
%define		pkgdatadir	%{_libdir}/%{pname}

%description
Endeavour Mark II is a complete file management suite that comes with
a file browser, image browser, archiver, recycled objects system, and
a set of file and disk management utility programs.

%description -l pl.UTF-8
Endeavour Mark II to kompletne oprogramowanie do zarządzania plikami,
zawierające przeglądarkę plików, przeglądarkę obrazów, archiwizer,
system recyklingu oraz zbiór programów narzędziowych do zarządzania
plikami i dyskami.

%package libs
Summary:	Endeavour2 base library
Summary(pl.UTF-8):	Bibloteka podstawowa Endeavour2
Group:		Libraries

%description libs
Endeavour2 base library.

%description libs -l pl.UTF-8
Biblioteka podstawowa Endeavour2.

%package devel
Summary:	Header files for endeavour2
Summary(pl.UTF-8):	Pliki nagłówkowe endeavour2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib-devel >= 1.2
Requires:	libstdc++-devel

%description devel
Endeavour2 header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe Endeavour2.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%if %{with polish}
%patch6 -p1
%endif

%build
./configure \
	Linux

%{__make} \
	CC="%{__cc}"			\
	CPP="%{__cxx}"			\
	OPTCFLAGS="%{rpmcflags} -fPIC"	\
	EDV_BIN_DIR=%{pkglibdir}/bin    \
	EDV_LIB_DIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{pkgconfdir}

%{__make} -j1 install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	EDV_ARCH_DIR=$RPM_BUILD_ROOT%{pkglibdir} \
	EDV_ARCHDEP_DIR=$RPM_BUILD_ROOT%{pkglibdir} \
	EDV_BIN_DIR=$RPM_BUILD_ROOT%{pkglibdir}/bin \
	EDV_LIB_DIR=$RPM_BUILD_ROOT%{_libdir} \
	LIB_DIR=$RPM_BUILD_ROOT%{_libdir} \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	MAN1_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	MAN3_DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
	ICONS_DIR=$RPM_BUILD_ROOT%{_pixmapsdir} \
	INSTBINFLAGS="-m755" \
	INSTLIBFLAGS="-m755" \
	LDCONFIG=:
	
bzip2 -d $RPM_BUILD_ROOT%{_mandir}/man1/*.bz2

# mime types by abram@
install %{SOURCE2} $RPM_BUILD_ROOT%{pkgconfdir}/mimetypes.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING TODO LANGUAGE README
%attr(755,root,root) %{_bindir}/endeavour2
%dir %{pkglibdir}
%dir %{pkglibdir}/bin
%attr(755,root,root) %{pkglibdir}/bin/*
%{_datadir}/%{pname}
%dir %{pkgconfdir}
%config(noreplace) %verify(not md5 mtime size) %{pkgconfdir}/mimetypes.ini
%{_pixmapsdir}/endeavour2*.xpm
%{_mandir}/man1/endeavour2.1*
%{_mandir}/man1/hedit.1*
%{_mandir}/man1/sysinfo.endeavour2.1*
%{_mandir}/man1/tedit.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libendeavour2-base.so

%files devel
%defattr(644,root,root,755)
%doc endeavour2/libendeavour2-base/INTERPS
%attr(755,root,root) %{_bindir}/endeavour2-base-config
%{_includedir}/%{pname}
%{_mandir}/man1/endeavour2-base-config.1*
