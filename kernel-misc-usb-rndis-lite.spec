#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	0.1
Summary:	usb-rdnis-lite
Name:		kernel%{_alt_kernel}-misc-usb-rndis-lite
Version:	0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	usb-rndis-lite-20070124.2730.tar.bz2
# Source0-md5:	b84f029bb4f35003d4b60e671df37e46
URL:		http://www.synce.org/index.php/Connecting_your_Windows_Mobile_2005_device_via_USB_(usb-rndis-lite)
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux drivers for:
- USB Host side RNDIS driver
- USB network driver framework
- USB CDC Ethernet devices

%package -n kernel%{_alt_kernel}-smp-misc-usb-rndis-lite
Summary:	usb-rdnis-lite
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-misc-usb-rndis-lite
This package contains the Linux SMP drivers for:
- USB Host side RNDIS driver
- USB network driver framework
- USB CDC Ethernet devices

%prep
%setup -q -n usb-rndis-lite

%build
%if %{with kernel}
%build_kernel_modules -m cdc_ether,rndis_host,usbnet
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m cdc_ether,rndis_host,usbnet -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-misc-usb-rndis-lite
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-misc-usb-rndis-lite
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-usb-rndis-lite
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
