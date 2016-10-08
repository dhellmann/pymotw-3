Creating Custom Protocol Handlers
=================================

:mod:`urllib2` has built-in support for HTTP(S), FTP, and local file
access. To add support for other URL types, register another protocol
handler. For example, to support URLs pointing to arbitrary files on
remote NFS servers, without requiring users to mount the path before
accessing the file, create a class derived from :class:`BaseHandler`
and with a method :func:`nfs_open`.

The protocol-specific :func:`open` method is given a single argument, the
:class:`Request` instance, and it should return an object with a
:func:`read` method that can be used to read the data, an
:func:`info` method to return the response headers, and
:func:`geturl` to return the actual URL of the file being read. A
simple way to achieve that is to create an instance of
:class:`urllib.addurlinfo`, passing the headers, URL, and open file
handle in to the constructor.

.. literalinclude:: urllib2_nfs_handler.py
    :caption:
    :start-after: #end_pymotw_header

The :class:`FauxNFSHandler` and :class:`NFSFile` classes print
messages to illustrate where a real implementation would add mount and
unmount calls. Since this is just a simulation,
:class:`FauxNFSHandler` is primed with the name of a temporary
directory where it should look for all of its files.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'urllib2_nfs_handler.py'))
.. }}}

::

	$ python urllib2_nfs_handler.py

	FauxNFSHandler simulating mount:
	  Remote path: /path/to/the
	  Server     : remote_server
	  Local path : tmpoqqoAV
	  Filename   : file.txt
	
	READ CONTENTS: Contents of file.txt
	URL          : nfs://remote_server/path/to/the/file.txt
	HEADERS:
	  Content-length  = 20
	  Content-type    = text/plain
	NFSFile:
	  unmounting tmpoqqoAV
	  when file.txt is closed

.. {{{end}}}
