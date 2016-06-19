#!/bin/bash
#
# Instructions for installing external dependencies with homebrew.
#

PKGS="
gettext
graphviz
lynx
readline
"

for pkg in $PKGS; do
    brew install $pkg
done
