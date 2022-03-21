%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        0.7.1
Release:        18%{?dist}
License:        Apache-2.0
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:	edgex-0.7.1.tar.gz
%define sha1 edgex=abeb109c0a1519af6c2193f02bfcb04478879cd8
# glide installed dependencies all in one tarball generated by:
# tar -cJf glide-tarball-for-edgex-0.6.0-1261522.tar.xz vendor/ glide.lock
Source1:	glide-tarball-for-edgex-0.7.1.tar.xz
%define sha1 glide-tarball-for-edgex=157f9383bba5d38c8a83c5f52cafba8ff15243d9
Source2:	edgex-template.service

BuildRequires:  go >= 1.9
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  zeromq-devel
Requires:       systemd
Requires:       consul
Requires:       redis

%description
EdgeX Foundry Go Services:
- config-seed
- core-command
- core-data
- core-metadata
- export-client
- export-distro
- support-logging
- support-notifications
- support-scheduler
- sys-mgmt-agent

%prep
%autosetup -c -T -a 0 -n src/github.com/edgexfoundry
mv %{_builddir}/src/github.com/edgexfoundry/edgex-go-%{version} %{_builddir}/src/github.com/edgexfoundry/edgex-go
%autosetup -D -c -T -a 1 -n src/github.com/edgexfoundry/edgex-go

%build
export GO111MODULE=auto
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go
# patch influxdb go get path
sed -i 's#influxdata/influxdb/client/v2#influxdata/influxdb1-client/v2#' internal/export/distro/influxdb.go

# modify configuration
sed -i 's#./logs/#/var/log/edgex/#' cmd/config-seed/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/core-command/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/core-data/res/configuration.toml
sed -i 's#Port = 27017#Port = 6379#' cmd/core-data/res/configuration.toml
sed -i "s#Type = 'mongodb'#Type = 'redisdb'#" cmd/core-data/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/core-metadata/res/configuration.toml
sed -i 's#Port = 27017#Port = 6379#' cmd/core-metadata/res/configuration.toml
sed -i "s#Type = 'mongodb'#Type = 'redisdb'#" cmd/core-metadata/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/export-client/res/configuration.toml
sed -i 's#Port = 27017#Port = 6379#' cmd/export-client/res/configuration.toml
sed -i "s#Type = 'mongodb'#Type = 'redisdb'#" cmd/export-client/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/export-distro/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/support-logging/res/configuration.toml
sed -i 's#Port = 27017#Port = 6379#' cmd/support-logging/res/configuration.toml
sed -i "s#Type = 'mongodb'#Type = 'redisdb'#" cmd/support-logging/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/support-notifications/res/configuration.toml
sed -i 's#Port = 27017#Port = 6379#' cmd/support-notifications/res/configuration.toml
sed -i "s#Type = 'mongodb'#Type = 'redisdb'#" cmd/support-notifications/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/support-scheduler/res/configuration.toml

sed -i 's#./logs/#/var/log/edgex/#' cmd/sys-mgmt-agent/res/configuration.toml
sed -i "s#OperationsType = 'docker'#OperationsType = 'os'#" cmd/sys-mgmt-agent/res/configuration.toml

GOPATH=%{_builddir} make build %{?_smp_mflags}

%install
# edgex-go
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_var}/log/%{name}
install -d -m755 %{buildroot}%{_libdir}/systemd/system

# install binary
for srv in config-seed core-command core-data core-metadata export-client export-distro support-logging support-notifications support-scheduler sys-mgmt-agent; do
install -p -m755 cmd/${srv}/${srv} %{buildroot}%{_bindir}/edgex-${srv}
install -d -m755 %{buildroot}%{_datadir}/%{name}/${srv}/res
install -p -m644 cmd/${srv}/res/configuration.toml %{buildroot}%{_datadir}/%{name}/${srv}/res/configuration.toml
sed "s/SERVICE_NAME/${srv}/" %{SOURCE2} > %{buildroot}%{_libdir}/systemd/system/edgex-${srv}.service
done

# config-seed extras
cp -a cmd/config-seed/res/properties %{buildroot}%{_datadir}/%{name}/config-seed/config

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*
%{_var}/log/*

%changelog
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.7.1-18
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.7.1-17
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.7.1-16
-   Bump up version to compile with new go
*   Wed Dec 22 2021 Nitesh Kumar <kunitesh@vmware.com> 0.7.1-15
-   Bump up to use consul 1.8.17
*   Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.7.1-14
-   Bump up version to compile with new go
*   Wed Oct 27 2021 Piyush Gupta <gpiyush@vmware.com> 0.7.1-13
-   Bump up version to compile with new go
*   Tue Oct 26 2021 Nitesh Kumar <kunitesh@vmware.com> 0.7.1-12
-   Bump up to use redis v6.0.16.
*   Thu Sep 30 2021 Shreyas B. <shreyasb@vmware.com> 0.7.1-11
-   Bump up to use redis v6.0.15
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.7.1-10
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.7.1-9
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.7.1-8
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.7.1-7
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.7.1-6
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 0.7.1-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.7.1-4
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.7.1-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.7.1-2
-   Bump up version to compile with new go
*   Wed Jan 16 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-1
-   Version update. Use redis db.
*   Wed Dec 05 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-2
-   Remove 'Requires: mongodb'. But edgex still depends on mongo.
*   Fri Jul 06 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-1
-   Initial version