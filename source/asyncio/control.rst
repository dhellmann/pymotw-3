==============================================
 Composing Coroutines with Control Structures
==============================================

Linear control flow between a series of coroutines is easy to manage
with the built-in language keyword ``await``. More complicated
structures allowing one coroutine to wait for several others to
complete in parallel are also possible using tools in :mod:`asyncio`.

Waiting for Multiple Coroutines
===============================

It is often useful to divide one operation into many parts and execute
them separately. For example, downloading several remote resources or
querying remote APIs. In situations where the order of execution
doesn't matter, and there may be an arbitrary number of operations,
:func:`wait` can be used to pause one coroutine until the other
background operations complete.

.. include:: asyncio_wait.py
   :literal:
   :start-after: #end_pymotw_header

The return value from :func:`wait` is a tuple containing two sets of
:class:`Task` instances. The first set holds the finished tasks, and
the second holds any that are still running.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_wait.py'))
.. }}}

::

	$ python3 asyncio_wait.py
	
	starting main
	waiting for phases to complete
	in phase 0
	in phase 1
	in phase 2
	done with phase 0
	done with phase 1
	done with phase 2
	result: ['phase 1 result', 'phase 0 result', 'phase 2 result']

.. {{{end}}}

There will only be pending operations left if :func:`wait` is used
with a timeout value.

.. include:: asyncio_wait_timeout.py
   :literal:
   :start-after: #end_pymotw_header

Those remaining background operations should either be cancelled or
finished by waiting for them. Leaving them pending while the event
loop continues will let them execute further, which may not be
desirable if the overall operation is considered aborted. Leaving them
pending at the end of the process will result in warnings being
reported.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_wait_timeout.py'))
.. }}}

::

	$ python3 asyncio_wait_timeout.py
	
	starting main
	waiting 0.1 for phases to complete
	in phase 2
	in phase 1
	in phase 0
	done with phase 0
	1 completed and 2 pending
	cancelling tasks
	exiting main
	phase 1 cancelled
	phase 2 cancelled

.. {{{end}}}

