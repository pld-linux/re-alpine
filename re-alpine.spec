# TODO:
# - backport man-pages from pine.spec
# - separate package with tcl web-frontend
# - fix as-needed
# - pico shouldn't link with kerberos, should it?
Summary:	The continuation of the Alpine email client from University of Washington
Summary(pl.UTF-8):	Kontynuacja klienta pocztowego Alpine z Uniwersytetu w Waszyngtonie
Name:		re-alpine
Version:	2.02
Release:	0.2
License:	Apache v2.0
Group:		Applications/Mail
# Main site:
Source0:	http://dl.sourceforge.net/re-alpine/%{name}-%{version}.tar.bz2
# Source0-md5:	5e75826b15f05674856be8618bdefdfb
Source1:	pico.desktop
Source2:	%{name}.desktop
Source3:	%{name}.png
Patch0:		%{name}-index_display.patch
Patch1:		%{name}-doc.patch
Patch2:		%{name}-filter.patch
Patch3:		%{name}-fhs.patch
Patch4:		%{name}-libc-client.patch
Patch5:		%{name}-ssl.patch
Patch6:		%{name}-no_1777_warning.patch
Patch7:		%{name}-home_etc.patch
URL:		http://re-alpine.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	home-etc-devel
%if "%{pld_release}" != "ac"
BuildRequires:	heimdal-devel
%endif
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
# Only for web-frontend:
#BuildRequires:	tcl-devel
Suggests:	aspell
Suggests:	ca-certificates
Conflicts:	ca-certificates < 20080809-4
Provides:	pine = 6.02
Provides:	alpine = 1:%{version}-%{release} 
Obsoletes:	pine
Obsoletes:	alpine < 1:2.01
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		alpineconfdir	%{_sysconfdir}/%{name}
%define		filterout_ld	-Wl,--as-needed

%description
Alpine -- an Alternatively Licensed Program for Internet News & Email
-- is a tool for reading, sending, and managing electronic messages.
Alpine is the successor to Pine and was developed by Computing &
Communications at the University of Washington. Though originally
designed for inexperienced email users, Alpine supports many advanced
features, and an ever-growing number of configuration and
personal-preference options.

%description -l pl.UTF-8
Alpine, czyli Alternatively Licensed Program for Internet News & Email
(alternatywnie licencjonowany program do newsów i poczty internetowej)
to narzędzie do czytania, wysyłania i zarządzania wiadomościami
elektronicznymi. Alpine jest następcą Pine'a i został napisany przez
wydział Computing & Communications (Obliczeń i komunikacji) na
Uniwersytecie w Waszyngtonie. Mimo że Alpine pierwotnie został
zaprojektowany dla niedoświadczonych użytkowników poczty, obsługuje
wiele zaawansowanych możliwości, a liczba opcji konfiguracyjnych
ciągle rośnie.

%package -n pico
Summary:	Simple text editor in the style of the Pine Composer
Summary(pl.UTF-8):	Prosty edytor tekstowy w stylu alpine
Summary(pt_BR.UTF-8):	Editor de textos para terminal simples e fácil de usar
Group:		Applications/Editors
Provides:	pico = 6.02

%description -n pico
Pico is a simple, display-oriented text editor based on the Alpine
message system composer. As with Pine, commands are displayed at the
bottom of the screen, and context-sensitive help is provided. As
characters are typed they are immediately inserted into the text.

%description -n pico -l pl.UTF-8
Pico jest prostym, zorientowanym na wyświetlanie edytorem bazującym na
alpine. Tak jak w pine komendy są wyświetlane na dole ekranu oraz
dostępna jest pomoc kontekstowa. Wpisywane znaki są natychmiast
włączane do tekstu.

%description -n pico -l pt_BR.UTF-8
Pico é um editor de texto baseado no compositor de mensagens do Alpine.
Assim como no Pine, comandos são mostrados na parte de baixo da tela,
e ajuda de acordo com o contexto está disponível.

%package -n pilot
Summary:	Simple file system browser in the style of the Alpine Composer
Summary(pl.UTF-8):	Prosta przeglądarka plików w stylu composera alpine
Summary(pt_BR.UTF-8):	Navegador de sistemas de arquivos no estilo do compositor do Alpine
Group:		Applications/Shells
Provides:	pilot = 6.02

%description -n pilot
Pilot is a simple, display-oriented file system browser based on the
Alpine message system composer. As with Alpine, commands are displayed
at the bottom of the screen, and context-sensitive help is provided.

%description -n pilot -l pl.UTF-8
Pilot jest prostą, zorientowaną na wyświetlanie przeglądarką plików w
stylu composera pine. Podobnie jak w alpine polecenia są wyświetlane
na dole ekranu oraz jest dostępna pomoc kontekstowa.

%description -n pilot -l pt_BR.UTF-8
Pilot é um navegador de sistemas de arquivos baseado no Pine. Assim
como no Pine, comandos são apresentados na parte de baixo da tela, e
ajuda de acordo com o contexto está disponível.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1

%build
rm -f libtool missing
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-quotas \
	--without-tcl \
	--with-smtp-msa=/usr/lib/sendmail \
	--with-simple-spellcheck=aspell \
	--with-system-pinerc=%{_sysconfdir}/%{name}/%{name}.conf \
	--with-system-fixed-pinerc=%{_sysconfdir}/%{name}/%{name}.conf.fixed \
	--with-krb5-dir=%{_prefix} \
	--with-ldap-dir=%{_prefix} \
	--with-system-mail-directory=/var/mail \
	--with-c-client-target=slx \
%if "%{pld_release}" == "ti"
	--with-ssl-dir=/var/lib/openssl/certs \
	--with-ssl-certs-dir=/var/lib/openssl/certs \
%else
	--with-ssl-dir=/etc/openssl/certs \
	--with-ssl-certs-dir=/etc/certs \
%endif
	--with-passfile=.pine.pwd

%{__make} \
	GCCOPTLEVEL="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

ln -s re-alpine $RPM_BUILD_ROOT%{_bindir}/pine

$RPM_BUILD_ROOT%{_bindir}/alpine -conf > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/alpine.conf
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/alpine.conf.fixed
#
# Alpine system-wide enforced configuration file - customize as needed
#
# This file holds the system-wide enforced values for alpine configuration
# settings. Any values set in it will override values set in the
# system-wide default configuration file (%{_sysconfdir}/%{name}/alpine.conf) and
# the user's own configuration file (~/.pinerc).
# For more information on the format of this file, read the
# comments at the top of %{_sysconfdir}/%{name}/alpine.conf

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README doc/tech-notes.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/alpine.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/alpine.conf.fixed
%attr(755,root,root) %{_bindir}/alpine
%attr(755,root,root) %{_bindir}/pine
%attr(755,root,root) %{_bindir}/rpload
%attr(755,root,root) %{_bindir}/rpdump
%{_mandir}/man1/alpine.1*
%{_mandir}/man1/rpload.1*
%{_mandir}/man1/rpdump.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%files -n pico
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pico
%{_desktopdir}/pico.desktop
%{_mandir}/man1/pico*

%files -n pilot
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pilot
%{_mandir}/man1/pilot*
