#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software
# and its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Doug Hellmann not be used in advertising or publicity
# pertaining to distribution of the software without specific,
# written prior permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
"""
"""
#end_pymotw_header

import imp
import os
import shelve
import sys


def _mk_init_name(fullname):
    """Return the name of the __init__ module
    for a given package name.
    """
    if fullname.endswith('.__init__'):
        return fullname
    return fullname + '.__init__'


def _get_key_name(fullname, db):
    """Look in an open shelf for fullname or
    fullname.__init__, return the name found.
    """
    if fullname in db:
        return fullname
    init_name = _mk_init_name(fullname)
    if init_name in db:
        return init_name
    return None


class ShelveFinder(object):
    """Find modules collected in a shelve archive."""

    _maybe_recursing = False

    def __init__(self, path_entry):
        # Loading shelve causes an import recursive loop when it
        # imports dbm, and we know we are not going to load the
        # module # being imported, so when we seem to be
        # recursing just ignore the request so another finder
        # will be used.
        if ShelveFinder._maybe_recursing:
            raise ImportError
        try:
            # Test the path_entry to see if it is a valid shelf
            try:
                ShelveFinder._maybe_recursing = True
                with shelve.open(path_entry, 'r'):
                    pass
            finally:
                ShelveFinder._maybe_recursing = False
        except Exception as e:
            print('shelf could not import from %s: %s' %
                  (path_entry, e))
            raise
        else:
            print('shelf added to import path:', path_entry)
            self.path_entry = path_entry
        return

    def __str__(self):
        return '<%s for "%s">' % (self.__class__.__name__,
                                  self.path_entry)

    def find_module(self, fullname, path=None):
        path = path or self.path_entry
        print('\nlooking for "%s"\n  in %s' % (fullname, path))
        with shelve.open(self.path_entry, 'r') as db:
            key_name = _get_key_name(fullname, db)
            if key_name:
                print('  found it as %s' % key_name)
                return ShelveLoader(path)
        print('  not found')
        return None


class ShelveLoader(object):
    """Load source for modules from shelve databases."""

    def __init__(self, path_entry):
        self.path_entry = path_entry
        return

    def _get_filename(self, fullname):
        # Make up a fake filename that starts with the path entry
        # so pkgutil.get_data() works correctly.
        return os.path.join(self.path_entry, fullname)

    def get_source(self, fullname):
        print('loading source for "%s" from shelf' % fullname)
        try:
            with shelve.open(self.path_entry, 'r') as db:
                key_name = _get_key_name(fullname, db)
                if key_name:
                    return db[key_name]
                raise ImportError(
                    'could not find source for %s' % fullname
                )
        except Exception as e:
            print('could not load source:', e)
            raise ImportError(str(e))

    def get_code(self, fullname):
        source = self.get_source(fullname)
        print('compiling code for "%s"' % fullname)
        return compile(source, self._get_filename(fullname),
                       'exec', dont_inherit=True)

    def get_data(self, path):
        print('looking for data\n  in %s\n  for "%s"' %
              (self.path_entry, path))
        if not path.startswith(self.path_entry):
            raise IOError
        path = path[len(self.path_entry) + 1:]
        key_name = 'data:' + path
        try:
            with shelve.open(self.path_entry, 'r') as db:
                return db[key_name]
        except Exception:
            # Convert all errors to IOError
            raise IOError()

    def is_package(self, fullname):
        init_name = _mk_init_name(fullname)
        with shelve.open(self.path_entry, 'r') as db:
            return init_name in db

    def load_module(self, fullname):
        source = self.get_source(fullname)

        if fullname in sys.modules:
            print('reusing existing module from import of %r' %
                  fullname)
            mod = sys.modules[fullname]
        else:
            print('creating a new module object for %r' %
                  fullname)
            mod = sys.modules.setdefault(
                fullname,
                imp.new_module(fullname)
            )

        # Set a few properties required by PEP 302
        mod.__file__ = self._get_filename(fullname)
        mod.__name__ = fullname
        mod.__path__ = self.path_entry
        mod.__loader__ = self
        # PEP-366 specifies that package's set __package__ to
        # their name, and modules have it set to their parent
        # package (if any).
        if self.is_package(fullname):
            mod.__package__ = fullname
        else:
            mod.__package__ = '.'.join(fullname.split('.')[:-1])

        if self.is_package(fullname):
            print('adding path for package')
            # Set __path__ for packages
            # so we can find the sub-modules.
            mod.__path__ = [self.path_entry]
        else:
            print('imported as regular module')

        print('execing source...')
        exec(source, mod.__dict__)
        print('done')
        return mod
