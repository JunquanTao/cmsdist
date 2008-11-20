### RPM external p5-time-hires 1.9715-CMS22
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Time-HiRes

Source: http://search.cpan.org/CPAN/authors/id/J/JH/JHI/%{downloadn}-%{realversion}.tar.gz
%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
