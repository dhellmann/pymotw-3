===================================================
hashlib -- Cryptographic hashes and message digests
===================================================

.. module:: hashlib
    :synopsis: Cryptographic hashes and message digests

:Purpose: Cryptographic hashes and message digests
:Available In: 2.5

The :mod:`hashlib` module deprecates the separate :mod:`md5` and
:mod:`sha` modules and makes their API consistent. To work with a
specific hash algorithm, use the appropriate constructor function to
create a hash object. Then you can use the same API to interact with
the hash no matter what algorithm is being used.

Since :mod:`hashlib` is "backed" by OpenSSL, all of of the algorithms
provided by that library are available, including:

 * md5
 * sha1
 * sha224
 * sha256
 * sha384
 * sha512

Sample Data
===========

All of the examples below use the same sample data:

.. include:: hashlib_data.py
    :literal:
    :start-after: #end_pymotw_header


MD5 Example
===========

To calculate the MD5 digest for a block of data (here an ASCII
string), create the hash object, add the data, and compute the digest.

.. include:: hashlib_md5.py
    :literal:
    :start-after: #end_pymotw_header

This example uses the :func:`hexdigest()` method instead of
:func:`digest()` because the output is formatted to be printed. If a
binary digest value is acceptable, you can use :func:`digest()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_md5.py'))
.. }}}

::

	$ python hashlib_md5.py
	
	c3abe541f361b1bfbbcfecbf53aad1fb

.. {{{end}}}

SHA1 Example
============

A SHA1 digest for the same data would be calculated in much the same way.

.. include:: hashlib_sha1.py
    :literal:
    :start-after: #end_pymotw_header

The digest value is different in this example because we changed the
algorithm from MD5 to SHA1

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_sha1.py'))
.. }}}

::

	$ python hashlib_sha1.py
	
	ac2a96a4237886637d5352d606d7a7b6d7ad2f29

.. {{{end}}}


new()
=====

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
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha512', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py md5', include_prefix=False))
.. }}}

::

	$ python hashlib_new.py sha1
	
	ac2a96a4237886637d5352d606d7a7b6d7ad2f29

	$ python hashlib_new.py sha256
	
	88b7404fc192fcdb9bb1dba1ad118aa1ccd580e9faa110d12b4d63988cf20332

	$ python hashlib_new.py sha512
	
	f58c6935ef9d5a94d296207ee4a7d9bba411539d8677482b7e9d60e4b7137f68d25f9747cab62fe752ec5ed1e5b2fa4cdbc8c9203267f995a5d17e4408dccdb4

	$ python hashlib_new.py md5
	
	c3abe541f361b1bfbbcfecbf53aad1fb

.. {{{end}}}


Calling update() more than once
===============================

The :func:`update()` method of the hash calculators can be called
repeatedly. Each time, the digest is updated based on the additional
text fed in. This can be much more efficient than reading an entire
file into memory, for example.

.. include:: hashlib_update.py
    :literal:
    :start-after: #end_pymotw_header

This example is a little contrived because it works with such a small amount
of text, but it illustrates how you could incrementally update a digest as
data is read or otherwise produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_update.py'))
.. }}}

::

	$ python hashlib_update.py
	
	All at once : c3abe541f361b1bfbbcfecbf53aad1fb
	Line by line: c3abe541f361b1bfbbcfecbf53aad1fb
	Same        : True

.. {{{end}}}

.. seealso::

    `hashlib <http://docs.python.org/2.7/library/hashlib.html>`_
        The standard library documentation for this module.

    `Voidspace: IronPython and hashlib <http://www.voidspace.org.uk/python/weblog/arch_d7_2006_10_07.shtml#e497>`_
        A wrapper for :mod:`hashlib` that works with IronPython.

    :mod:`hmac`
        The :mod:`hmac` module.
