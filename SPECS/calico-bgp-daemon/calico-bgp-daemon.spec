Summary:       GoBGP based Calico BGP Daemon
Name:          calico-bgp-daemon
Version:       0.2.2
Release:       16%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/calico-bgp-daemon
Distribution:  Photon

Source0:       %{name}-%{version}.tar.gz
%define sha1 calico-bgp-daemon=d823d92d1bbb887ea885080ab2b989a75e3a338d

BuildRequires: git
BuildRequires: glide
BuildRequires: go >= 1.7

%define debug_package %{nil}

%description
GoBGP based Calico BGP Daemon, an alternative to BIRD in calico/node.

%prep
%autosetup -p1

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
cp -r * ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/.
pushd ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon
mkdir -p dist
glide install --strip-vendor
GO111MODULE=auto go build -v -o dist/calico-bgp-daemon -ldflags "-X main.VERSION=%{version} -s -w" main.go ipam.go

%install
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/projectcalico/calico-bgp-daemon/dist/calico-bgp-daemon %{buildroot}%{_bindir}/

#%%check
# No tests available for this pkg

%files
%defattr(-,root,root)
%{_bindir}/calico-bgp-daemon

%changelog
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-16
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-15
-   Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.2-14
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-13
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-12
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.2-11
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.2-10
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.2.2-9
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.2.2-8
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.2.2-7
- Bump up version to compile with new go
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 0.2.2-6
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.2.2-5
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.2.2-4
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.2.2-3
- Bump up version to compile with new go
* Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.2-2
- gobgp comes from the Go BGP package.
* Thu Aug 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.2-1
- Calico BGP daemon for PhotonOS.
