.. _article-data-persistence:

#############################
Data Persistence and Exchange
#############################

Python provides several modules for storing data.  There are basically two aspects to persistence: converting the in-memory object back and forth into a format for saving it, and working with the storage of the converted data.

===================
Serializing Objects
===================

Python includes two modules capable of converting objects into a transmittable or storable format (*serializing*): :mod:`pickle` and :mod:`json`.  It is most common to use :mod:`pickle`, since there is a fast C implementation and it is integrated with some of the other standard library modules that actually store the serialized data, such as :mod:`shelve`.  Web-based applications may want to examine :mod:`json`, however, since it integrates better with some of the existing web service storage applications.

==========================
Storing Serialized Objects
==========================

Once the in-memory object is converted to a storable format, the next step is to decide how to store the data.  A simple flat-file with serialized objects written one after the other works for data that does not need to be indexed in any way.  But Python includes a collection of modules for storing key-value pairs in a simple database using one of the DBM format variants.

The simplest interface to take advantage of the DBM format is provided by :mod:`shelve`.  Simply open the shelve file, and access it through a dictionary-like API.  Objects saved to the shelve are automatically pickled and saved without any extra work on your part.  

One drawback of shelve is that with the default interface you can't guarantee which DBM format will be used.  That won't matter if your application doesn't need to share the database files between hosts with different libraries, but if that is needed you can use one of the classes in the module to ensure a specific format is selected (:ref:`shelve-shelf-types`).

If you're going to be passing a lot of data around via JSON anyway, using :mod:`json` and :mod:`anydbm` can provide another persistence mechanism.  Since the DBM database keys and values must be strings, however, the objects won't be automatically re-created when you access the value in the database.

====================
Relational Databases
====================

The excellent :mod:`sqlite3` in-process relational database is available with most Python distributions.  It stores its database in memory or in a local file, and all access is from within the same process, so there is no network lag.  The compact nature of :mod:`sqlite3` makes it especially well suited for embedding in desktop applications or development versions of web apps.

All access to the database is through the Python DBI 2.0 API, by default, as no object relational mapper (ORM) is included.  The most popular general purpose ORM is `SQLAlchemy <http://www.sqlalchemy.org/>`_, but others such as Django's native ORM layer also support SQLite.  SQLAlchemy is easy to install and set up, but if your objects aren't very complicated and you are worried about overhead, you may want to use the DBI interface directly.

======================================
Data Exchange Through Standard Formats
======================================

Although not usually considered a true persistence format :mod:`csv`, or comma-separated-value, files can be an effective way to migrate data between applications.  Most spreadsheet programs and databases support both export and import using CSV, so dumping data to a CSV file is frequently the simplest way to move data out of your application and into an analysis tool.
