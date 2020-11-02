Name:          crash
Version:       7.2.8
Release:       3%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:	       VMware, Inc.
Distribution:  Photon
URL:           http://people.redhat.com/anderson/
Source0:       http://people.redhat.com/anderson/crash-%{version}.tar.gz
%define sha1 crash=334bce71a69ccf8abefaf8c4bc5eec67c9b43c9e
%define GCORE_VERSION	1.5.1
Source1:       http://people.redhat.com/anderson/extensions/crash-gcore-command-%{GCORE_VERSION}.tar.gz
%define sha1 crash-gcore=9c542d8503824e5f16d00c47bfdb38a7481ed752
Source2:       https://ftp.gnu.org/gnu/gdb/gdb-7.6.tar.gz
%define sha1 gdb=026f4c9e1c8152a2773354551c523acd32d7f00e
Source3:       gcore_defs.patch
Source4:       CVE-2017-7226.patch
Patch0:        vmware_guestdump-new-input-format.patch
Patch1:        apply-patch-to-nested-gdb.patch

License:       GPL
BuildRequires: binutils
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
Requires:      binutils
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

This package contains libraries and header files need for development.

%prep
%setup -q -n %{name}-%{version}
%setup -a 1
%patch0 -p1
%patch1 -p1

%build
sed -i "s/tar --exclude-from/tar --no-same-owner --exclude-from/" Makefile
cp %{SOURCE2} .
cp %{SOURCE4} .
make GDB=gdb-7.6 RPMPKG=%{version}-%{release}
cd crash-gcore-command-%{GCORE_VERSION}
%ifarch x86_64
make -f gcore.mk ARCH=SUPPORTED TARGET=X86_64
%endif
%ifarch aarch64
patch -p1 < %{SOURCE3}
make -f gcore.mk ARCH=SUPPORTED TARGET=ARM64
%endif

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
mkdir -p %{buildroot}%{_bindir}
%make_install
mkdir -p %{buildroot}%{_mandir}/man8
install -pm 644 crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash
mkdir -p %{buildroot}%{_libdir}/crash
install -pm 755 crash-gcore-command-%{GCORE_VERSION}/gcore.so %{buildroot}%{_libdir}/crash/

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%{_bindir}/crash
%{_libdir}/crash/gcore.so
%{_mandir}/man8/crash.8.gz
%doc COPYING3 README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%changelog
*   Mon Nov 02 2020 Ajay Kaher <akaher@vmware.com> 7.2.8-3
-   Fix for CVE-2017-7226
*   Thu Sep 24 2020 Alexey Makhalov <amakhalov@vmware.com> 7.2.8-2
-   debug.guest (debug.vmem) support
*   Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 7.2.8-1
-   Version update
*   Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 7.2.3-1
-   Upgrading to version 7.2.3
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-2
-   Aarch64 support
*   Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-1
-   Update version to 7.1.8 (it supports linux-4.9)
-   Disable a patch - it requires a verification.
*   Fri Oct 07 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-2
-   gcore-support-linux-4.4.patch
*   Fri Sep 30 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-1
-   Update version to 7.1.5 (it supports linux-4.4)
-   Added gcore plugin
-   Remove zlib-devel requirement from -devel subpackage
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1.4-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1.4-1
-   Updated to version 7.1.4
*   Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 7.1.3-1
-   Initial build. First version
