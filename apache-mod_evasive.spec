%define		mod_name	evasive
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: evasive
Summary(pl.UTF-8):	Moduł Apache'a: evasive
Name:		apache-mod_%{mod_name}
Version:	1.10.1
Release:	1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	http://www.zdziarski.com/projects/mod_evasive/mod_evasive_%{version}.tar.gz
# Source0-md5:	784fca4a124f25ccff5b48c7a69a65e5
Source1:	%{name}.conf
URL:		http://www.zdziarski.com/projects/mod_evasive/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_evasive is an evasive maneuvers module for Apache.

%description -l pl.UTF-8

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}20.c -o mod_%{mod_name}20.la -DMAILER='/usr/lib/sendmail -t'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install .libs/mod_%{mod_name}20.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
