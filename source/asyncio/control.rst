==============================================
 Composing Coroutines with Control Structures
==============================================

Linear control flow between a series of coroutines is easy to manage
with the built-in language keyword ``await``. More complicated
structures allowing one coroutine to wait for several others to
complete in parallel are also possible using tools in ``asyncio``.

Waiting for Multiple Coroutines
===============================

It is often useful to divide one operation into many parts and execute
them separately. For example, downloading several remote resources or
querying remote APIs. In situations where the order of execution
doesn't matter, and where there may be an arbitrary number of
operations, ``wait()`` can be used to pause one coroutine until the
other background operations complete.

.. literalinclude:: asyncio_wait.py
   :caption:
   :start-after: #end_pymotw_header

Internally, ``wait()`` uses a ``set`` to hold the ``Task``
instances it creates. This results in them starting, and finishing, in
an unpredictable order.  The return value from ``wait()`` is a tuple
containing two sets holding the finished and pending tasks.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_wait.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_wait.py
	
	starting main
	waiting for phases to complete
	in phase 2
	in phase 0
	in phase 1
	done with phase 0
	done with phase 1
	done with phase 2
	results: ['phase 0 result', 'phase 1 result', 'phase 2 result']

.. {{{end}}}

There will only be pending operations left if ``wait()`` is used
with a timeout value.

.. literalinclude:: asyncio_wait_timeout.py
   :caption:
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

.. code-block:: none

	$ python3 asyncio_wait_timeout.py
	
	starting main
	waiting 0.1 for phases to complete
	in phase 1
	in phase 0
	in phase 2
	done with phase 0
	1 completed and 2 pending
	canceling tasks
	exiting main
	phase 1 canceled
	phase 2 canceled

.. {{{end}}}

Gathering Results from Coroutines
=================================

If the background phases are well-defined, and only the results of
those phases matter, then ``gather()`` may be more useful for
waiting for multiple operations.

.. literalinclude:: asyncio_gather.py
   :caption:
   :start-after: #end_pymotw_header

The tasks created by gather are not exposed, so they cannot be
cancelled. The return value is a list of results in the same order as
the arguments passed to ``gather()``, regardless of the order the
background operations actually completed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_gather.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_gather.py
	
	starting main
	waiting for phases to complete
	in phase1
	in phase2
	done with phase2
	done with phase1
	results: ['phase1 result', 'phase2 result']

.. {{{end}}}

Handling Background Operations as They Finish
=============================================

``as_completed()`` is a generator that manages the execution of a
list of coroutines given to it and produces their results one at a
time as they finish running. As with ``wait()``, order is not
guaranteed by ``as_completed()``, but it is not necessary to wait
for all of the background operations to complete before taking other
action.

.. literalinclude:: asyncio_as_completed.py
   :caption:
   :start-after: #end_pymotw_header

This example starts several background phases that finish in the
reverse order from which they start. As the generator is consumed, the
loop waits for the result of the coroutine using ``await``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_as_completed.py'))
.. }}}

.. code-block:: none

	$ python3 asyncio_as_completed.py
	
	starting main
	waiting for phases to complete
	in phase 1
	in phase 0
	in phase 2
	done with phase 2
	received answer 'phase 2 result'
	done with phase 1
	received answer 'phase 1 result'
	done with phase 0
	received answer 'phase 0 result'
	results: ['phase 2 result', 'phase 1 result', 'phase 0 result']

.. {{{end}}}

