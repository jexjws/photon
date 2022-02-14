%define debug_package %{nil}
%define __os_install_post %{nil}
%define gopath_comp github.com/containerd/containerd
Summary:        Containerd
Name:           containerd
Version:        1.4.12
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1    containerd=23b7126e50df745e4b0b4b935dd1fab72d6fb4fa
Source1:        containerd.service
Source2:        containerd-config.toml
Source3:        disable-containerd-by-default.preset

BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  go >= 1.10.7
BuildRequires:  go-md2man
BuildRequires:  systemd-devel

Requires:       libseccomp
Requires:       systemd
# containerd 1.4.5 and above allow to use runc 1.0.0-rc94 and above.
Requires:       runc >= 1.0.0-rc94

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
Requires:       %{name} = %{version}

%description    doc
Documentation for containerd.

%prep
%autosetup -p1 -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
go mod init
make %{?_smp_mflags} VERSION=%{version} binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} %{SOURCE1}
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
make %{?_smp_mflags} test
make %{?_smp_mflags} root-test
make %{?_smp_mflags} integration

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
*   Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.4.12-1
-   Upgrading to 1.4.12 to use latest runc.
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
-   Bump up version to compile with new go
*   Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Update to 1.4.4
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.4.1-4
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.1-3
-   Bump up version to compile with new go
*   Wed Oct 07 2020 Tapas Kundu <tkundu@vmware.com> 1.4.1-2
-   Use latest runc
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-   Automatic Version Bump
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.