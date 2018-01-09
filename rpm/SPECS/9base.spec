%define		git_rev_short	09e95a2
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d

Name:		9base
Version:	%{timestamp}_%{git_rev_short}
Release:	0%{?dist}
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
sed -i.ORIG 's#/usr/local/plan9#%{inst_prefix}#g' ssam/ssam sam/sam.c
sed -i.ORIG '/^PREFIX/d' config.mk
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
echo 'export PATH="${PATH}:%{inst_prefix}/bin"' > %{buildroot}%{profiled}/zz_%{name}.sh


%clean
cd %{_builddir}
rm -rf %{_builddir}/%{name}


%files
%{inst_prefix}/*
%{_sysconfdir}/profile.d/*%{name}*.sh


%changelog
* Tue Jan  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- ugly spec for building suckless 9base
