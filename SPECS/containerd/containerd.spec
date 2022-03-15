%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Containerd
Name:           containerd
Version:        1.4.12
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1    containerd=23b7126e50df745e4b0b4b935dd1fab72d6fb4fa
# Must be in sync with package version
%define CONTAINERD_GITCOMMIT 7b11cfaabd73bb80907dd23182b9347b4245eb5d

Patch1:         containerd-service-file-binpath.patch
Patch2:         containerd-1.4-Use-fs.RootPath-when-mounting-volumes.patch
Source2:        containerd-config.toml
Source3:        disable-containerd-by-default.preset
%define gopath_comp github.com/containerd/containerd

BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
# Upstream is unhappy with 1.14. 1.13 or 1.15+ is OK
BuildRequires:  go >= 1.16
BuildRequires:  go-md2man
BuildRequires:  systemd-devel
Requires:       libseccomp
Requires:       systemd
# containerd 1.4.5 and above allow to use runc 1.0.0-rc94 and above.
# refer to v1.4.5/RUNC.md
Requires:       runc >= 1.0.0.rc94

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        extras
Summary:        Extra binaries for containerd
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description    extras
Extra binaries for containerd

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation for containerd.

%prep
# Using autosetup is not feasible
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
%patch1 -p1 -d %{name}-%{version}
%patch2 -p1 -d %{name}-%{version}
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
export GO111MODULE=auto
cd src/%{gopath_comp}
make %{?_smp_mflags} VERSION=%{version} REVISION=%{CONTAINERD_GITCOMMIT} binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} containerd.service
install -v -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml
install -v -m644 -D %{SOURCE3} %{buildroot}%{_presetdir}/50-containerd.preset
make %{?_smp_mflags} DESTDIR=%{buildroot}%{_prefix} install
make %{?_smp_mflags} DESTDIR=%{buildroot}%{_datadir} install-man

%post
%systemd_post containerd.service

%postun
%systemd_postun_with_restart containerd.service

%preun
%systemd_preun containerd.service

%check
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make test %{?_smp_mflags}
make root-test %{?_smp_mflags}
make integration %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/ctr
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_datadir}/licenses/%{name}
%{_unitdir}/containerd.service
%{_presetdir}/50-containerd.preset
%config(noreplace) %{_sysconfdir}/containerd/config.toml

%files extras
%defattr(-,root,root)
%{_bindir}/containerd-shim-runc-v1
%{_bindir}/containerd-shim-runc-v2
%{_bindir}/containerd-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.12-2
-   Bump up version to compile with new go
*   Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.4.12-1
-   Update to 1.4.12 and fix CVE-2022-23648
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.4-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.4-9
-   Bump up version to compile with new go
*   Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-7
-   Bump up version to compile with new go
*   Fri Oct 01 2021 Bo Gan <ganb@vmware.com> 1.4.4-6
-   Fix CVE-2021-41103
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-5
-   Bump up version to compile with new go
*   Tue Jul 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-4
-   Bump up version to compile with new go.
*   Fri Jul 16 2021 Bo Gan <ganb@vmware.com> 1.4.4-3
-   Fix CVE-2021-32760
*   Tue May 18 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
-   Bump up version to compile with new go
*   Wed May 05 2021 Bo Gan <ganb@vmware.com> 1.4.4-1
-   Update to 1.4.4
*   Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.3.10-1
-   Update to 1.3.10 to fix CVE-2021-21334
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.3.9-3
-   Bump up version to compile with new go
*   Tue Dec 1 2020 HarinadhD <hdommaraju@vmware.com> 1.3.9-2
-   Bump up version to compile with new go
*   Mon Nov 30 2020 Bo Gan <ganb@vmware.com> 1.3.9-1
-   Update to 1.3.9 for upstream fix of CVE-2020-15257
*   Fri Nov 20 2020 Ankit Jain <ankitja@vmware.com> 1.3.7-1
-   Update to 1.3.7 to fix CVE-2020-15257
*   Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 1.2.14-1
-   Update to 1.2.14 to fix CVE-2020-15157
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-3
-   enable critical restart
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.10-2
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 1.2.10-1
-   Bump up version to 1.2.10 and cleanups
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.8-2
-   Bump up version to compile with go 1.13.3
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.
