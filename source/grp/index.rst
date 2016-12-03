=============================
 grp --- UNIX Group Database
=============================

.. module:: grp
    :synopsis: UNIX Group Database

:Purpose: Read group data from UNIX group database.

The ``grp`` module can be used to read information about UNIX
groups from the group database (usually ``/etc/group``).  The
read-only interface returns tuple-like objects with named attributes
for the standard fields of a group record.

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

This example prints a report of all of the "real" groups on a system,
including their members (where "real" is defined as having a name not
starting with "``_``").  To load the entire password database, use
``getgrall()``.

.. literalinclude:: grp_getgrall.py
    :caption:
    :start-after: #end_pymotw_header

The return value is a list with an undefined order, so it needs to be
sorted before printing the report.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrall.py'))
.. }}}

.. code-block:: none

	$ python3 grp_getgrall.py
	
	34
	Name                            GID         Members            
	------------------------------- ----------- -------------------
	accessibility                            90                    
	admin                                    80 root               
	authedusers                              50                    
	bin                                       7                    
	certusers                                29 root, _jabber,
	                                            _postfix, _cyrus,
	                                            _calendar, _dovecot
	com.apple.access_disabled               396                    
	com.apple.access_ftp                    395                    
	com.apple.access_screensharing          398                    
	com.apple.access_sessionkey             397                    
	com.apple.access_ssh                    399                    
	com.apple.sharepoint.group.1            701 dhellmann          
	consoleusers                             53                    
	daemon                                    1 root               
	dialer                                   68                    
	everyone                                 12                    
	group                                    16                    
	interactusers                            51                    
	kmem                                      2 root               
	localaccounts                            61                    
	mail                                      6 _teamsserver       
	netaccounts                              62                    
	netusers                                 52                    
	network                                  69                    
	nobody                           4294967294                    
	nogroup                                  -1                    
	operator                                  5 root               
	owner                                    10                    
	procmod                                   9 root               
	procview                                  8 root               
	staff                                    20 root               
	sys                                       3 root               
	tty                                       4 root               
	utmp                                     45                    
	wheel                                     0 root               

.. {{{end}}}

Group Memberships for a User
============================

Another common task might be to print a list of all the groups for a
given user:

.. literalinclude:: grp_groups_for_user.py
    :caption:
    :start-after: #end_pymotw_header

The set of unique group names is sorted before they are printed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_groups_for_user.py'))
.. }}}

.. code-block:: none

	$ python3 grp_groups_for_user.py
	
	dhellmann belongs to: _appserveradm, _appserverusr, _lpadmin, ad
	min, com.apple.sharepoint.group.1

.. {{{end}}}

Finding a Group By Name
=======================

As with :mod:`pwd`, it is also possible to query for information about
a specific group, either by name or numeric id.

.. literalinclude:: grp_getgrnam.py
    :caption:
    :start-after: #end_pymotw_header

The ``admin`` group has two members:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrnam.py'))
.. }}}

.. code-block:: none

	$ python3 grp_getgrnam.py
	
	Name    : admin
	GID     : 80
	Password: *
	Members : root, dhellmann

.. {{{end}}}

Finding a Group by ID
=====================

To identify the group running the current process, combine
``getgrgid()`` with ``os.getgid()``.

.. literalinclude:: grp_getgrgid_process.py
    :caption:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrgid_process.py'))
.. }}}

.. code-block:: none

	$ python3 grp_getgrgid_process.py
	
	Currently running with GID=20 name=staff

.. {{{end}}}

And to get the group name based on the permissions on a file, look up
the group returned by :func:`os.stat`.

.. literalinclude:: grp_getgrgid_fileowner.py
    :caption:
    :start-after: #end_pymotw_header

The file status record includes ownership and permission data for the
file or directory.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'grp_getgrgid_fileowner.py'))
.. }}}

.. code-block:: none

	$ python3 grp_getgrgid_fileowner.py
	
	grp_getgrgid_fileowner.py is owned by staff (20)

.. {{{end}}}


.. seealso::

    * :pydoc:`grp`

    * :mod:`pwd` -- Read user data from the password database.

    * :mod:`spwd` -- Read user data from the shadow password database.

    * :mod:`os` -- Operating system interfaces.
