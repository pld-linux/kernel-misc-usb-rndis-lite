#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.1
Summary:	Linux kernel drivers for USB RNDIS
Summary(pl.UTF-8):	Sterowniki jądra Linuksa do USB RNDIS
Name:		kernel%{_alt_kernel}-misc-usb-rndis-lite
Version:	0.11
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/synce/usb-rndis-lite-%{version}.tar.gz
# Source0-md5:	78c5b4900d2ebd54d957f03c53ab864d
URL:		http://www.synce.org/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux kernel drivers for:
- USB Host side RNDIS
- USB network driver framework
- USB CDC Ethernet devices

%description -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa do:
- RNDIS po stronie hosta USB
- szkieletu sterowników sieciowych USB
- urzędzeń ethernetowych USB CDC

%prep
%setup -q -n usb-rndis-lite-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m cdc_ether,rndis_host,usbnet \
	EXTRA_CFLAGS="%{?debug:-DDEBUG=1 -DVERBOSE=1}"
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

%if %{with kernel}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*
%endif
