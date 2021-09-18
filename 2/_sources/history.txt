History
=======

Development

  - Merge in fixes to the :mod:`select` module examples from Michael
    Schurter.

1.132

  - 24 Oct 2010, rewrite :mod:`ConfigParser`

1.131

  - 17 Oct 2010, :mod:`sqlite3`
  - Updates to :mod:`xml.etree.ElementTree`
  - Updates to :mod:`resource`
  - Updates to :mod:`subprocess`
  - Updates to :mod:`sys`
  - Re-generate :mod:`platform` example output on more modern systems.
  - Updates to :mod:`threading`
  - Updates to :mod:`dircache`

1.130

  - 10 Oct 2010, :mod:`random`
  - Updates to :mod:`contextlib`.
  - Updates to :mod:`logging`.
  - Updates to :mod:`mmap`.
  - Added more details about dialects to :mod:`csv`.
  - Updates to :mod:`difflib`.
  - Updates to :mod:`multiprocessing`.
  - Updates to :mod:`optparse`.
  - Updates to :mod:`pkgutil`.

1.129

  - 3 Oct 2010, :mod:`select`

1.128.1

  - 29 Sept 2010, Corrected the :class:`OrderedDict` equality example.

1.128

  - 28 Sept 2010, Updated :mod:`collections` to add
    :class:`OrderedDict` and :class:`Counter`, as well as the *rename*
    argument to :class:`namedtuple`.

1.127

  - 26 Sept 2010, :mod:`socket`

1.126

  - 19 Sept 2010, :mod:`sysconfig`

1.125

  - 12 Sept 2010, :mod:`pdb`

1.124.1

  - 9 Sept 2010, Updated packaging to fix installation errors.

1.124

  - 5 Sept 2010, :mod:`re`

1.123

  - 29 Aug 2010, :mod:`codecs`

1.122

  - 22 Aug 2010, :mod:`math`

1.121

  - 15 Aug 2010, :mod:`doctest`

1.120

  - 8 Aug 2010, :mod:`argparse`

1.119

  - 11 July 2010, :mod:`gc`

1.118.1

  - Updates to :mod:`locale`

1.118

  - Roberto Pauletto's Italian translation has moved to
    http://robyp.x10hosting.com/
  - 27 June 2010, :mod:`site`

1.117a

  - Added LifoQueue and PriorityQueue examples to :mod:`Queue`.
  - Completed an editing pass of the entire document, tweaking wording
    and formatting.

1.117
  - Updated :mod:`fileinput` example to use
    :mod:`xml.etree.ElementTree`.  Added an example to show how to get
    the filename and line number being processed.

1.116
  - 21 Mar 2010, :ref:`xml.etree.ElementTree.creating`
  - Fixed example in :ref:`abc-abstract-properties` so both the setter
    and getter work.  Thanks to Rune Hansen for pointing out the error
    in the original version.

1.115
  - 14 Mar 2010, :ref:`xml.etree.ElementTree.parsing`

1.114
  - 7 Mar 2010, :mod:`tabnanny`

1.113
  - 30 Jan 2010, :mod:`cgitb`
  - Added reference to presentation about using PyObjC to read/write
    binary plist files to :mod:`plist`.

1.112
  - 29 Nov 2009, :mod:`plistlib`

1.111.1
  - Clarify memory example based on comment from tartley.
  - Fix core dump detection in commands_getstatusoutput.py.  
    Thanks to Felix Labrecque for pointing out that it was wrong.

1.111
  - 23 Nov 2009, :mod:`sys`, continued with :ref:`sys-imports`

1.110
  - 15 Nov 2009, :mod:`sys`, continued with :ref:`sys-threads`

1.109
  - 8 Nov 2009, :mod:`sys`, continued with :ref:`sys-tracing`

1.108
  - 1 Nov 2009, :mod:`sys`, continued with :ref:`sys-exceptions`

1.107
  - 25 Oct 2009, :mod:`sys`, continued with :ref:`sys-limits`

1.106
  - 18 Oct 2009, :mod:`sys`, continued with :ref:`sys-runtime`

1.105
  - 12 Oct 2009, :mod:`sys` started with :ref:`sys-interpreter`

1.104
  - 20 Sept 2009, :mod:`resource`

1.103
  - 5 Sept 2009, :mod:`fractions`

1.102
  - 30 Aug 2009, :mod:`decimal`

1.101
  - 23 Aug 2009, :mod:`dis`

1.100
  - 9 Aug 2009, :mod:`pydoc`
  - Add pipes example to :mod:`subprocess`.
  - Add circular reference example to :mod:`pickle`.
  - Use the Sphinx text builder to create clean plaintext files for use with motw command line app.
  - Use :mod:`pydoc` ``pager()`` to show plaintext help from :ref:`motw-cli`.
  - Add built-in function ``motw()`` so that importing PyMOTW into your interactive session makes it easy to get to the examples interactively.  See :ref:`motw-interactive`.

1.99
  - 2 Aug 2009, Add :ref:`article-data-structures` article.

1.98
  - Added link to Roberto Pauletto's Italian translation.
  - 27 July 2009, Add :ref:`article-text-processing` article.

