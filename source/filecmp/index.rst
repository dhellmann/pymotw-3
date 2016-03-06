==========================
 filecmp -- Compare Files
==========================

.. module:: filecmp
    :synopsis: Compare files and directories on the file system.

:Purpose: Compare files and directories on the file system.
:Python Version: 2.1 and later

The :mod:`filecmp` module includes functions and a class for comparing
files and directories on the file system.

Example Data
============

The examples in this discussion use a set of test files created by
``filecmp_mkexamples.py``.

.. include:: filecmp_mkexamples.py
    :literal:
    :start-after: #end_pymotw_header

.. We don't care about the output of the script that creates the
.. example files, so run it, but don't include the output.
.. {{{cog
.. examples = path(cog.inFile).dirname() / 'example'
.. examples.rmtree()
.. examples.mkdir()
.. run_script(cog.inFile, 'filecmp_mkexamples.py')
.. }}}
.. {{{end}}}

Running ``filecmp_mkexamples.py`` produces a tree of files under the
directory ``example``:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'find example', interpreter=None))
.. }}}

::

	$ find example

	example
	example/dir1
	example/dir1/common_dir
	example/dir1/common_dir/dir1
	example/dir1/common_dir/dir1/common_dir
	example/dir1/common_dir/dir1/common_file
	example/dir1/common_dir/dir1/dir_only_in_dir1
	example/dir1/common_dir/dir1/file_in_dir1
	example/dir1/common_dir/dir1/file_only_in_dir1
	example/dir1/common_dir/dir1/not_the_same
	example/dir1/common_dir/dir2
	example/dir1/common_dir/dir2/common_dir
	example/dir1/common_dir/dir2/common_file
	example/dir1/common_dir/dir2/dir_only_in_dir2
	example/dir1/common_dir/dir2/file_in_dir1
	example/dir1/common_dir/dir2/file_only_in_dir2
	example/dir1/common_dir/dir2/not_the_same
	example/dir1/common_file
	example/dir1/dir_only_in_dir1
	example/dir1/file_in_dir1
	example/dir1/file_only_in_dir1
	example/dir1/not_the_same
	example/dir2
	example/dir2/common_dir
	example/dir2/common_dir/dir1
	example/dir2/common_dir/dir1/common_dir
	example/dir2/common_dir/dir1/common_file
	example/dir2/common_dir/dir1/dir_only_in_dir1
	example/dir2/common_dir/dir1/file_in_dir1
	example/dir2/common_dir/dir1/file_only_in_dir1
	example/dir2/common_dir/dir1/not_the_same
	example/dir2/common_dir/dir2
	example/dir2/common_dir/dir2/common_dir
	example/dir2/common_dir/dir2/common_file
	example/dir2/common_dir/dir2/dir_only_in_dir2
	example/dir2/common_dir/dir2/file_in_dir1
	example/dir2/common_dir/dir2/file_only_in_dir2
	example/dir2/common_dir/dir2/not_the_same
	example/dir2/common_file
	example/dir2/dir_only_in_dir2
	example/dir2/file_in_dir1
	example/dir2/file_only_in_dir2
	example/dir2/not_the_same

.. {{{end}}}

The same directory structure is repeated one time under the "``common_dir``"
directories to give interesting recursive comparison options.

Comparing Files
===============

:func:`cmp` compares two files on the file system.

.. include:: filecmp_cmp.py
    :literal:
    :start-after: #end_pymotw_header


The *shallow* argument tells :func:`cmp` whether to look at the
contents of the file, in addition to its metadata. The default is to
perform a shallow comparison using the information available from
:func:`os.stat` without looking at content.  Files of the same
size created at the same time are reported as the same, if their
contents are not compared.

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
:func:`cmpfiles`. The arguments are the names of the directories and a
list of files to be checked in the two locations. The list of common
files passed in should contain only filenames (directories always result in a
mismatch) and the files must be present in both locations. The next
example shows a simple way to build the common list. The comparison
also takes the *shallow* flag, just as with :func:`cmp`.

.. include:: filecmp_cmpfiles.py
    :literal:
    :start-after: #end_pymotw_header

:func:`cmpfiles` returns three lists of filenames containing files
that match, files that do not match, and files that could not be
compared (due to permission problems or for any other reason).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_cmpfiles.py'))
.. }}}

::

	$ python filecmp_cmpfiles.py

	Common files: ['not_the_same', 'file_in_dir1', 'common_file']
	Match   : ['not_the_same', 'common_file']
	Mismatch: ['file_in_dir1']
	Errors  : []

.. {{{end}}}


Comparing Directories
=====================

The functions described earlier are suitable for relatively simple
comparisons.  For recursive comparison of large directory trees or
for more complete analysis, the :class:`dircmp` class is more
useful. In its simplest use case, :func:`report` prints a report
comparing two directories.

.. include:: filecmp_dircmp_report.py
    :literal:
    :start-after: #end_pymotw_header

The output is a plain-text report showing the results of just the
contents of the directories given, without recursing. In this case,
the file "``not_the_same``" is thought to be the same because the contents
are not being compared. There is no way to have :mod:`dircmp` compare
the contents of files like :func:`cmp` does.

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

For more detail, and a recursive comparison, use
:func:`report_full_closure`:

.. include:: filecmp_dircmp_report_full_closure.py
    :literal:
    :start-after: #end_pymotw_header

