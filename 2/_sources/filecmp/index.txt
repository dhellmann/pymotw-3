========================
filecmp -- Compare files
========================

.. module:: filecmp
    :synopsis: Compare files and directories on the filesystem.

:Purpose: Compare files and directories on the filesystem.
:Available In: 2.1 and later

Example Data
============

The examples in the discussion below use a set of test files created by ``filecmp_mkexamples.py``.

.. include:: filecmp_mkexamples.py
    :literal:
    :start-after: #end_pymotw_header

.. We don't care about the output of the script that creates the example files.
.. {{{cog
.. workdir = path(cog.inFile).dirname()
.. examples = workdir / 'example'
.. examples.rmtree()
.. examples.mkdir()
.. mkexamples = workdir / 'filecmp_mkexamples.py'
.. sh('python %s' % mkexamples)
.. }}}
.. {{{end}}}


::

    $ ls -Rlast example
    total 0
    0 drwxr-xr-x  4 dhellmann  dhellmann  136 Apr 20 17:04 .
    0 drwxr-xr-x  9 dhellmann  dhellmann  306 Apr 20 17:04 ..
    0 drwxr-xr-x  8 dhellmann  dhellmann  272 Apr 20 17:04 dir1
    0 drwxr-xr-x  8 dhellmann  dhellmann  272 Apr 20 17:04 dir2

    example/dir1:
    total 32
    0 drwxr-xr-x  8 dhellmann  dhellmann  272 Apr 20 17:04 .
    0 drwxr-xr-x  4 dhellmann  dhellmann  136 Apr 20 17:04 ..
    0 drwxr-xr-x  2 dhellmann  dhellmann   68 Apr 20 17:04 common_dir
    8 -rw-r--r--  1 dhellmann  dhellmann   21 Apr 20 17:04 common_file
    0 drwxr-xr-x  2 dhellmann  dhellmann   68 Apr 20 17:04 dir_only_in_dir1
    8 -rw-r--r--  1 dhellmann  dhellmann   22 Apr 20 17:04 file_in_dir1
    8 -rw-r--r--  1 dhellmann  dhellmann   22 Apr 20 17:04 file_only_in_dir1
    8 -rw-r--r--  1 dhellmann  dhellmann   17 Apr 20 17:04 not_the_same

    example/dir2:
    total 24
    0 drwxr-xr-x  8 dhellmann  dhellmann  272 Apr 20 17:04 .
    0 drwxr-xr-x  4 dhellmann  dhellmann  136 Apr 20 17:04 ..
    0 drwxr-xr-x  2 dhellmann  dhellmann   68 Apr 20 17:04 common_dir
    8 -rw-r--r--  1 dhellmann  dhellmann   21 Apr 20 17:04 common_file
    0 drwxr-xr-x  2 dhellmann  dhellmann   68 Apr 20 17:04 dir_only_in_dir2
    0 drwxr-xr-x  2 dhellmann  dhellmann   68 Apr 20 17:04 file_in_dir1
    8 -rw-r--r--  1 dhellmann  dhellmann   22 Apr 20 17:04 file_only_in_dir2
    8 -rw-r--r--  1 dhellmann  dhellmann   17 Apr 20 17:04 not_the_same

The same directory structure is repeated one time under the "common_dir"
directories to give interesting recursive comparison options.

Comparing Files
===============

The filecmp module includes functions and a class for comparing files and
directories on the filesystem. If you need to compare two files, use the cmp()
function.

.. include:: filecmp_cmp.py
    :literal:
    :start-after: #end_pymotw_header

By default, cmp() looks only at the information available from os.stat(). The
shallow argument tells cmp() whether to look at the contents of the file, as
well. The default is to perform a shallow comparison, without looking inside
the files. Notice that files of the same size created at the same time seem to
be the same if their contents are not compared.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_cmp.py'))
.. }}}

::

	$ python filecmp_cmp.py
	
	common_file: True True
	not_the_same: True False
	identical: True True

.. {{{end}}}


To compare a set of files in two directories without recursing, use
filecmp.cmpfiles(). The arguments are the names of the directories and a list
of files to be checked in the two locations. The list of common files should
contain only filenames (directories always result in a mismatch) and
the files must be present in both locations. The code below shows a simple way
to build the common list. If you have a shorter formula, post it in the
comments. The comparison also takes the shallow flag, just as with cmp().

.. include:: filecmp_cmpfiles.py
    :literal:
    :start-after: #end_pymotw_header

cmpfiles() returns three lists of filenames for files that match, files that
do not match, and files that could not be compared (due to permission problems
or for any other reason).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_cmpfiles.py'))
.. }}}

::

	$ python filecmp_cmpfiles.py
	
	Common files: ['not_the_same', 'file_in_dir1', 'common_file']
	Match: ['not_the_same', 'common_file']
	Mismatch: ['file_in_dir1']
	Errors: []

.. {{{end}}}


Using dircmp
============

The functions described above are suitable for relatively simple comparisons,
but for recursive comparison of large directory trees or for more complete
analysis, the dircmp class is more useful. In its simplest use case, you can
print a report comparing two directories with the report() method:

.. include:: filecmp_dircmp_report.py
    :literal:
    :start-after: #end_pymotw_header

The output is a plain-text report showing the results of just the
contents of the directories given, without recursing. In this case,
the file "not_the_same" is thought to be the same because the contents
are not being compared. There is no way to have dircmp compare the
contents of files like cmp() can.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_report.py'))
.. }}}

::

	$ python filecmp_dircmp_report.py
	
	diff example/dir1 example/dir2
	Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
	Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
	Identical files : ['common_file', 'not_the_same']
	Common subdirectories : ['common_dir']
	Common funny cases : ['file_in_dir1']

