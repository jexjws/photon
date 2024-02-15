Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python3-urllib3
Version:        1.25.11
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/urllib3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/shazow/urllib3/archive/urllib3-%{version}.tar.gz
%define sha512  urllib3=58f77edb9ced62cbac7b0baf2651c07f9f413267f103730ee25f08c5d4d0bf52a2ace02f58841bcd55652db677c7a1dc9a756681e7e32d590bc69d8b93e8f173

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pip

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch
Patch0:         CVE-2023-43804.patch
Patch1:         CVE-2023-45803.patch
Provides:       python%{python3_version}dist(urllib3)

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python.
Much of the Python ecosystem already uses urllib3 and you should too.

%prep
%autosetup -p1 -n urllib3-%{version}
# Dummyserver tests are failing when running in chroot. So disabling the tests.
rm -rf test/with_dummyserver/

%build
%py3_build

%install
%py3_install

%check
nofiles=$(ulimit -n)
ulimit -n 5000
pip3 install -r dev-requirements.txt
ignoretestslist='not test_select_interrupt_exception and not test_selector_error and not timeout and not test_request_host_header_ignores_fqdn_dot and not test_dotted_fqdn'
case $(uname -m) in
ppc*)

ignoretestslist="$ignoretestslist and not test_select_timing and not test_select_multiple_interrupts_with_event and not test_interrupt_wait_for_read_with_event and not test_select_interrupt_with_event";;
esac

PYTHONPATH="%{buildroot}%{$python3_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test
ulimit -n $nofiles

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Feb 15 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.25.11-5
- Fix CVE-2023-45803
* Mon Nov 20 2023 Mukul Sikka <msikka@vmware.com> 1.25.11-4
- Fix CVE-2023-43804
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.25.11-3
- Update release to compile with python 3.11
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.25.11-2
- Added provides
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.25.11-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.25.10-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.25.10-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.23-3
- Mass removal python2
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.23-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.23-1
- Update to version 1.23
* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-5
- Increased number of open files per process to 5000 before run make check.
* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-4
- Fixed rpm check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.20-2
- Use python2 explicitly
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-1
- Initial packaging for Photon
