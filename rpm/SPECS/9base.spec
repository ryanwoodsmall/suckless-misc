%define		git_rev_short	09e95a2
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d
%define		origp9dir	/usr/local/plan9

Name:		9base
Version:	%{timestamp}_%{git_rev_short}
Release:	2%{?dist}
Summary:	suckless 9base

Group:		System Environment/Shells
License:	MIT
URL:		https://tools.suckless.org/9base

BuildRequires:	musl-static >= 1.1.18
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
echo "CC = musl-gcc" >> config.mk
echo "PREFIX = %{inst_prefix}" >> config.mk
%ifarch x86_64
	sed -i '/^OBJTYPE/d' config.mk
	echo "OBJTYPE = %{_arch}" >> config.mk
%endif


%build
cd %{_builddir}/%{name}
make


%install
cd %{_builddir}/%{name}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{profiled}
echo 'export PLAN9="%{inst_prefix}"' > %{buildroot}%{profiled}/zz_%{name}.sh
echo 'export PATH="${PATH}:${PLAN9}/bin"' >> %{buildroot}%{profiled}/zz_%{name}.sh
mkdir -p %{buildroot}/bin
ln -s %{inst_prefix}/bin/rc %{buildroot}/bin/


%clean
cd %{_builddir}
rm -rf %{_builddir}/%{name}


%files
%{inst_prefix}/*
%{_sysconfdir}/profile.d/*%{name}*.sh
/bin/rc


%changelog
* Tue Jan 10 2018 ryan woodsmall <rwoodsmall@gmail.com>
- replace /usr/local/plan9 everywhere
- add /bin/rc symlink

* Tue Jan  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- ugly spec for building suckless 9base
