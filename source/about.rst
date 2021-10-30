===============================
About Python Module of the Week
===============================

PyMOTW-3 is a series of articles written by `Doug Hellmann
<https://doughellmann.com/>`_.  to demonstrate how to use the modules of
the Python 3 standard library. It is based on the original PyMOTW_
series, which covered Python 2.7.

.. _PyMOTW: https://pymotw.com/2/

See the project home page at https://pymotw.com/3/ for updates.

Source code is available via git from https://github.com/dhellmann/pymotw-3/.

Complete documentation for the standard library can be found on the
Python web site at https://docs.python.org/3/library/.

Subscribe
=========

As new articles are written, they are posted to `my blog`_ as well as
https://pymotw.com.  Updates are available by RSS from
https://feeds.feedburner.com/PyMOTW. Follow
`@pymotw`_ or `@doughellmann`_ for updates as well.

.. _my blog: https://doughellmann.com/
.. _@pymotw: https://twitter.com/pymotw
.. _@doughellmann: https://twitter.com/doughellmann

Tools
=====

The source text for PyMOTW-3 is reStructuredText_ and the HTML output
is created using Sphinx_.

.. _reStructuredText: http://docutils.sourceforge.net

.. _Sphinx: http://www.sphinx-doc.org/en/stable/

The output from all the example programs has been generated with
CPython (see below for version) and inserted into the text using cog_.

.. _cog: http://nedbatchelder.com/code/cog/

.. {{{cog
.. cog.out(run_script(cog.inFile, '-V'))
.. }}}

.. code-block:: none

	$ python3 -V
	
	Python 3.7.1

.. {{{end}}}

.. warning::

  Some of the features described here may not be available in earlier
  versions of the standard library. When in doubt, refer to the
  documentation for the version of Python you are using.

Translations and Other Versions
===============================

`Italian <http://robyp.x10host.com/3/index.html>`__

  Roberto Pauletto has started translating the Python 3 articles into Italian.

`Chinese <http://www.pandacademy.com/pymotw-3-介绍/>`__

  Jaron has translated most of the articles into Chinese for pandacademy.com.

`Spanish <https://rico-schmidt.name/pymotw-3/>`__

  Ernesto Rico Schmidt has translated all of the articles into Spanish.

.. _copyright:

Copyright and Licensing
=======================

All of the prose from the Python Module of the Week is licensed under
a `Creative Commons Attribution, Non-commercial, Share-alike 4.0`_
license.  You are free to share and create derivative works from it.
If you post the material online, you must give attribution and link to
the PyMOTW home page (https://pymotw.com/).  You may not use this
work for commercial purposes.  If you alter, transform, or build upon
this work, you may distribute the resulting work only under the same
or similar license to this one.

The source code included here is copyright Doug Hellmann and licensed
under the BSD license.

   Copyright (c) 2015, Doug Hellmann, All Rights Reserved

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. _Creative Commons Attribution, Non-commercial, Share-alike 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/
