Summary:        A network performance benchmark tool.
Name:           iperf
Version:        3.14
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/esnet/iperf
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

#Source download URL: https://github.com/esnet/iperf/archive/%{version}.tar.gz
Source0:        https://github.com/esnet/iperf/archive/%{name}-%{version}.tar.gz
%define sha512 iperf=a90fbaddd73e5b721a84cee71cefb63391c13f64107f5785e954e7c44e9a8c5072e402b6fe45434966d3cc58ac97227c608ca9719161fc23459c5e5efcf8232b

Patch1:         disablepg.patch

BuildRequires:  autoconf
BuildRequires:  automake

%description
ipref is a network performance measurement tool that can measure the maximum
achievable network bandwidth on IP networks. It supports tuning of various
parameters related to timing, protocols, and buffers.  For each test it
reports the bandwidth, loss, and other parameters.

%package        doc
Summary:        Documentation for iperf
%description    doc
It contains the documentation and manpages for iperf package.
Requires:       %{name} = %{version}-%{release}

%prep
%autosetup -p1

%build
echo "VDBG optflags: " %{optflags}
./bootstrap.sh
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/iperf3
%{_includedir}/iperf_api.h
%{_libdir}/libiperf.*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/iperf3.1.gz
%{_mandir}/man3/libiperf.3.gz

%changelog
* Fri Aug 11 2023 Roye Eshed <eshedr@vmware.com> 3.14-1
- Update iperf version and absorb CVE-2023-38403 fix
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9-2
- Bump up release for openssl
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9-1
- Automatic Version Bump
* Mon Jun 22 2020 Ankit Jain <ankitja@vmware.com> 3.8.1-1
- Automatic Version Bump
* Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 3.6-1
- Upgraded to version 3.6
* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.7-1
- Upgraded to version 3.1.7
* Thu Oct 6 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.3-1
- Upgraded to version 3.1.3
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.1.2-1
- Upgrade to 3.1.2
* Wed Oct 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-1
- Add iperf v3.1 package.
