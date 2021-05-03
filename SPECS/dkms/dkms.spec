Summary:        Dynamic Kernel Module Support
Name:           dkms
Version:        2.8.4
Release:        1%{?dist}
License:        GPLv2+
URL:            http://linux.dell.com/dkms
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/dell/dkms/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=1b8b987b239db8cf00f367ee4f5faf13dc41b450f09fb046dc719e51d6a762d6b700bf41156d8011c3ea7e139064119d6717b60c1bf7fa0a75ea1fc63887baa5

Patch0:         0001-dkms-for-photon-os.patch

BuildArch:      noarch

BuildRequires:  systemd-devel

Requires:       systemd
Requires:       build-essential

%description
Dynamic Kernel Module Support (DKMS) is a program/framework that enables generating Linux kernel modules whose sources generally reside outside the kernel source tree.
The concept is to have DKMS modules automatically rebuilt when a new kernel is installed.

%prep
%autosetup -p1

%build

%install
%make_install %{?_smp_mflags} install-redhat-systemd
install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_datadir}/bash-completion/completions/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/framework.conf
%{_sysconfdir}/%{name}/template-%{name}-mkrpm.spec
%{_sysconfdir}/%{name}/template-%{name}-redhat-kmod.spec
%{_sysconfdir}/%{name}/kernel_install.d_dkms
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/%{name}/sign_helper.sh
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_libdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%{_sharedstatedir}/%{name}/dkms_dbversion

%changelog
*   Thu Sep 07 2023 Alexey Makhalov <amakhalov@vmware.com> 2.8.4-1
-   Version Bump
*   Mon Jan 18 2021 Ajay Kaher <akaher@vmware.com> 2.8.2-2
-   Modified Requires list.
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.2-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.6.1-1
-   Upgraded to version 2.6.1
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.2.0.3-4
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.0.3-3
-   GA - Bump release of all rpms
*   Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 2.2.0.3-2
-   Added systemd preset file with 'disable' default value.
-   Set BuildArch to noarch.
*   Thu Aug 6 2015 Divya Thaluru <dthaluru@vmware.com> 2.2.0.3-1
-   Initial version
