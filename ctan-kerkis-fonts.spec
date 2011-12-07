%global foundryname  ctan
%global fontpkg      kerkis
%global fontname     %{foundryname}-%{fontpkg}
%global fontconf     64-%{fontname}
%global ctan_date    20090115
%global texfonts     %{_texmf_main}/fonts
%global texfontpath  %{fontpkg}

# Common description
%global common_desc Kerkis type 1 fonts for LaTeX.  These fonts are particularly useful \
for typesetting Greek. The Greek repertoire includes full support for \
polytonic Greek, Greek numerals, and double forms of several letters \
that occur in variant forms.


Name:           ctan-kerkis-fonts
Version:        2.0
Release:        23%{?dist}
Summary:        Kerkis Type 1 fonts
Group:          Applications/Publishing
License:        LPPL
URL:            http://www.ctan.org/tex-archive/help/Catalogue/entries/kerkis.html
Source0:        kerkis-%{ctan_date}.zip
# upstream source - unversioned zip file
# ftp://tug.ctan.org/pub/tex-archive/fonts/greek/kerkis.zip
Source1:        %{fontname}-fontconfig.tar.gz
# Tarball of fontconfig files for each font
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  fontpackages-devel texlive-texmf
%description
%{common_desc}


%package common
Summary:  Kerkis Type 1 fonts, common files (documentation…)
Group:    User Interface/X
Requires: fontpackages-filesystem
%description common
%common_desc
This package consists of files used by other %{fontname} packages.


%global seriffonts %{fontname}-serif-fonts
%package -n %{seriffonts}
Summary:  Kerkis serif Type1 fonts
Group:    User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{seriffonts}
%{common_desc}
This package contains the Kerkis font family. It is based on the URW Bookman
font and extends it with Greek characters and math support.

%_font_pkg -n serif -f %{fontconf}-serif.conf Kerkis.* Kerkis-*Bold.* Kerkis-*Italic.* Kerkis-*SmallCaps*


%global sansfonts %{fontname}-sans-fonts
%package -n %{sansfonts}
Summary:  KerkisSans Type1 fonts
Group:    User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{sansfonts}
%{common_desc}
This package contains the KerkisSans font family, based on a free version
of the AvantGardURW Bookman font.

%_font_pkg -n sans -f %{fontconf}-sans.conf KerkisSans* 


%global calligraphicfonts %{fontname}-calligraphic-fonts
%package -n %{calligraphicfonts}
Summary:  Kerkis Calligraphic Type1 fonts
Group:    User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{calligraphicfonts}
%{common_desc}
This package contains the Kerkis-Calligraphic font family, a calligraphic font 
family of Kerkis, based on URW Bookman.

%_font_pkg -n calligraphic -f %{fontconf}-calligraphic.conf Kerkis-Calligraphic* ktsy.*


%global texfontpkg tex-kerkis
%package -n %{texfontpkg}
Summary:  Kerkis Type1 fonts, TeX support files
Group:    User Interface/X
Requires: %{seriffonts} = %{version}-%{release}, %{sansfonts} = %{version}-%{release}
Requires: tex(latex)
Provides: tetex-font-kerkis = %{version}-%{release}
Obsoletes: tetex-font-kerkis < 2.0-17

%description -n %{texfontpkg}
%{common_desc}
TeX support files.


%prep
%setup -q -a1 -n %{fontpkg}


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_texmf_main}/tex/latex/%{fontpkg}
mkdir -p %{buildroot}%{texfonts}/{afm,tfm,type1,vf}/%{texfontpath}
mkdir -p %{buildroot}%{texfonts}/{map,enc}/dvips/%{fontpkg}

