Name:           abuse
Version:        0.8
Release:        3%{?dist}
Summary:        The classic Crack-Dot-Com game
Group:          Amusements/Games
# The engine is GPLv2+, the data files are mostly in the public domain, except
# for the music and sfx files, which may be distributed freely, but not
# modified, and for the claudio addon, which states: "this ... can be used and
# modified freely for non-commercial purposes". Unfortunately the entire game
# depends heavily on the claudio addon now a days, so it cannot be removed.
License:        GPLv2+ and redistributable
URL:            http://abuse.zoy.org/
Source0:        http://abuse.zoy.org/raw-attachment/wiki/download/%{name}-%{version}.tar.gz
Source1:        http://abuse.zoy.org/static/%{name}.png
Source2:        %{name}.desktop
BuildRequires:  SDL-devel SDL_mixer-devel alsa-lib-devel libGLU-devel
BuildRequires:  desktop-file-utils ImageMagick
Requires:       hicolor-icon-theme
# abuse 0.8 comes with the data bundled
Obsoletes:      fRaBs < 2.11-7
Provides:       fRaBs = 2.11-7

%description
This is the SDL version of Abuse, the classic Crack-Dot-Com game. It can run in
a window or fullscreen and it has stereo sound with sound panning.


%prep
%setup -q


%build
%configure --with-assetdir=%{_datadir}/%{name}
make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
convert -background transparent -resize 256x256 -extent 256x256-28+0 \
  %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications 
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE2}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc AUTHORS COPYING* NEWS README
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_mandir}/man6/%{name}*.6*
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop


%changelog
* Sat May 11 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-3
- Resize icon to be exactly 256x256

* Thu May  9 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-2
- Add missing BuildRequires: SDL_mixer-devel

* Sat May  4 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.8-1
- Initial rpmfusion nonfree submission
