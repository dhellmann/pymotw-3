===================================
 hashlib --- Cryptographic Hashing
===================================

.. module:: hashlib
    :synopsis: Cryptographic hashes and message digests

The :mod:`hashlib` module defines an API for accessing different
cryptographic hashing algorithms. To work with a specific hash
algorithm, use the appropriate constructor function or :func:`new` to
create a hash object. From there, the objects use the same API, no
matter what algorithm is being used.

Hash Algorithms
===============

Since :mod:`hashlib` is "backed" by OpenSSL, all of the algorithms
provided by that library are available, including:

 * md5
 * sha1
 * sha224
 * sha256
 * sha384
 * sha512

Some algorithms are available on all platforms, and some depend on the
underlying libraries. For lists of each, look at
:data:`algorithms_guaranteed` and :data:`algorithms_available`
respectively.

.. literalinclude:: hashlib_algorithms.py
   :caption:
   :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_algorithms.py'))
.. }}}

.. code-block:: none

	$ python3 hashlib_algorithms.py
	
	Guaranteed:
	md5, sha1, sha224, sha256, sha384, sha512
	
	Available:
	DSA, DSA-SHA, MD4, MD5, MDC2, RIPEMD160, SHA, SHA1, SHA224, SHA2
	56, SHA384, SHA512, dsaEncryption, dsaWithSHA, ecdsa-with-SHA1, 
	md4, md5, mdc2, ripemd160, sha, sha1, sha224, sha256, sha384, sh
	a512

.. {{{end}}}



Sample Data
===========

All of the examples in this section use the same sample data:

.. literalinclude:: hashlib_data.py
    :caption:
    :start-after: #end_pymotw_header


MD5 Example
===========

To calculate the MD5 hash, or *digest*, for a block of data (here a
unicode string converted to a byte string), first create the hash
object, then add the data and call :func:`digest` or
:func:`hexdigest`.

.. literalinclude:: hashlib_md5.py
    :caption:
    :start-after: #end_pymotw_header

This example uses the :func:`hexdigest()` method instead of
:func:`digest()` because the output is formatted so it can be printed
clearly. If a binary digest value is acceptable, use :func:`digest()`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_md5.py'))
.. }}}

.. code-block:: none

	$ python3 hashlib_md5.py
	
	3f2fd2c9e25d60fb0fa5d593b802b7a8

.. {{{end}}}

SHA1 Example
============

A SHA1 digest is calculated in the same way.

.. literalinclude:: hashlib_sha1.py
    :caption:
    :start-after: #end_pymotw_header

The digest value is different in this example because the algorithm
changed from MD5 to SHA1.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_sha1.py'))
.. }}}

.. code-block:: none

	$ python3 hashlib_sha1.py
	
	ea360b288b3dd178fe2625f55b2959bf1dba6eef

.. {{{end}}}


Creating a Hash by Name
=======================

Sometimes it is more convenient to refer to the algorithm by name in a
string rather than by using the constructor function directly. It is
useful, for example, to be able to store the hash type in a
configuration file. In those cases, use :func:`new()` to create a hash
calculator.

.. literalinclude:: hashlib_new.py
    :caption:
    :start-after: #end_pymotw_header

When run with a variety of arguments:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha1'))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha256', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py sha512', include_prefix=False, break_lines_at=69))
.. cog.out(run_script(cog.inFile, 'hashlib_new.py md5', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 hashlib_new.py sha1
	
	ea360b288b3dd178fe2625f55b2959bf1dba6eef

	$ python3 hashlib_new.py sha256
	
	3c887cc71c67949df29568119cc646f46b9cd2c2b39d456065646bc2fc09ffd8

	$ python3 hashlib_new.py sha512
	
	a7e53384eb9bb4251a19571450465d51809e0b7046101b87c4faef96b9bc904cf7f90
	035f444952dfd9f6084eeee2457433f3ade614712f42f80960b2fca43ff

	$ python3 hashlib_new.py md5
	
	3f2fd2c9e25d60fb0fa5d593b802b7a8

.. {{{end}}}


Incremental Updates
===================

The :func:`update()` method of the hash calculators can be called
repeatedly. Each time, the digest is updated based on the additional
text fed in. Updating incrementally is more efficient than reading an
entire file into memory, and produces the same results.

.. literalinclude:: hashlib_update.py
    :caption:
    :start-after: #end_pymotw_header

This example demonstrates how to update a digest incrementally as data
is read or otherwise produced.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'hashlib_update.py'))
.. }}}

.. code-block:: none

	$ python3 hashlib_update.py
	
	All at once : 3f2fd2c9e25d60fb0fa5d593b802b7a8
	Line by line: 3f2fd2c9e25d60fb0fa5d593b802b7a8
	Same        : True

.. {{{end}}}

.. seealso::

    * :pydoc:`hashlib`

    * :mod:`hmac` -- The ``hmac`` module.

    * OpenSSL_ -- An open source encryption toolkit.

    * Cryptography_ module -- A Python package that provides
      cryptographic recipes and primitives.

    * `Voidspace: IronPython and hashlib
      <http://www.voidspace.org.uk/python/weblog/arch_d7_2006_10_07.shtml#e497>`_
      -- A wrapper for ``hashlib`` that works with IronPython.

.. _OpenSSL: http://www.openssl.org/
.. _Cryptography: https://pypi.python.org/pypi/cryptography
