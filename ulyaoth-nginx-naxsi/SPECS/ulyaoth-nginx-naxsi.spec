#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm
%define nginx_version 1.8.1

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?fedora} >= 18
Group: System Environment/Daemons
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary: Nginx Anti Xss & Sql Injection.
Name: ulyaoth-nginx-naxsi
Version: 0.54
Release: 3%{?dist}
BuildArch: x86_64
Vendor: nginx inc.
URL: http://nginx.org/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: http://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/logrotate
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.init
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.sysconf
Source4: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx-naxsi.conf
Source5: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.vh.default-naxsi.conf
Source6: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.vh.example_ssl.conf
Source7: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.suse.init
Source8: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.service
Source9: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nginx.upgrade.sh
Source10: naxsi.tar.gz
Source11: naxsi_core.rules
Source12: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SOURCES/nbs.rules

License: 2-clause BSD-like license

Requires: openssl
Requires: GeoIP

BuildRoot: %{_tmppath}/nginx-%{nginx_version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: GeoIP
BuildRequires: GeoIP-devel
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: curl-devel

Provides: webserver
Provides: nginx
Provides: ulyaoth-nginx
Provides: nginx-naxsi
Provides: ulyaoth-nginx-naxsi

%description
Naxsi behaves like a DROP-by-default firewall, the only job needed is to add required ACCEPT rules for the target website to work properly.

%package debug
Summary: debug version of nginx compiled with Naxsi. 
Group: System Environment/Daemons
Requires: ulyaoth-nginx-naxsi
%description debug
Not stripped version of nginx built with the debugging log support and compiled with Naxsi.

%prep
%setup -q -n nginx-%{nginx_version}

%build
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
	    --with-http_geoip_module \
		--add-module=/etc/nginx/modules/naxsi/naxsi_src \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-http_spdy_module \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/nginx-%{nginx_version}/objs/nginx \
        %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
	    --with-http_geoip_module \
		--add-module=/etc/nginx/modules/naxsi/naxsi_src \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-http_spdy_module \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE11} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/naxsi_core.rules   
%{__install} -m 644 -p %{SOURCE12} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nbs.rules 
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-enabled

# Install ModSecurity
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules
tar xvf %{SOURCE10} -C $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules/
   
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%{__mkdir} -p $RPM_BUILD_ROOT/opt/
cd %{buildroot}/opt/
ln -s /etc/nginx/modules/naxsi/nxapi naxsi
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/opt/naxsi

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/sites-available
%dir %{_sysconfdir}/nginx/sites-enabled
%dir %{_sysconfdir}/nginx/modules
%{_sysconfdir}/nginx/modules/*

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/naxsi_core.rules
%config(noreplace) %{_sysconfdir}/nginx/nbs.rules
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-nginx-naxsi!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

Please find the official Naxsi documentation here:
* https://github.com/nbs-system/naxsi

For any additional help please visit our website at:
* https://www.ulyaoth.net

Ulyaoth repository could use your help! Please consider a donation:
* https://www.ulyaoth.net/donate.html

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%changelog
* Thu Jan 28 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.54-3
- Update to Nginx 1.8.1.

* Mon Dec 21 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.54-2
- Added the following symlink: /opt/naxsi -> /etc/nginx/modules/naxsi/nxapi.

* Sun Oct 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.54-1
- Build with Stable Naxsi version 0.54.

* Tue Jul 7 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 0.53.2-1
- Build with Stable Naxsi version 0.53-2.