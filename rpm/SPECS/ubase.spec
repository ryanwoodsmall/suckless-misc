%define		git_rev_short	3c88778
%define		timestamp	%(date '+%%Y%%m%%d%%H%%M%%S')
%define		inst_prefix	/opt/%{name}
%define		profiled	%{_sysconfdir}/profile.d

Name:		ubase
Version:	%{timestamp}_%{git_rev_short}
Release:	10%{?dist}
Summary:	suckless %{name}

Group:		System Environment/Shells
License:	MIT
URL:		https://core.suckless.org/%{name}

BuildRequires:	musl-static >= 1.2.1-1
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
# XXX - ugh
#sed -i '/__GLIBC__/s/ifdef/ifndef/g' ls.c tar.c
echo '#include <sys/sysmacros.h>' >> util.h


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
