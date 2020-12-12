Summary:	LASzip - free and lossless LiDAR compression
Summary(pl.UTF-8):	LASzip - wolnodostępna, bezstratna kompresja danych LiDARowych
Name:		laszip
Version:	3.4.3
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://laszip.org/
Source0:	https://github.com/LASzip/LASzip/releases/download/%{version}/%{name}-src-%{version}.tar.gz
# Source0-md5:	e07be9ba6247889a4ba0bda8535c77e3
Patch0:		%{name}-link.patch
# from Fedora: restore old API for libLAS, related to https://github.com/libLAS/libLAS/issues/144
Patch1:		%{name}-restoreapi.patch
Patch2:		%{name}-example.patch
URL:		https://laszip.org/
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LASzip - a free open source product of rapidlasso GmbH - quickly turns
bulky LAS files into compact LAZ files without information loss.

%description -l pl.UTF-8
LASzip - darmowy, mający otwarty kod źródłowy produk rapidlasso GmbH -
szybko przekształca masywne pliki LAS w kompaktowe pliki LAZ bez
utraty informacji.

%package devel
Summary:	Header files for LASzip library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LASzip
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for LASzip library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LASzip.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build/example
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# omitted by install
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -p build/example/laszip.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__rm} $RPM_BUILD_ROOT%{_bindir}/laszippertest

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.txt ChangeLog NEWS README.rst
%attr(755,root,root) %{_libdir}/liblaszip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblaszip.so.8
%attr(755,root,root) %{_libdir}/liblaszip_api.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblaszip_api.so.8

%files devel
%defattr(644,root,root,755)
%doc design/*.rst
%attr(755,root,root) %{_bindir}/laszip-config
%attr(755,root,root) %{_libdir}/liblaszip.so
%attr(755,root,root) %{_libdir}/liblaszip_api.so
%{_includedir}/laszip
%{_pkgconfigdir}/laszip.pc
