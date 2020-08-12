Name:    lksctp-tools
Summary: User-space access to Linux Kernel SCTP
Version: 1.0.18
Release: 1
# src/apps/bindx_test.C is GPLv2, I've asked upstream for clarification
License: GPLv2 and GPLv2+ and LGPLv2 and MIT
URL:     http://lksctp.sourceforge.net

Source0: %{name}-%{version}.tar.gz
Patch0: lksctp-tools-1.0.16-libdir.patch
Patch1: lksctp-tools-1.0.18-withsctp-use-PACKAGE_VERSION-in-withsctp.h.patch
Patch2: lksctp-tools-1.0.18-configure.ac-add-CURRENT-REVISION-and-AGE-for-libsct.patch
Patch3: lksctp-tools-1.0.18-build-fix-netinet-sctp.h-not-to-be-installed.patch
Patch4: lksctp-tools-1.0.18-build-remove-v4.12-secondary-defines-in-favor-of-HAV.patch
Patch5: lksctp-tools-1.0.18-build-fix-probing-for-HAVE_SCTP_SENDV.patch
Patch6: lksctp-tools-1.0.18-build-0b0dce7a36fb-actually-belongs-to-v4.19.patch
BuildRequires: libtool, automake, autoconf

%description
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the base run-time library and command-line tools.

%package devel
Summary: Development files for lksctp-tools
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for lksctp-tools which include man pages, header files,
static libraries, symlinks to dynamic libraries and some tutorial source code.

%package doc
Summary: Documents pertaining to SCTP
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
Documents pertaining to LKSCTP & SCTP in general (IETF RFC's & Internet
Drafts).

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

[ ! -x ./configure ] && sh bootstrap
%configure --disable-static
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
rm -f doc/rfc2960.txt doc/states.txt
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING* README
%{_bindir}/*
%{_libdir}/libsctp.so.1*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.1*
%{_mandir}/man7/*

%files devel
%{_includedir}/*
%{_libdir}/libsctp.so
%{_libdir}/pkgconfig/libsctp.pc
%{_libdir}/lksctp-tools/libwithsctp.so
%{_datadir}/lksctp-tools/
%{_mandir}/man3/*

%files doc
%doc doc/*.txt
