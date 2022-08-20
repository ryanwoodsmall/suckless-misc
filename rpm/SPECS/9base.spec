%global		debug_package	%{nil}

%define		git_rev_short	63916da
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d
%define		origp9dir	/usr/local/plan9

Name:		9base
Version:	%{timestamp}_%{git_rev_short}
Release:	19%{?dist}
Summary:	suckless 9base
Source0:	https://raw.githubusercontent.com/ryanwoodsmall/suckless-misc/master/bin/%{name}
Source1:	https://raw.githubusercontent.com/ryanwoodsmall/suckless-misc/master/bin/lc
Source2:	https://raw.githubusercontent.com/ryanwoodsmall/suckless-misc/master/bin/mc
Source3:	https://raw.githubusercontent.com/ryanwoodsmall/crosware-source-mirror/master/9base/fortunes-dc60de7b64948e89832f03181e6db799060036b8

Group:		System Environment/Shells
License:	MIT
URL:		https://tools.suckless.org/9base

BuildRequires:	musl-static >= 1.2.3-1
BuildRequires:	git

%description

This is a port of various original Plan 9 tools for Unix, based on
plan9port from suckless.org


%prep
cd %{_builddir}
test -d %{name} && rm -rf %{name}
git clone https://git.suckless.org/%{name}
cd %{name}
git checkout %{git_rev_short}
grep -ril '%{origp9dir}' \
| grep -v \\.git \
| xargs sed -i 's#%{origp9dir}#%{inst_prefix}#g'
sed -i '/^PREFIX/d' config.mk
sed -i '/^CC/d' config.mk
echo "CC = musl-gcc -fcommon" >> config.mk
echo "PREFIX = %{inst_prefix}" >> config.mk
%ifarch x86_64
	sed -i '/^OBJTYPE/d' config.mk
	echo "OBJTYPE = %{_arch}" >> config.mk
%endif


%build
. /etc/profile
cd %{_builddir}/%{name}
make


%install
. /etc/profile
cd %{_builddir}/%{name}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{profiled}
echo 'export PLAN9="%{inst_prefix}"' > %{buildroot}%{profiled}/zz_%{name}.sh
echo 'export PATH="${PATH}:${PLAN9}/bin"' >> %{buildroot}%{profiled}/zz_%{name}.sh
install -m 755 %SOURCE0 %{buildroot}%{inst_prefix}/bin
install -m 755 %SOURCE1 %{buildroot}%{inst_prefix}/bin
install -m 755 %SOURCE2 %{buildroot}%{inst_prefix}/bin
install -m 644 %SOURCE3 %{buildroot}%{inst_prefix}/lib/fortunes
ln -s %{inst_prefix}/bin/%{name} %{buildroot}%{inst_prefix}/bin/%{name}-box


%clean
cd %{_builddir}
rm -rf %{_builddir}/%{name}
rm -rf %{buildroot}


%files
%{inst_prefix}/*
%{_sysconfdir}/profile.d/*%{name}*.sh


%changelog
* Sat Aug 20 2022 ryanwoodsmall
- turn off debug
- source profile
- add -fcommon

* Fri Apr 29 2022 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.2.3

* Fri May 21 2021 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for...
- updated 9base script
- add mc (via sbase cols) and lc wrappers
- add fortunes

* Fri Jan 15 2021 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.2.2

* Wed Dec 30 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl CVE-2020-28928

* Tue Oct 20 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.2.1

* Sat Oct 26 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.24

* Wed Jul 17 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.23

* Thu Apr 11 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.22

* Tue Jan 22 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.21

* Wed Nov 28 2018 ryan woodsmall <rwoodsmall@gmail.com>
- make sure we have full url to 9base wrapper

* Tue Sep 11 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.20

* Wed Jul 11 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for buildroot cleanup

* Thu Feb 22 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.19

* Sat Feb 17 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for simpler 9base-box wrapper

* Fri Feb  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- add 9base sbase-box/ubase-box like wrapper script
- remove /bin/rc symlink, can be handled with static editline rc
- https://github.com/ryanwoodsmall/rc-misc

* Wed Jan 10 2018 ryan woodsmall <rwoodsmall@gmail.com>
- replace /usr/local/plan9 everywhere
- add /bin/rc symlink

* Tue Jan  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- ugly spec for building suckless 9base
