================================
 pwd --- Unix Password Database
================================

.. module:: pwd
    :synopsis: Unix Password Database

:Purpose: Read user data from Unix password database.

The ``pwd`` module can be used to read user information from the
Unix password database (usually ``/etc/passwd``).  The read-only
interface returns tuple-like objects with named attributes for the
standard fields of a password record.

===== ============= =======
Index Attribute     Meaning
===== ============= =======
 0    ``pw_name``   The user's login name
 1    ``pw_passwd`` Encrypted password (optional)
 2    ``pw_uid``    User id (integer)
 3    ``pw_gid``    Group id (integer)
 4    ``pw_gecos``  Comment/full name
 5    ``pw_dir``    Home directory
 6    ``pw_shell``  Application started on login, usually a command interpreter
===== ============= =======

Querying All Users
==================

This example prints a report of all of the "real" users on a system,
including their home directories (where "real" is defined as having a
name not starting with "``_``").  To load the entire password
database, use ``getpwall()``.  The return value is a list with an
undefined order, so it needs to be sorted before the report is
printed.

.. literalinclude:: pwd_getpwall.py
    :caption:
    :start-after: #end_pymotw_header

Most of the example code above deals with formatting the results
nicely.  The ``for`` loop at the end shows how to access fields from
the records by name.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pwd_getpwall.py', break_lines_at=68))
.. }}}

.. code-block:: none

	$ python3 pwd_getpwall.py
	
	User               UID Home Dir          Description
	---------- ----------- ----------------- --------------------
	Guest              201 /Users/Guest      Guest User
	daemon               1 /var/root         System Services
	daemon               1 /var/root         System Services
	dhellmann          501 /Users/dhellmann  Doug Hellmann
	nobody      4294967294 /var/empty        Unprivileged User
	nobody      4294967294 /var/empty        Unprivileged User
	root                 0 /var/root         System Administrator
	root                 0 /var/root         System Administrator

.. {{{end}}}


Querying User By Name
=====================

To read information about one user it is not necessary to read the
entire password database.  Use ``getpwnam()``, to retrieve the
information about a user by name.

.. literalinclude:: pwd_getpwnam.py
    :caption:
    :start-after: #end_pymotw_header

The passwords on the system where this example was run are stored
outside of the main user database in a shadow file, so the password
field, when set, is reported as all ``*``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pwd_getpwnam.py dhellmann'))
.. cog.out(run_script(cog.inFile, 'pwd_getpwnam.py nobody', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 pwd_getpwnam.py dhellmann
	
	Username: dhellmann
	Password: ********
	Comment : Doug Hellmann
	UID/GID : 501 / 20
	Home    : /Users/dhellmann
	Shell   : /bin/bash

	$ python3 pwd_getpwnam.py nobody
	
	Username: nobody
	Password: *
	Comment : Unprivileged User
	UID/GID : 4294967294 / 4294967294
	Home    : /var/empty
	Shell   : /usr/bin/false

.. {{{end}}}


Querying User By UID
====================

It is also possible to look up a user by their numerical user id.
This is useful to find the owner of a file:

.. literalinclude:: pwd_getpwuid_fileowner.py
    :caption:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pwd_getpwuid_fileowner.py'))
.. }}}

.. code-block:: none

	$ python3 pwd_getpwuid_fileowner.py
	
	pwd_getpwuid_fileowner.py is owned by dhellmann (501)

.. {{{end}}}


The numeric user id is can also be used to find information about the
user currently running a process:

.. literalinclude:: pwd_getpwuid_process.py
    :caption:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'pwd_getpwuid_process.py'))
.. }}}

.. code-block:: none

	$ python3 pwd_getpwuid_process.py
	
	Currently running with UID=501 username=dhellmann

.. {{{end}}}


.. seealso::

    * :pydoc:`pwd`

    * :mod:`spwd` -- Secure password database access for systems using
      shadow passwords.

    * :mod:`grp` -- The :mod:`grp` module reads Unix group
      information.
