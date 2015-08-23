=============
 defaultdict
=============

The standard dictionary includes the method :func:`setdefault` for
retrieving a value and establishing a default if the value does not
exist. By contrast, :class:`defaultdict` lets the caller specify the
default up front when the container is initialized.

.. include:: collections_defaultdict.py
    :literal:
    :start-after: #end_pymotw_header

This works well as long as it is appropriate for all keys to have the
same default. It can be especially useful if the default is a type
used for aggregating or accumulating values, such as a :class:`list`,
:class:`set`, or even :class:`int`. The standard library documentation
includes several examples of using :class:`defaultdict` this way.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'collections_defaultdict.py'))
.. }}}

::

	$ python collections_defaultdict.py
	
	d: defaultdict(<function default_factory at 0x100d9ba28>, {'foo': 'bar'})
	foo => bar
	bar => default value

.. {{{end}}}

.. seealso::

    `defaultdict examples <http://docs.python.org/lib/defaultdict-examples.html>`_
        Examples of using defaultdict from the standard library documentation.

    `Evolution of Default Dictionaries in Python <http://jtauber.com/blog/2008/02/27/evolution_of_default_dictionaries_in_python/>`_
        Discussion from James Tauber of how :class:`defaultdict`
        relates to other means of initializing dictionaries.
