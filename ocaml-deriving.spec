Name:           ocaml-deriving
Version:        0.1.1a
Release:        %mkrel 2
Summary:        Extension to OCaml for deriving functions from types
License:        MIT
Group:          Development/Other
URL:            http://code.google.com/p/deriving/
Source0:        http://deriving.googlecode.com/files/deriving-%{version}.tar.gz
Patch0:         ocaml-deriving-no-link-libs.patch
Patch1:         ocaml-deriving-0.1.1a-dynlink.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml-findlib
BuildRequires:  camlp4

%description
Extension to OCaml for deriving functions from type declarations.
Includes derivers for pretty-printing, type-safe marshalling with
structure-sharing, dynamic typing, equality, and more.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n deriving-0.1.1
%patch0
%patch1 -p1

%build
make

cat > META <<EOF
name="deriving"
version="%{version}"
requires="camlp4"
description="%{summary}"
# need a syntax here XXX
archive(byte)="deriving.cma"
archive(native)="deriving.cmxa"
EOF

%check
cd tests
make
./tests

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p %{buildroot}%{_bindir}

ocamlfind install deriving \
  META lib/*.cma lib/*.cmxa lib/*.a lib/*.mli lib/*.cmi lib/*.cmx
install -m 0755 syntax/deriving %{buildroot}%{_bindir}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%dir %{_libdir}/ocaml/deriving
%{_libdir}/ocaml/deriving/META
%{_libdir}/ocaml/deriving/*.cma
%{_libdir}/ocaml/deriving/*.cmi
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc COPYING README CHANGES
%{_libdir}/ocaml/deriving/*.a
%{_libdir}/ocaml/deriving/*.cmxa
%{_libdir}/ocaml/deriving/*.cmx
%{_libdir}/ocaml/deriving/*.mli

