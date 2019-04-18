%define		git_rev_short	ef9f6f3
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d

Name:		sbase
Version:	%{timestamp}_%{git_rev_short}
Release:	6%{?dist}
Summary:	suckless %{name}

Group:		System Environment/Shells
License:	MIT
URL:		https://core.suckless.org/%{name}

BuildRequires:	musl-static >= 1.1.22
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
make %{name}-box


%install
cd %{_builddir}/%{name}
make %{name}-box-install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{profiled}
echo 'export PATH="${PATH}:%{inst_prefix}/bin"' > %{buildroot}%{profiled}/zz_%{name}.sh


%clean
cd %{_builddir}
rm -rf %{_builddir}/%{name}
rm -rf %{buildroot}


%files
%{inst_prefix}/*
%{_sysconfdir}/profile.d/*%{name}*.sh


%changelog
* Thu Apr 11 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.22

* Tue Jan 22 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.21

* Tue Sep 11 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.20

* Wed Jul 11 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for buildroot cleanup

* Fri Jun 29 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for sbase/ubase spec sync

* Thu Feb 22 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release no. bump for musl-libc 1.1.19

* Tue Jan  9 2018 ryan woodsmall <rwoodsmall@gmail.com>
- ugly rpm specs for building suckless *base
