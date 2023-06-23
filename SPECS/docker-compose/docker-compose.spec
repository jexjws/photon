%global debug_package %{nil}

Name:           docker-compose
Version:        2.19.0
Release:        1%{?dist}
Summary:        Multi-container orchestration for Docker
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=a75ae0311a7aa78aed6cde3885452eb2e94842a3ff8a1c9a829b880fbc9cc84db94ec902ab06611589f2b129a52663cad27166e4fe33db809bd3eb52df441ac2

BuildRequires:  go
BuildRequires:  ca-certificates

%description
Docker Compose (V2) plugin for the Docker CLI.

This plugin provides the 'docker compose' subcommand.

The binary can also be run standalone as a direct replacement for
Docker Compose V1 ('docker-compose').

%prep
%autosetup -p1 -n compose-%{version}

%build
make VERSION=%{version} build %{?_smp_mflags}

%install
install -D -p -m 0755 bin/build/docker-compose %{buildroot}%{_bindir}/docker-compose
for f in LICENSE MAINTAINERS NOTICE README.md; do
    install -D -p -m 0644 "$f" "docker-compose-docs/$f"
done

%if 0%{?with_check}
%check
ver="$(%{buildroot}%{_bindir}/docker-compose docker-cli-plugin-metadata | awk '{ gsub(/[",:]/,"")}; $1 == "Version" { print $2 }')"; \
    test "$ver" = %{version} && echo "PASS: docker-compose version OK" || (echo "FAIL: docker-compose version ($ver) did not match" && exit 1)
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docker-compose-docs/*
%{_bindir}/*

%changelog
* Fri Jun 23 2023 Piyush Gupta <gpiyush@vmware.com> 2.19.0-1
- Upgrade to v2.19.0.
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-6
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-5
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-4
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-2
- Bump up version to compile with new go
* Mon Sep 19 2022 Mukul Sikka <msikka@vmware.com> 2.11.0-1
- Initial Build
