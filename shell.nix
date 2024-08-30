{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  buildInputs = with pkgs.python3Packages; [
    colorama
    contourpy
    cycler
    filelock
    fonttools
    fsspec
    jinja2
    kiwisolver
    markupsafe
    matplotlib
    mpmath
    networkx
    numpy
    packaging
    pillow
    pygame
    pyparsing
    python-dateutil
    six
    sympy
    torch
  ];

  shellHook = ''
    export SNAKE_AI_ENV="dev"
  '';
}