.. {{{end}}}

For more detail, and a recursive comparison, use report_full_closure():

.. include:: filecmp_dircmp_report_full_closure.py
    :literal:
    :start-after: #end_pymotw_header

The output includes comparisons of all parallel subdirectories.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_report_full_closure.py'))
.. }}}

::

	$ python filecmp_dircmp_report_full_closure.py
	
	diff example/dir1 example/dir2
	Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
	Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
	Identical files : ['common_file', 'not_the_same']
	Common subdirectories : ['common_dir']
	Common funny cases : ['file_in_dir1']
	
	diff example/dir1/common_dir example/dir2/common_dir
	Common subdirectories : ['dir1', 'dir2']
	
	diff example/dir1/common_dir/dir2 example/dir2/common_dir/dir2
	Identical files : ['common_file', 'file_only_in_dir2', 'not_the_same']
	Common subdirectories : ['common_dir', 'dir_only_in_dir2', 'file_in_dir1']
	
	diff example/dir1/common_dir/dir2/common_dir example/dir2/common_dir/dir2/common_dir
	
	diff example/dir1/common_dir/dir2/dir_only_in_dir2 example/dir2/common_dir/dir2/dir_only_in_dir2
	
	diff example/dir1/common_dir/dir2/file_in_dir1 example/dir2/common_dir/dir2/file_in_dir1
	
	diff example/dir1/common_dir/dir1 example/dir2/common_dir/dir1
	Identical files : ['common_file', 'file_in_dir1', 'file_only_in_dir1', 'not_the_same']
	Common subdirectories : ['common_dir', 'dir_only_in_dir1']
	
	diff example/dir1/common_dir/dir1/common_dir example/dir2/common_dir/dir1/common_dir
	
	diff example/dir1/common_dir/dir1/dir_only_in_dir1 example/dir2/common_dir/dir1/dir_only_in_dir1

.. {{{end}}}

Using differences in your program
=================================

Besides producing printed reports, dircmp calculates useful lists of files you
can use in your programs directly. Each of the following attributes is
calculated only when requested, so instantiating a dircmp does not incur a lot
of extra overhead.

The files and subdirectories contained in the directories being compared are
listed in left_list and right_list:

.. include:: filecmp_dircmp_list.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_list.py'))
.. }}}

::

	$ python filecmp_dircmp_list.py
	
	Left : ['common_dir', 'common_file', 'dir_only_in_dir1', 'file_in_dir1', 'file_only_in_dir1', 'not_the_same']
	Right: ['common_dir', 'common_file', 'dir_only_in_dir2', 'file_in_dir1', 'file_only_in_dir2', 'not_the_same']

.. {{{end}}}

The inputs can be filtered by passing a list of names to ignore to the
constructor. By default the names RCS, CVS, and tags are ignored.

.. include:: filecmp_dircmp_list_filter.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the "common_file" is left out of the list of files to be
compared.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_list_filter.py'))
.. }}}

::

	$ python filecmp_dircmp_list_filter.py
	
	Left : ['common_dir', 'dir_only_in_dir1', 'file_in_dir1', 'file_only_in_dir1', 'not_the_same']
	Right: ['common_dir', 'dir_only_in_dir2', 'file_in_dir1', 'file_only_in_dir2', 'not_the_same']

.. {{{end}}}

The set of files common to both input directories is maintained in common, and
the files unique to each directory are listed in left_only, and right_only.

.. include:: filecmp_dircmp_membership.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_membership.py'))
.. }}}

::

	$ python filecmp_dircmp_membership.py
	
	Common: ['not_the_same', 'common_file', 'file_in_dir1', 'common_dir']
	Left  : ['dir_only_in_dir1', 'file_only_in_dir1']
	Right : ['dir_only_in_dir2', 'file_only_in_dir2']

.. {{{end}}}

The common members can be further broken down into files, directories and
"funny" items (anything that has a different type in the two directories or
where there is an error from os.stat()).

.. include:: filecmp_dircmp_common.py
    :literal:
    :start-after: #end_pymotw_header

In the example data, the item named "file_in_dir1" is a file in one directory
and a subdirectory in the other, so it shows up in the "funny" list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_common.py'))
.. }}}

::

	$ python filecmp_dircmp_common.py
	
	Common     : ['not_the_same', 'common_file', 'file_in_dir1', 'common_dir']
	Directories: ['common_dir']
	Files      : ['not_the_same', 'common_file']
	Funny      : ['file_in_dir1']

.. {{{end}}}

The differences between files are broken down similarly:

.. include:: filecmp_dircmp_diff.py
    :literal:
    :start-after: #end_pymotw_header

Remember, the file "not_the_same" is only being compared via os.stat, and the contents are not examined.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_diff.py'))
.. }}}

::

	$ python filecmp_dircmp_diff.py
	
	Same      : ['not_the_same', 'common_file']
	Different : []
	Funny     : []

.. {{{end}}}

Finally, the subdirectories are also mapped to new dircmp objects in the
attribute subdirs to allow easy recursive comparison.

.. include:: filecmp_dircmp_subdirs.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python filecmp_dircmp_subdirs.py
    Subdirectories:
    {'common_dir': <filecmp.dircmp instance at 0x85da0>}

.. seealso::

    `filecmp <http://docs.python.org/2.7/library/filecmp.html>`_
        The standard library documentation for this module.

    :ref:`os-directories` from :mod:`os`
        Listing the contents of a directory.

    :mod:`difflib`
        Computing the differences between two sequences.