1.97
  - 19 July 2009, :mod:`urllib2`

1.96
  - 12 July 2009, :ref:`article-file-access`

1.95
  - 5 July 2009, :mod:`abc`
  - Rearrange packaging to install the HTML files.
  - Add ``motw`` command line app to show PyMOTW article on a given module, similar to pydoc.

1.94
  - Moved ``run_script()`` from pavement.py to `sphinxcontrib-paverutils <http://pypi.python.org/pypi/sphinxcontrib-paverutils>`_ 1.1.
  - 28 June 2009, :mod:`pyclbr`

1.93
  - 21 Jun 2009, :mod:`robotparser`

1.92
  - 14 June 2009, :mod:`gettext`
  - Added Windows info to :mod:`platform`, courtesy of Scott Lyons.
  - Added process group example to :mod:`subprocess`, courtesy of Scott Leerssen.

1.91
  - Add :ref:`article-data-persistence` article.
  - Correct link to library table of contents on python.org from about page.  Thanks to Tetsuya Morimoto for pointing out the broken link.
  - Add information about Tetsuya Morimoto's Japanese translation.
  - Add link to jsonpickle on :mod:`json` article, courtesy of Sebastien Binet.
  - Add time-stamps to HTML output
  - Remove extraneous javascript file from web html template to avoid 404 errors

1.90
  - 24 May 2009, :mod:`json`
  - updated daemon process examples in :mod:`multiprocessing`
  
1.89
  - 28 April 2009, :mod:`multiprocessing` (part 2, communication and MapReduce example)

1.88
  - 19 April 2009, :mod:`multiprocessing` (part 1, basic usage)
  - Upgraded to Python 2.6.2.
  - Add options to blog command in pavement.py to let the user specify alternate input and output file names for the blog HTML.
  - Added namedtuple example to :mod:`collections`.

1.87.1
  - Added dialect example to :mod:`csv` to show how to parse files with ``|``-delimited fields.

1.87
  - 5 Apr 2009, :mod:`pipes`
  - Converted PEP links to use ``pep`` role.
  - Converted RFC references to use ``rfc`` role.
  - Updated examples in :mod:`warnings` and :mod:`string` to work with changes in Python 2.6.1.

1.86.1
  - Updated working environment to use Paver 1.0b1.
  - Corrected errors in ``*.rst`` files identified by update to new version of Paver that doesn't let cog errors slide.
  - Added ignore_error option to run_script() in pavement.py so scripts with errors I'm expecting can be quietly ignored.
  - Finished converting all articles to use cog, where appropriate.

1.86
  - 14 Mar 2009, :mod:`asynchat`
  - Move to bitbucket.org for DVCS hosting
  - Updated description of ``uuid4()`` in :mod:`uuid` based on feedback via O'Reilly blog comment.

1.85
  - 1 Mar 2009, :mod:`asyncore`
  - Continue converting older articles to use cog.
  - Fix subprocess examples so they work if the permissions on the "child" scripts haven't been changed from the default way they are installed.

1.84
  - 22 Feb 2009, :mod:`tarfile`
  - Updated DictWriter example in :mod:`csv` based on feedback from Trilok Khairnar.
  - Cleaned up use of cog in a few older modules

1.83
  - 15 Feb 2009, :mod:`grp`
  - Continue converting older articles to use cog.

1.82
  - 8 Feb 2009, :mod:`pwd`
  - Fix ``set_unixfrom()`` examples in :mod:`mailbox` article based on feedback from Tom Lynn.
  - Add this history section

1.81
  - 18 Jan 2009, :mod:`compileall`

1.80    
  - 4 Jan 2009, :mod:`bz2`

1.79    
  - 28 Dec 2008, :mod:`zlib`.

1.78.1  
  - Updated :mod:`gzip` examples to avoid using built-in names for local variables.

1.78    
  - 7 Dec 2008, :mod:`gzip`.

1.77    
  - 30 Nov 2008, :mod:`readline` and :mod:`rlcompleter`

1.76    
  -  9 Nov 2008, :mod:`array`

1.75    
  - 2 Nov 2008, :mod:`struct`.

1.74.1  
  - Update formatting of several modules to make them more consistent.

1.74    
  - 19 Oct 2008, :mod:`smtpd`.

1.73    
  - 12 Oct 2008, :mod:`trace`

1.72    
  - 5 Oct 2008, :mod:`smtplib`

1.71    
  - 26 Sept 2008, :mod:`mailbox`

1.70.4  
  - Update formatting of several modules and fix the examples on the :mod:`difflib` page.

1.70.3  
  - 21 Sept 2008 :mod:`imaplib`

1.70.2  
  - 21 Sept 2008 :mod:`imaplib`

1.70.1  
  - 21 Sept 2008 :mod:`imaplib` (markup fixed).

1.70    
  - 21 Sept 2008, :mod:`imaplib`.

1.69    
  - 14 Sept 2008, :mod:`anydbm` and related modules.

1.68    
  - Sept 12, 2008, :mod:`exceptions`

1.67.1  
  - minor changes to accommodate site redesign