The output includes comparisons of all parallel subdirectories.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_report_full_closure.py', break_lines_at=69))
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
	Identical files : ['common_file', 'file_only_in_dir2', 'not_the_same'
	]
	Common subdirectories : ['common_dir', 'dir_only_in_dir2', 'file_in_d
	ir1']
	
	diff example/dir1/common_dir/dir2/common_dir example/dir2/common_dir/
	dir2/common_dir
	
	diff example/dir1/common_dir/dir2/dir_only_in_dir2 example/dir2/commo
	n_dir/dir2/dir_only_in_dir2
	
	diff example/dir1/common_dir/dir2/file_in_dir1 example/dir2/common_di
	r/dir2/file_in_dir1
	
	diff example/dir1/common_dir/dir1 example/dir2/common_dir/dir1
	Identical files : ['common_file', 'file_in_dir1', 'file_only_in_dir1'
	, 'not_the_same']
	Common subdirectories : ['common_dir', 'dir_only_in_dir1']
	
	diff example/dir1/common_dir/dir1/common_dir example/dir2/common_dir/
	dir1/common_dir
	
	diff example/dir1/common_dir/dir1/dir_only_in_dir1 example/dir2/commo
	n_dir/dir1/dir_only_in_dir1

.. {{{end}}}

Using Differences in a Program
==============================

Besides producing printed reports, :class:`dircmp` calculates lists of
files that can be used in programs directly. Each of the following
attributes is calculated only when requested, so creating a
:class:`dircmp` instance does not incur overhead for unused data.

.. include:: filecmp_dircmp_list.py
    :literal:
    :start-after: #end_pymotw_header

The files and subdirectories contained in the directories being
compared are listed in :attr:`left_list` and :attr:`right_list`.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_list.py'))
.. }}}

::

	$ python filecmp_dircmp_list.py

	Left:
	['common_dir',
	 'common_file',
	 'dir_only_in_dir1',
	 'file_in_dir1',
	 'file_only_in_dir1',
	 'not_the_same']
	
	Right:
	['common_dir',
	 'common_file',
	 'dir_only_in_dir2',
	 'file_in_dir1',
	 'file_only_in_dir2',
	 'not_the_same']

.. {{{end}}}

The inputs can be filtered by passing a list of names to ignore to the
constructor. By default the names ``RCS``, ``CVS``, and ``tags`` are
ignored.

.. include:: filecmp_dircmp_list_filter.py
    :literal:
    :start-after: #end_pymotw_header

In this case, the "``common_file``" is left out of the list of files to be
compared.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_list_filter.py', break_lines_at=79))
.. }}}

::

	$ python filecmp_dircmp_list_filter.py

	Left:
	['common_dir',
	 'dir_only_in_dir1',
	 'file_in_dir1',
	 'file_only_in_dir1',
	 'not_the_same']
	
	Right:
	['common_dir',
	 'dir_only_in_dir2',
	 'file_in_dir1',
	 'file_only_in_dir2',
	 'not_the_same']

.. {{{end}}}

The names of files common to both input directories are saved in
:attr:`common`, and the files unique to each directory are listed in
:attr:`left_only`, and :attr:`right_only`.  

.. include:: filecmp_dircmp_membership.py
    :literal:
    :start-after: #end_pymotw_header

The "left" directory is the first argument to :func:`dircmp` and the
"right" directory is the second.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_membership.py'))
.. }}}

::

	$ python filecmp_dircmp_membership.py

	Common:
	['not_the_same', 'common_file', 'file_in_dir1', 'common_dir']
	
	Left:
	['dir_only_in_dir1', 'file_only_in_dir1']
	
	Right:
	['dir_only_in_dir2', 'file_only_in_dir2']

.. {{{end}}}

The common members can be further broken down into files, directories
and "funny" items (anything that has a different type in the two
directories or where there is an error from :func:`os.stat`).

.. include:: filecmp_dircmp_common.py
    :literal:
    :start-after: #end_pymotw_header

In the example data, the item named "``file_in_dir1``" is a file in one
directory and a subdirectory in the other, so it shows up in the
funny list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_common.py'))
.. }}}

::

	$ python filecmp_dircmp_common.py

	Common:
	['not_the_same', 'common_file', 'file_in_dir1', 'common_dir']
	
	Directories:
	['common_dir']
	
	Files:
	['not_the_same', 'common_file']
	
	Funny:
	['file_in_dir1']

.. {{{end}}}

The differences between files are broken down similarly.

.. include:: filecmp_dircmp_diff.py
    :literal:
    :start-after: #end_pymotw_header

The file ``not_the_same`` is only being compared via :func:`os.stat`,
and the contents are not examined, so it is included in the
:attr:`same_files` list.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'filecmp_dircmp_diff.py'))
.. }}}

::

	$ python filecmp_dircmp_diff.py

	Same      : ['not_the_same', 'common_file']
	Different : []
	Funny     : []

.. {{{end}}}

Finally, the subdirectories are also saved to allow easy recursive
comparison.

.. include:: filecmp_dircmp_subdirs.py
    :literal:
    :start-after: #end_pymotw_header

The attribute :attr:`subdirs` is a dictionary mapping the directory
name to new :class:`dircmp` objects.

::

    $ python filecmp_dircmp_subdirs.py

    Subdirectories:
    {'common_dir': <filecmp.dircmp instance at 0x85da0>}

.. seealso::

    `filecmp <http://docs.python.org/library/filecmp.html>`_
        The standard library documentation for this module.

    :ref:`os-directories`
        Listing the contents of a directory using :mod:`os`.

    :mod:`difflib`
        Computing the differences between two sequences.
