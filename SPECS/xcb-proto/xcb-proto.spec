%global debug_package %{nil}
Summary:        provides the XML-XCB protocol descriptions.
Name:           xcb-proto
Version:        1.15.2
Release:        1%{?dist}
License:        MIT
URL:            http://xcb.freedesktop.org/
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.gz
%define sha512  xcb-proto=4aaf4886dbbb465ec9d123beca2db616f4690f76297df7f85a2cb6afeea114e7ee08995268821b090226a55109c93676f134840065b448180a5d61d8d95095b0

BuildRequires:  python3-devel
Requires:       python3
Requires:       pkg-config

%description
The xcb-proto package provides the XML-XCB protocol descriptions that libxcb uses to generate the majority of its code and API.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_datadir}/xcb
%{_datadir}/pkgconfig

%changelog
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 1.15.2-1
- initial version
