Summary:        Modern asynchronous API to the DNS
Name:           getdns
Version:        1.7.0
Release:        1%{?dist}
License:        BSD
Url:            http://www.getdnsapi.net
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.getdnsapi.net/dist/%{name}-%{version}.tar.gz
%define sha512  %{name}=d09b8bdd0b4a3df2d25b9689166226da83a5a7eb2c7436487dc637539ac6077624a4d66cf684c4e6c4911561872c6bd191af3afd90d275b1662e4c6c47773ef6

BuildRequires:  cmake
BuildRequires:  check
BuildRequires:  libev-devel
BuildRequires:  libuv-devel
BuildRequires:  glibc-devel
BuildRequires:  openssl-devel

Requires:       openssl
Requires:       glibc
Requires:       libev
Requires:       libuv

%description
getdns is a modern asynchronous DNS API. It implements DNS entry points
from a design developed and vetted by application developers, in an API
specification edited by Paul Hoffman. With the development of this API,
we intend to offer application developers a modernized and flexible way
to access DNS security (DNSSEC) and other powerful new DNS features; a
particular hope is to inspire application developers towards innovative
security solutions in their applications.

%package devel
Summary: Development package that includes getdns header files
Requires: %{name} = %{version}-%{release}

%description devel
The devel package contains the getdns library and the include files and
some example C code.

%package utils
Summary: getdns utilities
Requires: %{name} = %{version}-%{release}

%description utils
The %{name}-utils package contains utilities using getdns library,
getdns_query and getdns_query_mon utilities. They can be used to analyze
responses from DNS servers over UDP, TCP and TLS, including support for
DNS security.

getdns_query can be used for fetching details of DNS responses in json format.
getdns_query_mon is great for automated monitoring of DNS server replies.

%prep
%autosetup -p1

%build
%cmake -DUSE_LIBIDN2=OFF -DENABLE_STUB_ONLY=ON

cmake --build .

%if 0%{?with_check}
%check
# make test needs a network connection - so disabled per default
#make test %{?_smp_mflags}
%endif

%install
DESTDIR=%{buildroot} cmake --install .

rm -rf %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_docdir}/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libgetdns*.a
%{_libdir}/libgetdns*.so*
%doc README.md NEWS AUTHORS ChangeLog
%license LICENSE

%files utils
%defattr(-,root,root)
%{_bindir}/getdns_query
%{_bindir}/getdns_server_mon

%files devel
%defattr(-,root,root)
%{_includedir}/getdns/
%{_libdir}/pkgconfig/*.pc
%{_mandir}/*/*.3*
%doc spec

%changelog
* Mon Apr 11 2022 Mukul Sikka <msikka@vmware.com> 1.7.0-1
- Initial Build