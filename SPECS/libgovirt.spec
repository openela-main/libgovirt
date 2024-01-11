# -*- rpm-spec -*-

%global with_gir 0

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.

# Force running autoreconf because data center patches touch Makefile.am.
# To disable autoreconf, change the value to 0.
%{!?enable_autotools:%global enable_autotools 1}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_gir 1
%endif

Summary: A GObject library for interacting with oVirt REST API
Name: libgovirt
Version: 0.3.7
Release: 4%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source0: http://ftp.gnome.org/pub/GNOME/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
Source1: http://ftp.gnome.org/pub/GNOME/sources/libgovirt/0.3/%{name}-%{version}.tar.xz.sig
Source2: etrunko-57E1C130.keyring
URL: https://gitlab.gnome.org/GNOME/libgovirt

Patch0001: 0001-Initial-support-for-Disks.patch
Patch0002: 0002-ovirt-storage-domain-Introduce-ovirt_storage_domain_.patch
Patch0003: 0003-ovirt-disk-Fix-content-type-property-name.patch
Patch0004: 0004-proxy-Fix-error-handling.patch

%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
%endif
BuildRequires: git-core

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: intltool
BuildRequires: rest-devel >= 0.7.92
%if %{with_gir}
BuildRequires: gobject-introspection-devel
%endif
#needed for make check
BuildRequires: glib-networking
BuildRequires: dconf
#needed for GPG signature checek
BuildRequires: gnupg2

%description
libgovirt is a library that allows applications to use oVirt REST API
to list VMs managed by an oVirt instance, and to get the connection
parameters needed to make a SPICE/VNC connection to them.

%package devel
Summary: Libraries, includes, etc. to compile with the libgovirt library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description devel
libgovirt is a library that allows applications to use oVirt REST API
to list VMs managed by an oVirt instance, and to get the connection
parameters needed to make a SPICE/VNC connection to them.

Libraries, includes, etc. to compile with the libgovirt library

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git_am

%build
%if 0%{?enable_autotools}
autoreconf -if
%endif

%if %{with_gir}
%global gir_arg --enable-introspection=yes
%else
%global gir_arg --enable-introspection=no
%endif

%configure %{gir_arg}
%__make %{?_smp_mflags} V=1

%install
%__make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
%find_lang %{name} --with-gnome

%check
make check

%ldconfig_scriptlets

%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS README
%{_libdir}/%{name}.so.2*
%if %{with_gir}
%{_libdir}/girepository-1.0/GoVirt-1.0.typelib
%endif

%files devel
%{_libdir}/%{name}.so
%dir %{_includedir}/govirt-1.0/
%dir %{_includedir}/govirt-1.0/govirt/
%{_includedir}/govirt-1.0/govirt/*.h
%{_libdir}/pkgconfig/govirt-1.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/GoVirt-1.0.gir
%endif

%changelog
* Tue Dec 22 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.7-4
- Fix error handling in ovirt-proxy.c
  Resolves: rhbz#1910033

* Tue Jun 16 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.7-3
- Fix content-type property name
  Resolves: rhbz#1847223

* Tue Jun 16 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.7-2
- Add support for storage domains 'disks' query
  Resolves: rhbz#1847223

* Fri May 08 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.7-1
- Rebase to latest upstream version
  Resolves: rhbz#1801226

* Mon Mar 16 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.4-11
- Bumped version and rebuild to trigger gating for 8.2.0.z properly
  Resolves: rhbz#1813962

* Mon Mar 16 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.4-10
- Update to RHV REST API version 4
  Resolves: rhbz#1813962

* Mon Aug 2 2019 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.4-9
- Sync with the rhel 7.7 package
  Related: rhbz#1717900

* Mon Jun 11 2018 Christophe Fergeau <cfergeau@redhat.com> - 0.3.4-8
- Sync with the rhel 7.6 package
  Resolves: rhbz#1584506

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.4-7
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.4-5
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 13 2016 Christophe Fergeau <cfergeau@redhat.com> 0.3.4-1
- Update to libgovirt 0.3.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Christophe Fergeau <cfergeau@redhat.com> 0.3.3-1
- Update to upstream release 0.3.3

* Thu Oct 09 2014 Christophe Fergeau <cfergeau@redhat.com> 0.3.2-1
- Update to upstream release 0.3.2

* Wed Sep 03 2014 Christophe Fergeau <cfergeau@redhat.com> 0.3.1-1
- Update to upstream release 0.3.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard Jones <rjones@redhat.com> - 0.3.0-6
- Force rebuild for aarch64.

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.3.0-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Christophe Fergeau <cfergeau@redhat.com> 0.3.0-3
- Actually apply Patch0 /o\

* Tue Nov 26 2013 Christophe Fergeau <cfergeau@redhat.com> 0.3.0-2
- Add patch to fix a memory corruption issue when librest does not have the
  RestProxy::ssl-ca-file property (which is currently the case in Fedora)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Christophe Fergeau <cfergeau@redhat.com> 0.1.0-1
- Update to upstream release 0.1.0

* Mon Mar 11 2013 Christophe Fergeau <cfergeau@redhat.com> 0.0.3-2
- Removed definition of BuildRoot and cleanup of BuildRoot in %%clean
- Added missing arch to versioned Requires: %%{name} in the -devel package
- Don't include empty NEWS and ChangeLog in built RPM

* Wed Feb 20 2013 Christophe Fergeau <cfergeau@redhat.com> 0.0.3-1
- Initial import of libgovirt 0.0.3


