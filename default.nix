{ nixpkgs ? import <nixpkgs> {}
}:

let
  sourceFilter =
    with nixpkgs.lib; with builtins;
    path: type:
    let
      name = baseNameOf (toString path);
      ignoreDirectories = directories:
        !(any (directory: directory == name && type == "directory")
          directories);
      ignoreFileTypes = types:
        !(any (type: hasSuffix ("." + type) name && type == "regular") types);
    in ignoreDirectories [
      "bumpv.egg-info"
      "__pycache__"
      "build"
      "dist"
      ".mypy_cache"
    ] && ignoreFileTypes [ "pyc" ];
  bumpv =
    { buildPythonPackage
    , click
    , pyaml
    , lib
    }:
    buildPythonPackage {
      name = "bumpv";
      src = lib.cleanSourceWith {
        src = ./.;
        filter = sourceFilter;
      };
      propagatedBuildInputs = [
        click
        pyaml
      ];
    };
in nixpkgs.python36.pkgs.callPackage bumpv {}
