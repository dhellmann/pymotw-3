==================================
 hashlib -- Cryptographic Hashing
==================================

.. module:: hashlib
    :synopsis: Cryptographic hashes and message digests

:Purpose: Cryptographic hashes and message digests
:Python Version: 2.5 and later

The :mod:`hashlib` module deprecates the separate :mod:`md5` and
:mod:`sha` modules and makes their API consistent. To work with a
specific hash algorithm, use the appropriate constructor function to
create a hash object. From there, the objects use the same API, no
matter what algorithm is being used.

Since :mod:`hashlib` is "backed" by OpenSSL, all of the algorithms
provided by that library are available, including:

 * md5
 * sha1
 * sha224
 * sha256
 * sha384
 * sha512

Sample Data
===========

All of the examples in this section use the same sample data:

.. include:: hashlib_data.py
    :literal:
    :start-after: #end_pymotw_header


MD5 Example
===========

To calculate the MD5 hash, or :term:`digest`, for a block of data
(here an ASCII string), first create the hash object, then add the
data and call :func:`digest` or :func:`hexdigest`.

.. include:: hashlib_md5.py
    :literal:
    :start-after: #end_pymotw_header

This example uses the :func:`hexdigest()` method instead of
:func:`digest()` because the output is formatted so it can be printed
clearly. If a binary digest value is acceptable, use :func:`digest()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_md5.py'))
.. }}}

::

	$ python hashlib_md5.py

	1426f365574592350315090e295ac273

.. {{{end}}}

SHA1 Example
============

A SHA1 digest is calculated in the same way.

.. include:: hashlib_sha1.py
    :literal:
    :start-after: #end_pymotw_header

The digest value is different in this example because the algorithm
changed from MD5 to SHA1.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_sha1.py'))
.. }}}

::

	$ python hashlib_sha1.py

	8173396ba8a560b89a3f3e2fcc024b044bc83d0a

.. {{{end}}}


Creating a Hash by Name
=======================

Sometimes it is more convenient to refer to the algorithm by name in a
string rather than by using the constructor function directly. It is
useful, for example, to be able to store the hash type in a
configuration file. In those cases, use :func:`new()` to create a hash
calculator.

.. include:: hashlib_new.py
    :literal:
    :start-after: #end_pymotw_header

When run with a variety of arguments:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha1'))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha256', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha512', include_prefix=False, break_lines_at=69))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py md5', include_prefix=False))
.. }}}

::

	$ python hashlib_new.py sha1

	8173396ba8a560b89a3f3e2fcc024b044bc83d0a

	$ python hashlib_new.py sha256

	dca37495608c68ec23bbb54ab9675bf0152db63e5a51ab1061dc9982b843e767

	$ python hashlib_new.py sha512

	0e3d4bc1cbc117382fa077b147a7ff6363f6cbc7508877460f978a566a0adb6dbb4c8
	b89f56514da98eb94d7135e1b7ad7fc4a2d747c02af67fcd4e571bd54de

	$ python hashlib_new.py md5

	1426f365574592350315090e295ac273

.. {{{end}}}


Incremental Updates
===================

The :func:`update()` method of the hash calculators can be called
repeatedly. Each time, the digest is updated based on the additional
text fed in. Updating incrementally is more efficient than reading an
entire file into memory, and produces the same results.

.. include:: hashlib_update.py
    :literal:
    :start-after: #end_pymotw_header

This example demonstrates how to update a digest incrementally as data
is read or otherwise produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_update.py'))
.. }}}

::

	$ python hashlib_update.py

	All at once : 1426f365574592350315090e295ac273
	Line by line: 1426f365574592350315090e295ac273
	Same        : True

.. {{{end}}}

.. seealso::

    `hashlib <http://docs.python.org/library/hashlib.html>`_
        The standard library documentation for this module.

    `Voidspace: IronPython and hashlib <http://www.voidspace.org.uk/python/weblog/arch_d7_2006_10_07.shtml#e497>`_
        A wrapper for ``hashlib`` that works with IronPython.

    :mod:`hmac`
        The ``hmac`` module.

    OpenSSL_
        An open source encryption toolkit.

.. _OpenSSL: http://www.openssl.org/