install -p -m 644 tex/{*.sty,*.fd} %{buildroot}%{_texmf_main}/tex/latex/%{fontpkg}/
install -p -m 644 tfm/*.tfm %{buildroot}%{texfonts}/tfm/%{texfontpath}/
install -p -m 644 vf/*.vf %{buildroot}%{texfonts}/vf/%{texfontpath}/
install -p -m 644 dvips/*.map %{buildroot}%{texfonts}/map/dvips/%{fontpkg}/
install -p -m 644 dvips/*.enc %{buildroot}%{texfonts}/enc/dvips/%{fontpkg}/

#install .pfb and .afm files in %{_fontdir} as per the fedora font guidelines
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p type1/* %{buildroot}%{_fontdir}
install -m 0644 -p afm/* %{buildroot}%{_fontdir}

pushd %{buildroot}%{_fontdir}
for pfb_file in *.pfb ;  do
    ln -s %{_fontdir}/$pfb_file %{buildroot}%{texfonts}/type1/%{texfontpath}/$pfb_file
done
for afm_file in *.afm ;  do
    ln -s %{_fontdir}/$afm_file %{buildroot}%{texfonts}/afm/%{texfontpath}/$afm_file
done
popd


# fontconfig stuff (see spectemplate-fonts-multi.spec)
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p fontconfig/%{fontname}-serif.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf
install -m 0644 -p fontconfig/%{fontname}-sans.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p fontconfig/%{fontname}-calligraphic.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-calligraphic.conf


for fconf in %{fontconf}-serif.conf \
             %{fontconf}-sans.conf \
             %{fontconf}-calligraphic.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done



%clean
rm -rf %{buildroot}


%post -n %{texfontpkg}
texhash
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" = "1" ]; then
    updmap-sys --quiet --nohash --cnffile ${conffile} --enable Map %{fontpkg}.map
fi


%postun -n %{texfontpkg}
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" = "0" ]; then
    updmap-sys --quiet --nohash --cnffile ${conffile} --disable %{fontpkg}.map
fi
texhash

%files common
%defattr(0644,root,root,0755)
%doc License.txt README.html
%dir %{_fontdir}


%files -n %{texfontpkg}
%defattr(-,root,root,-)
%{_texmf_main}/tex/latex/%{fontpkg}
%{texfonts}/afm/%{texfontpath}
%{texfonts}/tfm/%{texfontpath}
%{texfonts}/type1/%{texfontpath}
%{texfonts}/vf/%{texfontpath}
%{texfonts}/map/dvips/%{fontpkg}
%{texfonts}/enc/dvips/%{fontpkg}



%changelog
* Thu Feb 11 2010 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-23
- Update source (tiny patch in kerkis.sty) (bug #561794). Thanks Jens Petersen
- Minor housecleaning

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.0-22.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  1 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-20
- Also add forgotten requires on -common.

* Sat Jan 31 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-19
- Add forgotten %%{_fontdir} in %%files section in -common (bz #483333)

* Tue Jan 20 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-18
- Address comments in https://bugzilla.redhat.com/show_bug.cgi?id=480591#c2
  (thanks Nicolas Mailhot)
    - Add a buildrequires for texlive-texmf
    - Remove Requires: fontpackages-filesystem from main and add to common
      subpackage.
    - Fix Obsoletes to cover latest update for F-10
    - Add -calligraphic-fonts subpackage
    - Add substitution rules for fonts from which Kerkis and KerkisSans
      derived
    - Remove tabs to silence rpmlint

* Fri Jan 16 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-17
- Rename the package to ctan-kerkis-fonts
- Name the subpackages according to
  http://fedoraproject.org/wiki/PackagingDrafts/Font_package_naming_(2009-01-13)
- Update to fontpackages-* >= 1.15

* Mon Jan 12 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-16
- Restructure spec file according to
  https://fedoraproject.org/wiki/Fonts_SIG_Fedora_11_packaging_changes
  (bug #477462)
- Split package to cm-lgc-fonts (.pfb and .afm) and tetex-font-cm-lgc
  (TeX stuff)
- Include .afm files (forgotten in the previous versions)


* Fri Jan  4 2008 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-15
- Drop requirement for -fonts.
- Point source URL to ctan.
- Change license to LPPL.

* Tue Aug 29 2006 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-13
- Bump release for FC6 rebuild.

* Mon Feb 20 2006 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-11
- Rebuild for FC5.

* Sun Nov  6 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-10
- Use run-time define updmap.cfg (Michal Jaegermann, bug #172492).

* Wed Nov  2 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-9
- Use absolute path commands in post and postun.

* Wed Nov  2 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-8
- Remove explicit outputdir for updmap-sys (bug #172268)
- Readd texhash in post and postun.

* Fri Oct  7 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-7
- Require tetex-fonts.
- Drop kerkis-test.tex.
- Use ctan zip soure.
- Other cleanups.

* Tue Jun 21 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-6
- Run updmap-sys only when installing/removing, not updating.

* Fri Jun 10 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-5
- Fix location for font encoding files
- Use updmap-sys instead of updmap

* Wed Jun  1 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 2.0-4
- update location for map files according to TeXLive 2004.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed May  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.0-0.fdr.2
- Added kerkis-test.tex test document (bug 998).
- Moved preun script to postun (bug 998).
- Split Requires(post,postun) into separate Require statements (bug 998).

* Sun Nov 16 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:2.0-0.fdr.1
- Initial RPM release.
