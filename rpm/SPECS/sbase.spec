%define		git_rev_short	4b9c664
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d

Name:		sbase
Version:	%{timestamp}_%{git_rev_short}
Release:	0%{?dist}
Summary:	suckless sbase

Group:		System Environment/Shells
License:	MIT
URL:		https://core.suckless.org/sbase

BuildRequires:	musl-static >= 1.1.18
BuildRequires:	git

%description

sbase - suckless base
sbase is a collection of unix tools that are portable across unix-systems.


%prep
cd %{_builddir}
test -d %{name} && rm -rf %{name}
git clone https://git.suckless.org/%{name}
cd %{name}
git checkout %{git_rev_short}
sed -i.ORIG '/^PREFIX/d' config.mk
sed -i '/^CC/d' config.mk
sed -i '/^LDFLAGS/d' config.mk
echo "CC = musl-gcc" >> config.mk
echo "PREFIX = %{inst_prefix}" >> config.mk
echo "LDFLAGS = -s -static" >> config.mk


%build
cd %{_builddir}/%{name}
make sbase-box


%install
cd %{_builddir}/%{name}
make sbase-box-install DESTDIR=%{buildroot}
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
- ugly spec for building suckless sbase
