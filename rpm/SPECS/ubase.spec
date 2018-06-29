%define		git_rev_short	5579553
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d

Name:		ubase
Version:	%{timestamp}_%{git_rev_short}
Release:	2%{?dist}
Summary:	suckless %{name}

Group:		System Environment/Shells
License:	MIT
URL:		https://core.suckless.org/%{name}

BuildRequires:	musl-static >= 1.1.19
BuildRequires:	git

%description

ubase - unportable base
ubase is a collection of unportable tools, similar in spirit to util-linux but much simpler.


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
make %{name}-box


%install
cd %{_builddir}/%{name}
make %{name}-box-install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{profiled}
echo 'export PATH="${PATH}:%{inst_prefix}/bin"' > %{buildroot}%{profiled}/zz_%{name}.sh


%clean
cd %{_builddir}
rm -rf %{_builddir}/%{name}


%files
%{inst_prefix}/*
%{_sysconfdir}/profile.d/*%{name}*.sh


%changelog
* Fri Jun 29 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for sbase/ubase spec sync

* Thu Feb 22 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.19

* Tue Jan  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- ugly spec for building suckless ubase
