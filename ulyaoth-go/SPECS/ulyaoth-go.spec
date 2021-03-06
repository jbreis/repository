AutoReqProv: no
%define debug_package %{nil}
%global __os_install_post %{nil}

Summary: The Go Programming Language
Name: ulyaoth-go
Version: 1.8.1
Release: 1%{?dist}
BuildArch: x86_64
URL: https://golang.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: https://storage.googleapis.com/golang/go1.8.1.linux-amd64.tar.gz
BuildRoot:  %{_tmppath}/ulyaoth-golang-1.8-%{release}-root-%(%{__id_u} -n)

License: BSD

Provides: ulyaoth-go

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
%setup -q -n go

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/local/ulyaoth
cp -rf %{_builddir}/go $RPM_BUILD_ROOT/usr/local/ulyaoth

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth/go
/usr/local/ulyaoth/go/*

%post
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-go!

Please find the official documentation for go here:
* https://golang.org/

For any additional information or help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

%changelog
* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.8.1-1
- Updated to Go 1.8.1.

* Sun Feb 19 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.8.0-1
- Updated to Go 1.8.0.

* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.5-1
- Updated to Go 1.7.5.

* Sat Dec 3 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.4-1
- Updated to Go 1.7.4.

* Sat Oct 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.3-1
- Updated to Go 1.7.3.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.1-1
- Updated to Go 1.7.1.

* Sat Aug 20 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.7.0-1
- Updated to Go 1.7.0.

* Tue Jul 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.3-1
- Updated to Go 1.6.3.

* Sat Apr 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.2-1
- Updated to Go 1.6.2.

* Thu Apr 14 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.1-1
- Updated to Go 1.6.1.

* Sat Feb 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.6.0-1
- Updated to Go 1.6.0.

* Sat Jan 30 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.5.3-1
- Creating initial release with Go 1.5.3.