1.67    
  - 31 Aug 2008, overing :mod:`profile`, :mod:`cProfile`, and :mod:`pstats`.

1.66.1  
  - Fix a logic bug in the code that prints the currently registered signals.

1.66    
  - 17 Aug 2008, :mod:`signal`

1.65    
  - 10 Aug 2008, adding Sphinx-generated documentation all of the modules covered so far.

1.64    
  - 3 Aug 2008 :mod:`webbrowser`

1.63    
  - 27 July 2008, :mod:`uuid`

1.62    
  - 20 July 2008 :mod:`base64`.

1.61    
  - 6 July 2008, :mod:`xmlrpclib`.

1.60    
  - 29 June 2008, :mod:`SimpleXMLRPCServer`

1.59    
  - 22 June 2008, :mod:`warnings`

1.58    
  - 15 June 2008, :mod:`platform`

1.57    
  - 8 June 2008, :mod:`dircache`.

1.56    
  - 1 June 2008, :mod:`Cookie`

1.55    
  - 25 May 2008, :mod:`contextlib`

1.54    
  - 18 May 2008, :mod:`traceback`.

1.53    
  - 11 May 2008, :mod:`heapq`.

1.52    
  - 4 May 2008, :mod:`cmd`.

1.51    
  - 27 Apr 2008, :mod:`functools`.

1.50    
  - 20 Apr 2008, :mod:`filecmp`.

1.49    
  - 13 April 2008, :mod:`fnmatch`.

1.48    
  - 4 April 2008, :mod:`operator`.

1.47    
  - 30 March 2008, :mod:`urllib`.

1.46    
  - 23 March 2008, :mod:`collections`.

1.45    
  - PyCon 2008 edition for 16 Mar 2008, :mod:`datetime`.

1.44    
  - 9 Mar 2008, :mod:`time`

1.43    
  - 2 March 2008, :mod:`EasyDialogs`.

1.42    
  - 24 Feb 2008 :mod:`imp`.

1.41    
  - 17 Feb 2008, :mod:`pkgutil`.

1.40    
  - 10 Feb 2008, :mod:`tempfile`.

1.39    
  - 3 Feb 2008, :mod:`string`.

1.38    
  - 26 Jan 2008, :mod:`os.path`.

1.37    
  - 19 Jan 2008, :mod:`hashlib`.

1.36    
  - 13 Jan 2008, :mod:`threading`

1.35    
  - 6 Jan 2008, :mod:`weakref`.

1.34    
  - 30 Dec 2007, :mod:`mmap`.

1.33.1  
  - Correction for release 1.33 for 22 Dec 2007 the :mod:`zipimport` module.

1.33    
  - 22 Dec 2007, :mod:`zipimport`.

1.32    
  -  16 Dec 2007 :mod:`zipfile`.

1.31    
  - 9 Dec 2007, :mod:`BaseHTTPServer`

1.30    
  - Dec 2, 2007 :mod:`SocketServer`

1.29    
  - Nov 25, 2007 :mod:`inspect`.

1.28    
  - Nov 15, 2007 :mod:`urlparse`

1.27    
  - 10 Nov 2007, :mod:`pprint`

1.26    
  - 4 Nov 2007, :mod:`shutils`

1.25    
  - 28 Oct 2007, :mod:`commands`

1.24    
  - 20 Oct 2007, :mod:`itertools`

1.23    
  - Added another :mod:`difflib` example based on comments on that post.

1.22    
  - 14 Oct 2007, :mod:`shlex`.

1.21    
  - 7 Oct 2007, :mod:`difflib`.

1.20    
  - 30 Sept 2007, :mod:`copy`

1.19    
  - 25 Sept 2007, :mod:`sched`

1.18    
  -  20 September 2007, :mod:`timeit`

1.17    
  -  12 Sept 2007, :mod:`hmac`

1.16    
  - 3 Sept 2007, :mod:`unittest`

1.15    
  - 27 Aug, 2007 :mod:`optparse`.

1.14    
  -  20 Aug 2007, :mod:`csv`

1.13    
  - 12 Aug 2007, :mod:`getopt`.

1.12    
  - August 5, 2007, :mod:`shelve`

1.11    
  -  July 30, 2007, :mod:`glob`

1.10    
  -  July 22, 2007, :mod:`calendar`

1.9     
  -  July 15, 2007, :mod:`getpass`

1.8     
  -  July 8, 2007, :mod:`atexit`

1.7     
  -  July 1, 2007, :mod:`subprocess`

1.6     
  - June 24, 2007, :mod:`pickle`

1.5     
  - June 17, 2007, wrapping up the :mod:`os` module.

1.4     
  - June 10, 2007, :mod:`os` module files and directories.

1.3     
  -  June 3, 2007, continuing coverage of :mod:`os`

1.2     
  -  May 27, 2007, :mod:`os`

1.1     
  -  May 20, 2007, :mod:`locale`

1.0     
  - First packaged release, includes :mod:`fileinput`, :mod:`ConfigParser`, :mod:`Queue`, :mod:`StringIO`, :mod:`textwrap`, :mod:`linecache`, :mod:`bisect`, and :mod:`logging`.
