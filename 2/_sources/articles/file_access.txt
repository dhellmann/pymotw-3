.. _article-file-access:

###########
File Access
###########

Python's standard library includes a large range of tools for working with files, filenames, and file contents.

Filenames
=========

The first step in working with files is to get the name of the file so you can operate on it.  Python represents filenames as simple strings, but provides tools for building them from standard, platform-independent, components in :mod:`os.path`.  List the contents of a directory with ``listdir()`` from :mod:`os`, or use :mod:`glob` to build a list of filenames from a pattern.  Finer grained filtering of filenames is possible with :mod:`fnmatch`.  

Meta-data
=========

Once you know the name of the file, you may want to check other characteristics such as permissions or the file size using ``os.stat()`` and the constants in :mod:`stat`.

Reading Files
=============

If you're writing a filter application that processes text input line-by-line, :mod:`fileinput` provides an easy framework to get started.  The fileinput API calls for you to iterate over the ``input()`` generator, processing each line as it is yielded.  The generator handles parsing command line arguments for file names, or falling back to reading directly from ``sys.stdin``.  The result is a flexible tool your users can run directly on a file or as part of a pipeline.

If your app needs random access to files, :mod:`linecache` makes it easy to read lines by their line number.  The contents of the file are maintained in a cache, so be careful of memory consumption.

Temporary Files
===============

For cases where you need to create scratch files to hold data temporarily, or before moving it to a permanent location, :mod:`tempfile` will be very useful.  It provides classes to create temporary files and directories safely and securely.  Names are guaranteed not to collide, and include random components so they are not easily guessable.

Files and Directories
=====================

Frequently you need to work on a file as a whole, without worrying about what is in it.  The :mod:`shutil` module includes high-level file operations such as copying files and directories, setting permissions, etc.
