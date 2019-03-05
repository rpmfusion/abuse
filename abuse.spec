%global commit 3c674b19c6ccb5fe4943658f41bb188a8dd19d5c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           abuse
Version:        0.9
Release:        4%{?dist}
Summary:        The classic Crack-Dot-Com game
# The engine is GPLv2+, the data files are mostly in the public domain, except
# for the music and sfx files, which may be distributed freely, but not
# modified, and for the claudio addon, which states: "this ... can be used and
# modified freely for non-commercial purposes". Unfortunately the entire game
# depends heavily on the claudio addon now a days, so it cannot be removed.
License:        GPLv2+ and redistributable
URL:            http://abuse.zoy.org/
Source0:        https://github.com/Xenoveritas/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# We use the original 0.8 sources for the non-free sfx and music
Source1:        http://abuse.zoy.org/raw-attachment/wiki/download/%{name}-0.8.tar.gz
Source2:        %{name}.png
Source3:        %{name}.desktop
# Fix NULL pointer deref at startup
Patch0:         0001-Fix-NULL-pointer-deref-when-built-with-gcc-O1-or-O2.patch
BuildRequires:  SDL2-devel SDL2_mixer-devel alsa-lib-devel libGLU-devel
BuildRequires:  cmake desktop-file-utils ImageMagick gcc-c++
Requires:       hicolor-icon-theme

%description
This is the SDL version of Abuse, the classic Crack-Dot-Com game. It can run
in a window or fullscreen and it has stereo sound with sound panning.


%prep
%autosetup -p1 -n %{name}-%{commit} -a 1
mv abuse-0.8/data/sfx abuse-0.8/data/music data
sed -i 's/@VERSION@/%{version}/' doc/abuse*.6.in


%build
mkdir build
pushd build
# BUILD_SHARED_LIBS:BOOL=OFF -> make builtin helper libs static
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF ..
make %{?_smp_mflags}
popd


%install
pushd build
%make_install INSTALL="install -p"
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
convert -background transparent -resize 256x256 -extent 256x256-28+0 \
  %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications 
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE3}

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6
install -p -m 0644 doc/abuse.6.in $RPM_BUILD_ROOT%{_mandir}/man6/abuse.6
install -p -m 0644 doc/abuse-tool.6.in $RPM_BUILD_ROOT%{_mandir}/man6/abuse-tool.6


%files
%doc AUTHORS COPYING* NEWS README.md
%{_bindir}/%{name}*
%{_datadir}/games/%{name}
%{_mandir}/man6/%{name}*.6*
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop


%changelog
* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Hans de Goede <j.w.r.degoede@gmail.com> - 0.9-1
- Rebase to now github upstream, which calls itself version 0.9
- 0.9 uses SDL2 instead of SDL-1.2
- Fix abuse crashing at startup, making it playable again (rf#4276)
- Modernize spec file a bit

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-6
- Rebuilt

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-5
- Rebuilt

* Mon Aug 26 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-4
- Really resize the icon to be exactly 256x256

* Sat May 11 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-3
- Resize icon to be exactly 256x256

* Thu May  9 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-2
- Add missing BuildRequires: SDL_mixer-devel

* Sat May  4 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-1
- Initial rpmfusion nonfree submission
