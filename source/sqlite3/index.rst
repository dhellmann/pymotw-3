==========================================
 sqlite3 --- Embedded Relational Database
==========================================

.. module:: sqlite3
    :synopsis: Embedded relational database

:Purpose: Implements an embedded relational database with SQL support.

The :mod:`sqlite3` module provides a DB-API 2.0 compliant interface to
SQLite, an in-process relational database.  SQLite is designed to be
embedded in applications, instead of using a separate database server
program such as MySQL, PostgreSQL, or Oracle.  It is fast, rigorously
tested, and flexible, making it suitable for prototyping and
production deployment for some applications.

Creating a Database
===================

An SQLite database is stored as a single file on the file system.  The
library manages access to the file, including locking it to prevent
corruption when multiple writers use it.  The database is created the
first time the file is accessed, but the application is responsible
for managing the table definitions, or *schema*, within the database.

This example looks for the database file before opening it with
:func:`connect` so it knows when to create the schema for new
databases.

.. literalinclude:: sqlite3_createdb.py
   :caption:
   :start-after: #end_pymotw_header

Running the script twice shows that it creates the empty file if it
does not exist.

.. {{{cog
.. run_script(cog.inFile, 'rm -f todo.db', interpreter='')
.. cog.out(run_script(cog.inFile, 'ls *.db', interpreter='', ignore_error=True))
.. cog.out(run_script(cog.inFile, 'sqlite3_createdb.py', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'ls *.db', interpreter='', include_prefix=False))
.. cog.out(run_script(cog.inFile, 'sqlite3_createdb.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ ls *.db
	
	ls: *.db: No such file or directory

	$ python3 sqlite3_createdb.py
	
	Need to create schema

	$ ls *.db
	
	todo.db

	$ python3 sqlite3_createdb.py
	
	Database exists, assume schema does, too.

.. {{{end}}}

After creating the new database file, the next step is to create the
schema to define the tables within the database.  The remaining
examples in this section all use the same database schema with tables
for managing tasks.  The details of the database schema are presented
in :table:`The "project" Table` and :table:`The "task" Table`.

.. table:: The "project" Table

  ===========  ====  ===========
  Column       Type  Description
  ===========  ====  ===========
  name         text  Project name
  description  text  Long project description
  deadline     date  Due date for the entire project
  ===========  ====  ===========

.. table:: The "task" Table

  ===============  =======  ===========
  Column           Type     Description
  ===============  =======  ===========
  id               number   Unique task identifier
  priority         integer  Numerical priority, lower is more important
  details          text     Full task details
  status           text     Task status (one of 'new', 'pending', 'done', or 'canceled').
  deadline         date     Due date for this task
  completed_on     date     When the task was completed.
  project          text     The name of the project for this task.
  ===============  =======  ===========

The *data definition language* (DDL) statements to create the tables
are:

.. literalinclude:: todo_schema.sql
   :caption:
   :language: sql

The :func:`executescript` method of the :class:`Connection` can be
used to run the DDL instructions to create the schema.

.. literalinclude:: sqlite3_create_schema.py
   :caption:
   :start-after: #end_pymotw_header

After the tables are created, a few :command:`insert` statements
create a sample project and related tasks.  The :command:`sqlite3`
command line program can be used to examine the contents of the
database.

.. {{{cog
.. run_script(cog.inFile, 'rm -f todo.db', interpreter='')
.. cog.out(run_script(cog.inFile, 'sqlite3_create_schema.py'))
.. cog.out(run_script(cog.inFile, "sqlite3 todo.db 'select * from task'", 
..         interpreter=None, include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 sqlite3_create_schema.py
	
	Creating schema
	Inserting initial data

	$ sqlite3 todo.db 'select * from task'
	
	1|1|write about select|done|2016-04-25||pymotw
	2|1|write about random|waiting|2016-08-22||pymotw
	3|1|write about sqlite3|active|2017-07-31||pymotw

.. {{{end}}}


Retrieving Data
===============

To retrieve the values saved in the :data:`task` table from within a
Python program, create a :class:`Cursor` from a database connection.
A cursor produces a consistent view of the data, and is the primary
means of interacting with a transactional database system like SQLite.

.. literalinclude:: sqlite3_select_tasks.py
   :caption:
   :start-after: #end_pymotw_header

Querying is a two step process.  First, run the query with the
cursor's :func:`execute` method to tell the database engine what data
to collect.  Then, use :func:`fetchall` to retrieve the results.  The
return value is a sequence of tuples containing the values for the
columns included in the :command:`select` clause of the query.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_select_tasks.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_select_tasks.py
	
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [waiting ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

The results can be retrieved one at a time with :func:`fetchone`, or
in fixed-size batches with :func:`fetchmany`.

.. literalinclude:: sqlite3_select_variations.py
   :caption:
   :start-after: #end_pymotw_header

The value passed to :func:`fetchmany` is the maximum number of items
to return.  If fewer items are available, the sequence returned will
be smaller than the maximum value.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_select_variations.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_select_variations.py
	
	Project details for Python Module of the Week (pymotw)
	  due 2016-11-01
	
	Next 5 tasks:
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [waiting ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

Query Metadata
==============

The DB-API 2.0 specification says that after :func:`execute` has been
called, the :class:`Cursor` should set its :attr:`description`
attribute to hold information about the data that will be returned by
the fetch methods.  The API specification say that the description
value is a sequence of tuples containing the column name, type,
display size, internal size, precision, scale, and a flag that says
whether null values are accepted.

.. literalinclude:: sqlite3_cursor_description.py
   :caption:
   :start-after: #end_pymotw_header

Because :mod:`sqlite3` does not enforce type or size constraints on
data inserted into a database, only the column name value is filled
in.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_cursor_description.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_cursor_description.py
	
	Task table has these columns:
	('id', None, None, None, None, None, None)
	('priority', None, None, None, None, None, None)
	('details', None, None, None, None, None, None)
	('status', None, None, None, None, None, None)
	('deadline', None, None, None, None, None, None)
	('completed_on', None, None, None, None, None, None)
	('project', None, None, None, None, None, None)

.. {{{end}}}

Row Objects
===========

By default, the values returned by the fetch methods as "rows" from
the database are tuples.  The caller is responsible for knowing the
order of the columns in the query and extracting individual values
from the tuple.  When the number of values in a query grows, or the
code working with the data is spread out in a library, it is usually
easier to work with an object and access values using their
column names.  That way, the number and order of the tuple
contents can change over time as the query is edited, and code
depending on the query results is less likely to break.

:class:`Connection` objects have a :data:`row_factory` property that
allows the calling code to control the type of object created to
represent each row in the query result set.  :mod:`sqlite3` also
includes a :class:`Row` class intended to be used as a row factory.
Column values can be accessed through :class:`Row` instances by using
the column index or name.

.. literalinclude:: sqlite3_row_factory.py
   :caption:
   :start-after: #end_pymotw_header

This version of the ``sqlite3_select_variations.py`` example has been
re-written using :class:`Row` instances instead of tuples.  The row
from the project table is still printed by accessing the column values
through position, but the :command:`print` statement for tasks uses
keyword lookup instead, so it does not matter that the order of the
columns in the query has been changed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_row_factory.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_row_factory.py
	
	Project details for Python Module of the Week (pymotw)
	  due 2016-11-01
	
	Next 5 tasks:
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [waiting ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

Using Variables with Queries
============================

Using queries defined as literal strings embedded in a program is
inflexible.  For example, when another project is added to the
database the query to show the top five tasks should be updated to
work with either project.  One way to add more flexibility is to build
an SQL statement with the desired query by combining values in Python.
However, building a query string in this way is dangerous, and should
be avoided.  Failing to correctly escape special characters in the
variable parts of the query can result in SQL parsing errors, or
worse, a class of security vulnerabilities known as *SQL-injection
attacks*, which allow intruders to execute arbitrary SQL statements in
the database.

The proper way to use dynamic values with queries is through *host
variables* passed to :func:`execute` along with the SQL instruction.
A placeholder value in the SQL is replaced with the value of the host
variable when the statement is executed.  Using host variables instead
of inserting arbitrary values into the SQL before it is parsed avoids
injection attacks because there is no chance that the untrusted values
will affect how the SQL is parsed.  SQLite supports two forms for
queries with placeholders, positional and named.

Positional Parameters
---------------------

A question mark (``?``) denotes a positional argument, passed to
:func:`execute` as a member of a tuple.

.. literalinclude:: sqlite3_argument_positional.py
   :caption:
   :start-after: #end_pymotw_header

The command line argument is passed safely to the query as a
positional argument, and there is no chance for bad data to corrupt
the database.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_argument_positional.py pymotw'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_argument_positional.py pymotw
	
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [waiting ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

Named Parameters
----------------

Use named parameters for more complex queries with a lot of parameters,
or where some parameters are repeated multiple times within the query.
Named parameters are prefixed with a colon (e.g., ``:param_name``).

.. literalinclude:: sqlite3_argument_named.py
   :caption:
   :start-after: #end_pymotw_header

Neither positional nor named parameters need to be quoted or escaped,
since they are given special treatment by the query parser.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_argument_named.py pymotw'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_argument_named.py pymotw
	
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [waiting ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

Query parameters can be used with :command:`select`,
:command:`insert`, and :command:`update` statements.  They can appear
in any part of the query where a literal value is legal.

.. literalinclude:: sqlite3_argument_update.py
   :caption:
   :start-after: #end_pymotw_header

This :command:`update` statement uses two named parameters.  The
:data:`id` value is used to find the right row to modify, and the
:data:`status` value is written to the table.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_argument_update.py 2 done', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'sqlite3_argument_named.py pymotw', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 sqlite3_argument_update.py 2 done
	$ python3 sqlite3_argument_named.py pymotw
	
	 1 [1] write about select        [done    ] (2016-04-25)
	 2 [1] write about random        [done    ] (2016-08-22)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}

Bulk Loading
============

To apply the same SQL instruction to a large set of data, use
:func:`executemany`.  This is useful for loading data, since it avoids
looping over the inputs in Python and lets the underlying library
apply loop optimizations.  This example program reads a list of tasks
from a comma-separated value file using the :mod:`csv` module and
loads them into the database.

.. literalinclude:: sqlite3_load_csv.py
   :caption:
   :start-after: #end_pymotw_header

The sample data file ``tasks.csv`` contains:

.. literalinclude:: tasks.csv

Running the program produces:

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_load_csv.py tasks.csv', trailing_newlines=False))
.. cog.out(run_script(cog.inFile, 'sqlite3_argument_named.py pymotw', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 sqlite3_load_csv.py tasks.csv
	$ python3 sqlite3_argument_named.py pymotw
	
	 1 [1] write about select        [done    ] (2016-04-25)
	 5 [2] revise chapter intros     [active  ] (2016-08-20)
	 2 [1] write about random        [done    ] (2016-08-22)
	 6 [1] subtitle                  [active  ] (2016-11-01)
	 4 [2] finish reviewing markup   [active  ] (2016-11-30)
	 3 [1] write about sqlite3       [active  ] (2017-07-31)

.. {{{end}}}


Defining New Column Types
=========================

SQLite has native support for integer, floating point, and text
columns.  Data of these types is converted automatically by
:mod:`sqlite3` from Python's representation to a value that can be
stored in the database, and back again, as needed.  Integer values are
loaded from the database into :class:`int` or :class:`long` variables,
depending on the size of the value.  Text is saved and retrieved as
:class:`str`, unless the :attr:`text_factory` for the
:class:`Connection` has been changed.

Although SQLite only supports a few data types internally,
:mod:`sqlite3` includes facilities for defining custom types to allow
a Python application to store any type of data in a column.
Conversion for types beyond those supported by default is enabled in
the database connection using the :data:`detect_types` flag.  Use
:const:`PARSE_DECLTYPES` if the column was declared using the desired
type when the table was defined.

.. literalinclude:: sqlite3_date_types.py
   :caption:
   :start-after: #end_pymotw_header

:mod:`sqlite3` provides converters for date and timestamp columns,
using the classes :class:`date` and :class:`datetime` from the
:mod:`datetime` module to represent the values in Python.  Both
date-related converters are enabled automatically when type-detection
is turned on.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_date_types.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_date_types.py
	
	Without type detection:
	  id        1                          <class 'int'>
	  details   'write about select'       <class 'str'>
	  deadline  '2016-04-25'               <class 'str'>
	
	With type detection:
	  id        1                          <class 'int'>
	  details   'write about select'       <class 'str'>
	  deadline  datetime.date(2016, 4, 25) <class 'datetime.date'>

.. {{{end}}}

Two functions need to be registered to define a new type.  The
*adapter* takes the Python object as input and returns a byte string
that can be stored in the database.  The *converter* receives the
string from the database and returns a Python object.  Use
:func:`register_adapter` to define an adapter function, and
:func:`register_converter` for a converter function.

.. literalinclude:: sqlite3_custom_type.py
   :caption:
   :start-after: #end_pymotw_header

This example uses :mod:`pickle` to save an object to a string that can
be stored in the database, a useful technique for storing arbitrary
objects, but one that does not allow querying based on object
attributes.  A real *object-relational mapper*, such as SQLAlchemy_, that
stores attribute values in their own columns will be more useful for
large amounts of data.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_custom_type.py', break_lines_at=68))
.. }}}

.. code-block:: none

	$ python3 sqlite3_custom_type.py
	
	adapter_func(MyObj('this is a value to save'))
	
	adapter_func(MyObj(42))
	
	converter_func(b'\x80\x03c__main__\nMyObj\nq\x00)\x81q\x01}q\x02X\x0
	3\x00\x00\x00argq\x03X\x17\x00\x00\x00this is a value to saveq\x04sb
	.')
	
	converter_func(b'\x80\x03c__main__\nMyObj\nq\x00)\x81q\x01}q\x02X\x0
	3\x00\x00\x00argq\x03K*sb.')
	
	Retrieved 1 MyObj('this is a value to save')
	  with type <class '__main__.MyObj'>
	
	Retrieved 2 MyObj(42)
	  with type <class '__main__.MyObj'>
	

.. {{{end}}}

Determining Types for Columns
=============================

There are two sources for types information about the data for a
query.  The original table declaration can be used to identify the
type of a real column, as shown earlier.  A type specifier can also be
included in the :command:`select` clause of the query itself using the
form ``as "name [type]"``.

.. literalinclude:: sqlite3_custom_type_column.py
   :caption:
   :start-after: #end_pymotw_header

Use the :data:`detect_types` flag :const:`PARSE_COLNAMES` when the
type is part of the query instead of the original table definition.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_custom_type_column.py', break_lines_at=68))
.. }}}

.. code-block:: none

	$ python3 sqlite3_custom_type_column.py
	
	adapter_func(MyObj('this is a value to save'))
	
	adapter_func(MyObj(42))
	
	converter_func(b'\x80\x03c__main__\nMyObj\nq\x00)\x81q\x01}q\x02X\x0
	3\x00\x00\x00argq\x03X\x17\x00\x00\x00this is a value to saveq\x04sb
	.')
	
	converter_func(b'\x80\x03c__main__\nMyObj\nq\x00)\x81q\x01}q\x02X\x0
	3\x00\x00\x00argq\x03K*sb.')
	
	Retrieved 1 MyObj('this is a value to save')
	  with type <class '__main__.MyObj'>
	
	Retrieved 2 MyObj(42)
	  with type <class '__main__.MyObj'>
	

.. {{{end}}}

Transactions
============

One of the key features of relational databases is the use of
*transactions* to maintain a consistent internal state.  With
transactions enabled, several changes can be made through one
connection without effecting any other users until the results are
*committed* and flushed to the actual database.

Preserving Changes
------------------

Changes to the database, either through :command:`insert` or
:command:`update` statements, need to be saved by explicitly calling
:func:`commit`.  This requirement gives an application an opportunity
to make several related changes together, so they are stored
*atomically* instead of incrementally, and avoids a situation where
partial updates are seen by different clients connecting to the
database simultaneously.

The effect of calling :func:`commit` can be seen with a program that
uses several connections to the database.  A new row is inserted with
the first connection, and then two attempts are made to read it back
using separate connections.

.. literalinclude:: sqlite3_transaction_commit.py
   :caption:
   :start-after: #end_pymotw_header

When :func:`show_projects` is called before :data:`conn1` has been
committed, the results depend on which connection is used.  Since the
change was made through :data:`conn1`, it sees the altered data.
However, :data:`conn2` does not.  After committing, the new connection
:data:`conn3` sees the inserted row.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_transaction_commit.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_transaction_commit.py
	
	Before changes:
	   pymotw
	
	After changes in conn1:
	   pymotw
	   virtualenvwrapper
	
	Before commit:
	   pymotw
	
	After commit:
	   pymotw
	   virtualenvwrapper

.. {{{end}}}


Discarding Changes
------------------

Uncommitted changes can also be discarded entirely using
:func:`rollback`.  The :func:`commit` and :func:`rollback` methods are
usually called from different parts of the same ``try:except`` block,
with errors triggering a rollback.

.. literalinclude:: sqlite3_transaction_rollback.py
   :caption:
   :start-after: #end_pymotw_header

After calling :func:`rollback`, the changes to the database are no
longer present.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_transaction_rollback.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_transaction_rollback.py
	
	Before changes:
	   pymotw
	   virtualenvwrapper
	
	After delete:
	   pymotw
	ERROR: simulated error
	
	After rollback:
	   pymotw
	   virtualenvwrapper

.. {{{end}}}

Isolation Levels
================

:mod:`sqlite3` supports three locking modes, called *isolation
levels*, that control the technique used to prevent incompatible changes
between connections.  The isolation level is set by passing a string
as the *isolation_level* argument when a connection is opened, so
different connections can use different values.

This program demonstrates the effect of different isolation levels on
the order of events in threads using separate connections to the same
database.  Four threads are created.  Two threads write changes to the
database by updating existing rows.  The other two threads attempt to
read all of the rows from the ``task`` table.

.. literalinclude:: sqlite3_isolation_levels.py
   :caption:
   :start-after: #end_pymotw_header

The threads are synchronized using an :class:`Event` object from the
:mod:`threading` module.  The :func:`writer` function connects and
make changes to the database, but does not commit before the event
fires.  The :func:`reader` function connects, then waits to query the
database until after the synchronization event occurs.

Deferred
--------

The default isolation level is ``DEFERRED``.  Using deferred mode
locks the database, but only once a change is begun.  All of the
previous examples use deferred mode.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_isolation_levels.py DEFERRED'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_isolation_levels.py DEFERRED
	
	2016-08-20 17:26:25,132 (Reader 2  ) waiting to synchronize
	2016-08-20 17:26:25,132 (Reader 1  ) waiting to synchronize
	2016-08-20 17:26:25,135 (Writer 1  ) waiting to synchronize
	2016-08-20 17:26:26,133 (MainThread) setting ready
	2016-08-20 17:26:26,133 (Reader 2  ) wait over
	2016-08-20 17:26:26,134 (Writer 1  ) PAUSING
	2016-08-20 17:26:26,134 (Reader 1  ) wait over
	2016-08-20 17:26:26,134 (Reader 2  ) SELECT EXECUTED
	2016-08-20 17:26:26,134 (Reader 2  ) results fetched
	2016-08-20 17:26:26,134 (Reader 1  ) SELECT EXECUTED
	2016-08-20 17:26:26,134 (Reader 1  ) results fetched
	2016-08-20 17:26:27,136 (Writer 1  ) CHANGES COMMITTED
	2016-08-20 17:26:27,200 (Writer 2  ) waiting to synchronize
	2016-08-20 17:26:27,200 (Writer 2  ) PAUSING
	2016-08-20 17:26:28,202 (Writer 2  ) CHANGES COMMITTED

.. {{{end}}}


Immediate
---------

Immediate mode locks the database as soon as a change starts and
prevents other cursors from making changes until the transaction is
committed.  It is suitable for a database with complicated writes, but
more readers than writers, since the readers are not blocked while the
transaction is ongoing.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_isolation_levels.py IMMEDIATE'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_isolation_levels.py IMMEDIATE
	
	2016-08-20 17:26:28,292 (Reader 1  ) waiting to synchronize
	2016-08-20 17:26:28,293 (Reader 2  ) waiting to synchronize
	2016-08-20 17:26:28,295 (Writer 2  ) waiting to synchronize
	2016-08-20 17:26:29,294 (MainThread) setting ready
	2016-08-20 17:26:29,294 (Reader 1  ) wait over
	2016-08-20 17:26:29,294 (Reader 2  ) wait over
	2016-08-20 17:26:29,294 (Writer 2  ) PAUSING
	2016-08-20 17:26:29,295 (Reader 1  ) SELECT EXECUTED
	2016-08-20 17:26:29,295 (Reader 2  ) SELECT EXECUTED
	2016-08-20 17:26:29,295 (Reader 1  ) results fetched
	2016-08-20 17:26:29,295 (Reader 2  ) results fetched
	2016-08-20 17:26:30,297 (Writer 2  ) CHANGES COMMITTED
	2016-08-20 17:26:30,348 (Writer 1  ) waiting to synchronize
	2016-08-20 17:26:30,349 (Writer 1  ) PAUSING
	2016-08-20 17:26:31,351 (Writer 1  ) CHANGES COMMITTED

.. {{{end}}}

Exclusive
---------

Exclusive mode locks the database to all readers and writers.  Its use
should be limited in situations where database performance is
important, since each exclusive connection blocks all other users.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_isolation_levels.py EXCLUSIVE'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_isolation_levels.py EXCLUSIVE
	
	2016-08-20 17:26:31,427 (Reader 1  ) waiting to synchronize
	2016-08-20 17:26:31,427 (Reader 2  ) waiting to synchronize
	2016-08-20 17:26:31,430 (Writer 1  ) waiting to synchronize
	2016-08-20 17:26:32,428 (MainThread) setting ready
	2016-08-20 17:26:32,428 (Reader 1  ) wait over
	2016-08-20 17:26:32,428 (Writer 1  ) PAUSING
	2016-08-20 17:26:32,428 (Reader 2  ) wait over
	2016-08-20 17:26:33,429 (Writer 1  ) CHANGES COMMITTED
	2016-08-20 17:26:33,480 (Reader 2  ) SELECT EXECUTED
	2016-08-20 17:26:33,480 (Reader 2  ) results fetched
	2016-08-20 17:26:33,488 (Writer 2  ) waiting to synchronize
	2016-08-20 17:26:33,488 (Writer 2  ) PAUSING
	2016-08-20 17:26:34,490 (Writer 2  ) CHANGES COMMITTED
	2016-08-20 17:26:34,509 (Reader 1  ) SELECT EXECUTED
	2016-08-20 17:26:34,509 (Reader 1  ) results fetched

.. {{{end}}}

Because the first writer has started making changes, the readers and
second writer block until it commits.  The :func:`sleep` call
introduces an artificial delay in the writer thread to highlight the
fact that the other connections are blocking.



Autocommit
----------

The *isolation_level* parameter for the connection can also be set to
``None`` to enable autocommit mode.  With autocommit enabled, each
:func:`execute` call is committed immediately when the statement
finishes.  Autocommit mode is suited for short transactions, such as
those that insert a small amount of data into a single table.  The
database is locked for as little time as possible, so there is less
chance of contention between threads.

In ``sqlite3_autocommit.py``, the explicit call to :func:`commit` has
been removed and the isolation level is set to ``None``, but otherwise
is the same as ``sqlite3_isolation_levels.py``.  The output is
different, however, since both writer threads finish their work before
either reader starts querying.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_autocommit.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_autocommit.py
	
	2016-08-20 17:26:34,573 (Reader 1  ) waiting to synchronize
	2016-08-20 17:26:34,573 (Reader 2  ) waiting to synchronize
	2016-08-20 17:26:34,578 (Writer 1  ) waiting to synchronize
	2016-08-20 17:26:34,579 (Writer 2  ) waiting to synchronize
	2016-08-20 17:26:35,573 (MainThread) setting ready
	2016-08-20 17:26:35,573 (Reader 1  ) wait over
	2016-08-20 17:26:35,573 (Reader 2  ) wait over
	2016-08-20 17:26:35,573 (Writer 2  ) PAUSING
	2016-08-20 17:26:35,573 (Writer 1  ) PAUSING
	2016-08-20 17:26:35,574 (Reader 1  ) SELECT EXECUTED
	2016-08-20 17:26:35,574 (Reader 1  ) results fetched
	2016-08-20 17:26:35,575 (Reader 2  ) SELECT EXECUTED
	2016-08-20 17:26:35,575 (Reader 2  ) results fetched

.. {{{end}}}


In-Memory Databases
===================

SQLite supports managing an entire database in RAM, instead of relying
on a disk file.  In-memory databases are useful for automated testing,
where the database does not need to be preserved between test runs, or
when experimenting with a schema or other database features.  To open
an in-memory database, use the string ``':memory:'`` instead of a
filename when creating the :class:`Connection`.  Each ``':memory:'``
connection creates a separate database instance, so changes made by a
cursor in one do not effect other connections.

Exporting the Contents of a Database
====================================

The contents of an in-memory database can be saved using the
:func:`iterdump` method of the :class:`Connection`.  The iterator
returned by :func:`iterdump` produces a series of strings that
together build SQL instructions to recreate the state of the database.

.. literalinclude:: sqlite3_iterdump.py
   :caption:
   :start-after: #end_pymotw_header

:func:`iterdump` can also be used with databases saved to files, but
it is most useful for preserving a database that would not otherwise
be saved.  This output has been edited to fit on the page while
remaining syntactically correct.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_iterdump.py', 
..                    break_lines_at=74, line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_iterdump.py
	
	Creating schema
	Inserting initial data
	Dumping:
	BEGIN TRANSACTION;
	CREATE TABLE project (
	    name        text primary key,
	    description text,
	    deadline    date
	);
	INSERT INTO "project" VALUES('pymotw','Python Module of the
	Week','2010-11-01');
	DELETE FROM "sqlite_sequence";
	INSERT INTO "sqlite_sequence" VALUES('task',3);
	CREATE TABLE task (
	    id           integer primary key autoincrement not null,
	    priority     integer default 1,
	    details      text,
	    status       text,
	    deadline     date,
	    completed_on date,
	    project      text not null references project(name)
	);
	INSERT INTO "task" VALUES(1,1,'write about
	select','done','2010-10-03',NULL,'pymotw');
	INSERT INTO "task" VALUES(2,1,'write about
	random','waiting','2010-10-10',NULL,'pymotw');
	INSERT INTO "task" VALUES(3,1,'write about
	sqlite3','active','2010-10-17',NULL,'pymotw');
	COMMIT;

.. {{{end}}}

Using Python Functions in SQL
=============================

SQL syntax supports calling functions during queries, either in
the column list or :command:`where` clause of the :command:`select`
statement.  This feature makes it possible to process data before
returning it from the query, and can be used to convert between
different formats, perform calculations that would be clumsy in pure
SQL, and reuse application code.

.. literalinclude:: sqlite3_create_function.py
   :caption:
   :start-after: #end_pymotw_header

Functions are exposed using the :func:`create_function` method of the
:class:`Connection`.  The parameters are the name of the function (as
it should be used from within SQL), the number of arguments the
function takes, and the Python function to expose.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_create_function.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_create_function.py
	
	Original values:
	(1, 'write about select')
	(2, 'write about random')
	(3, 'write about sqlite3')
	(4, 'finish reviewing markup')
	(5, 'revise chapter intros')
	(6, 'subtitle')
	
	Encrypting...
	Encrypting 'write about select'
	Encrypting 'write about random'
	Encrypting 'write about sqlite3'
	Encrypting 'finish reviewing markup'
	Encrypting 'revise chapter intros'
	Encrypting 'subtitle'
	
	Raw encrypted values:
	(1, 'jevgr nobhg fryrpg')
	(2, 'jevgr nobhg enaqbz')
	(3, 'jevgr nobhg fdyvgr3')
	(4, 'svavfu erivrjvat znexhc')
	(5, 'erivfr puncgre vagebf')
	(6, 'fhogvgyr')
	
	Decrypting in query...
	Decrypting 'jevgr nobhg fryrpg'
	Decrypting 'jevgr nobhg enaqbz'
	Decrypting 'jevgr nobhg fdyvgr3'
	Decrypting 'svavfu erivrjvat znexhc'
	Decrypting 'erivfr puncgre vagebf'
	Decrypting 'fhogvgyr'
	(1, 'write about select')
	(2, 'write about random')
	(3, 'write about sqlite3')
	(4, 'finish reviewing markup')
	(5, 'revise chapter intros')
	(6, 'subtitle')

.. {{{end}}}

Custom Aggregation
==================

An aggregation function collects many pieces of individual data and
summarizes it in some way.  Examples of built-in aggregation functions
are :func:`avg` (average), :func:`min`, :func:`max`, and
:func:`count`.

The API for aggregators used by :mod:`sqlite3` is defined in terms of
a class with two methods.  The :func:`step` method is called once for
each data value as the query is processed.  The :func:`finalize`
method is called one time at the end of the query and should return
the aggregate value.  This example implements an aggregator for the
arithmetic *mode*.  It returns the value that appears most frequently
in the input.

.. literalinclude:: sqlite3_create_aggregate.py
   :caption:
   :start-after: #end_pymotw_header

The aggregator class is registered with the :func:`create_aggregate`
method of the :class:`Connection`.  The parameters are the name of the
function (as it should be used from within SQL), the number of
arguments the :func:`step` method takes, and the class to use.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_create_aggregate.py'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_create_aggregate.py
	
	step('2016-04-25')
	step('2016-08-22')
	step('2017-07-31')
	step('2016-11-30')
	step('2016-08-20')
	step('2016-11-01')
	finalize() -> '2016-11-01' (1 times)
	mode(deadline) is: 2016-11-01

.. {{{end}}}

Threading and Connection Sharing
================================

For historical reasons having to do with old versions of SQLite,
:class:`Connection` objects cannot be shared between threads.  Each
thread must create its own connection to the database.

.. literalinclude:: sqlite3_threading.py
   :caption:
   :start-after: #end_pymotw_header

Attempts to share a connection between threads result in an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_threading.py', break_lines_at=66, 
..         line_break_mode='wrap'))
.. }}}

.. code-block:: none

	$ python3 sqlite3_threading.py
	
	Starting thread
	ERROR: SQLite objects created in a thread can only be used in that
	same thread.The object was created in thread id 140735234088960
	and this is thread id 123145307557888

.. {{{end}}}

Restricting Access to Data
==========================

Although SQLite does not have user access controls found in other,
larger, relational databases, it does have a mechanism for limiting
access to columns.  Each connection can install an *authorizer
function* to grant or deny access to columns at runtime based on any
desired criteria.  The authorizer function is invoked during the
parsing of SQL statements, and is passed five arguments.  The first is
an action code indicating the type of operation being performed
(reading, writing, deleting, etc.).  The rest of the arguments depend
on the action code.  For :const:`SQLITE_READ` operations, the
arguments are the name of the table, the name of the column, the
location in the SQL where the access is occurring (main query, trigger,
etc.), and ``None``.  

.. literalinclude:: sqlite3_set_authorizer.py
   :caption:
   :start-after: #end_pymotw_header

This example uses :const:`SQLITE_IGNORE` to cause the strings from the
``task.details`` column to be replaced with null values in the query
results.  It also prevents all access to the ``task.priority`` column
by returning :const:`SQLITE_DENY`, which in turn causes SQLite to
raise an exception.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'sqlite3_set_authorizer.py', ignore_error=True))
.. }}}

.. code-block:: none

	$ python3 sqlite3_set_authorizer.py
	
	Using SQLITE_IGNORE to mask a column value:
	
	authorizer_func(21, None, None, None, None)
	requesting permission to run a select statement
	
	authorizer_func(20, task, id, main, None)
	requesting access to column task.id from main
	
	authorizer_func(20, task, details, main, None)
	requesting access to column task.details from main
	  ignoring details column
	
	authorizer_func(20, task, project, main, None)
	requesting access to column task.project from main
	1 None
	2 None
	3 None
	4 None
	5 None
	6 None
	
	Using SQLITE_DENY to deny access to a column:
	
	authorizer_func(21, None, None, None, None)
	requesting permission to run a select statement
	
	authorizer_func(20, task, id, main, None)
	requesting access to column task.id from main
	
	authorizer_func(20, task, priority, main, None)
	requesting access to column task.priority from main
	  preventing access to priority column
	Traceback (most recent call last):
	  File "sqlite3_set_authorizer.py", line 53, in <module>
	    """)
	sqlite3.DatabaseError: access to task.priority is prohibited

.. {{{end}}}

The possible action codes are available as constants in
:mod:`sqlite3`, with names prefixed ``SQLITE_``.  Each type of SQL
statement can be flagged, and access to individual columns can be
controlled as well.


.. Extension Modules
.. =================

.. .. Only works if the proper version of the sqlite library is available
.. .. during compilation

.. * full-text search
.. * loading from api
.. * loading from sql

.. seealso::

   * :pydoc:`sqlite3`

   * :pep:`249` -- DB API 2.0 Specification (A standard interface for
     modules that provide access to relational databases.)

   * `SQLite`_ -- The official site of the SQLite library.

   * :mod:`shelve` -- Key-value store for saving arbitrary Python objects.

   * SQLAlchemy_ -- A popular object-relational mapper that supports
     SQLite among many other relational databases.

.. _SQLite: http://www.sqlite.org/
.. _SQLAlchemy: http://sqlalchemy.org/
