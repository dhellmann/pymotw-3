===========================
grp -- Unix Group Database
===========================

.. module:: grp
    :synopsis: Unix Group Database

:Purpose: Read group data from Unix group database.
:Available In: 1.4 and later

The grp module can be used to read information about Unix groups from
the group database (usually ``/etc/group``).  The read-only interface
returns tuple-like objects with named attributes for the standard
fields of a group record.

===== ========= =======
Index Attribute Meaning
===== ========= =======
 0    gr_name   Name
 1    gr_passwd Password, if any (encrypted)
 2    gr_gid    Numerical id (integer)
 3    gr_mem    Names of group members
===== ========= =======

The name and password values are both strings, the GID is an integer,
and the members are reported as a list of strings.

Querying All Groups
===================

Suppose you need to print a report of all of the "real" groups on a
system, including their members (for our purposes, "real" is defined
as having a name not starting with "``_``").  To load the entire
password database, you would use ``getgrall()``.  The return value is
a list with an undefined order, so you probably want to sort it before
printing the report.

.. include:: grp_getgrall.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrall.py'))
.. }}}

::

	$ python grp_getgrall.py
	
	Name                                      GID   Password Members
	---------------------------------------- ---- ---------- ------------------------------
	accessibility                              90          * 
	accessibility                              90          * 
	admin                                      80          * root, dhellmann
	admin                                      80          * root
	authedusers                                50          * 
	authedusers                                50          * 
	bin                                         7          * 
	bin                                         7          * 
	certusers                                  29          * root, _jabber, _postfix, _cyrus, _calendar, _dovecot
	certusers                                  29          * root, _jabber, _postfix, _cyrus, _calendar, _dovecot
	com.apple.access_screensharing            401            dhellmann
	com.apple.access_screensharing-disabled   101            dhellmann
	com.apple.access_ssh                      102            dhellmann
	consoleusers                               53          * 
	consoleusers                               53          * 
	daemon                                      1          * root
	daemon                                      1          * root
	dhellmann                                 501            
	dialer                                     68          * 
	dialer                                     68          * 
	everyone                                   12          * 
	everyone                                   12          * 
	group                                      16          * 
	group                                      16          * 
	interactusers                              51          * 
	interactusers                              51          * 
	kmem                                        2          * root
	kmem                                        2          * root
	localaccounts                              61          * 
	localaccounts                              61          * 
	mail                                        6          * _teamsserver
	mail                                        6          * _teamsserver
	netaccounts                                62          * 
	netaccounts                                62          * 
	netusers                                   52          * 
	netusers                                   52          * 
	network                                    69          * 
	network                                    69          * 
	nobody                                   4294967294          * 
	nobody                                   4294967294          * 
	nogroup                                  4294967295          * 
	nogroup                                  4294967295          * 
	operator                                    5          * root
	operator                                    5          * root
	owner                                      10          * 
	owner                                      10          * 
	procmod                                     9          * root
	procmod                                     9          * root
	procview                                    8          * root
	procview                                    8          * root
	racemi                                    500            dhellmann
	smmsp                                     103          * 
	staff                                      20          * root
	staff                                      20          * root
	sys                                         3          * root
	sys                                         3          * root
	tty                                         4          * root
	tty                                         4          * root
	utmp                                       45          * 
	utmp                                       45          * 
	wheel                                       0          * root
	wheel                                       0          * root

.. {{{end}}}

Group Memberships for a User
============================

Another common task might be to print a list of all the groups for a
given user:

.. include:: grp_groups_for_user.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_groups_for_user.py'))
.. }}}

::

	$ python grp_groups_for_user.py
	
	dhellmann belongs to: _lpadmin, admin, com.apple.access_screensharing-disabled, com.apple.access_screensharing, com.apple.access_ssh, racemi

.. {{{end}}}

Finding a Group By Name
=======================

As with :mod:`pwd`, it is also possible to query for information about
a specific group, either by name or numeric id.

.. include:: grp_getgrnam.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrnam.py'))
.. }}}

::

	$ python grp_getgrnam.py
	
	Name    : admin
	GID     : 80
	Password: *
	Members : root, dhellmann

.. {{{end}}}

Finding a Group by ID
=====================

To identify the group running the current process, combine
``getgrgid()`` with ``os.getgid()``.

.. include:: grp_getgrgid_process.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrgid_process.py'))
.. }}}

::

	$ python grp_getgrgid_process.py
	
	Currently running with GID=501 name=dhellmann

.. {{{end}}}

And to get the group name based on the permissions on a file, look up
the group returned by ``os.stat()``.

.. include:: grp_getgrgid_fileowner.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrgid_fileowner.py'))
.. }}}

::

	$ python grp_getgrgid_fileowner.py
	
	grp_getgrgid_fileowner.py is owned by dhellmann (501)

.. {{{end}}}


.. seealso::

    `grp <http://docs.python.org/2.7/library/grp.html>`_
        The standard library documentation for this module.

    :mod:`pwd`
        Read user data from the password database.

    :mod:`spwd`
        Read user data from the shadow password database.
