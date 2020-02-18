# add --with checks option (default is enable non strict checks)
%bcond_with checks

# The default behavior of rpmbuild, depending on your OS, often is to strip
# binaries after installation in order to reduce file size. The two macros
# defined below override that behavior and compresses the man and info pages
# for debugging purposes. For more information:
# https://www.redhat.com/archives/rpm-list/2001-November/msg00257.html
%define __os_install_post /usr/lib/rpm/brp-compress
%define debug_package %{nil}

# Default give dir is /usr/give, unless the user overrides it
%{!?give_dir: %define give_dir /usr/give}

Name: give
Version: 3.1
Release: 5
Summary: lc file transfer utility
License: LLNL Internal
Group: System Environment/Base
Source0: https://github.com/hpc/%{name}/archive/v%{version}-%{release}.tar.gz
URL: https://github.com/hpc/%{name}


######################################################################
%prep
%setup -n %{name}-%{version}-%{release}

%build
%if %{with checks}
    %configure --enable-givedir=%{give_dir}
    %define local_options Built with strict checks
    make
%else
    %configure --enable-non-strict-checks --enable-givedir=%{give_dir}
    %define local_options Built with non-strict checks (default)
    make
%endif

%description
Give and take are a set of companion utilities that allow a 
secure transfer of files from one user to another without 
exposing the files to third parties.  
%local_options

%install
rm -rf "$RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install give-assist $RPM_BUILD_ROOT%{_bindir}
install give.py $RPM_BUILD_ROOT%{_bindir}/give
install -m 644 give.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln $RPM_BUILD_ROOT%{_bindir}/give $RPM_BUILD_ROOT%{_bindir}/take
install -m 644 take.1 $RPM_BUILD_ROOT%{_mandir}/man1
# # # This step fails on the Crays, and appears to be redundant. Skip it.
# # # DESTDIR="$RPM_BUILD_ROOT"%makeinstall

#######################################################################

%clean
rm -rf $RPM_BUILD_ROOT


#######################################################################
%post

%files
%defattr(-,root,root,0755)
%attr(4555,root,root)%{_bindir}/give-assist
%{_bindir}/give
%{_bindir}/take
%{_mandir}/man1/*
	

%changelog
 * Tue Aug 14 2012 Dominic Manno <dmanno@lanl.gov>
- Original; LANL version to add alt-givedir and no-strict-checking options
 * Thu Nov 01 2012 Georgia Pedicini <gap@lanl.gov>
- LANL version 3.1-2, tighten permissions
 * Tue Nov 06 2012 Georgia Pedicini <gap@lanl.gov>
- Added defined text string to include in description, citing which (if any)
options were used in the build.
 * Wed May 25 2016 Dominic Manno <dmanno@lanl.gov>
- Converted to be python2 and python3 compatible, mostly print statement to
function calls
