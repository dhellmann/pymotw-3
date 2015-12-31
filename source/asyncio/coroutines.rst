==========================================
 Cooperative Multitasking with Coroutines
==========================================

Coroutines are a language construct designed for concurrent
operation. A coroutine function creates a coroutine object when
called, and the coroutine object enters and exits execution,
maintaining its state even when it is not actively running.

Starting a Coroutine
====================

There are a few different ways to have the :mod:`asyncio` event loop
start a coroutine. The simplest is to use :func:`run_until_complete`,
passing the coroutine to it directly.

.. include:: asyncio_coroutine.py
   :literal:
   :start-after: #end_pymotw_header

The first step is to obtain a reference to the event loop. The default
loop type can be used, or a specific loop class can be
instantiated. In this example, the default loop is used. The
:func:`run_until_complete` method starts the loop with the coroutine
object and stops the loop when the coroutine exits by returning.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_coroutine.py'))
.. }}}

::

	$ python3 asyncio_coroutine.py
	
	entering event loop
	in coroutine
	closing event loop

.. {{{end}}}

Returning Values from Coroutines
================================

The return value of a coroutine is passed back to the code that starts
and waits for it.

.. include:: asyncio_coroutine_return.py
   :literal:
   :start-after: #end_pymotw_header

In this case, :func:`run_until_complete` also returns the result of
the coroutine it is waiting for.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_coroutine_return.py'))
.. }}}

::

	$ python3 asyncio_coroutine_return.py
	
	in coroutine
	it returned: 'result'

.. {{{end}}}


Chaining Coroutines
===================

One coroutine can start another coroutine and wait for the
results. This makes it easier to decompose a task into reusable parts.
The following example has two phases that must be executed in order,
but that can run concurrently with other operations.

.. include:: asyncio_coroutine_chain.py
   :literal:
   :start-after: #end_pymotw_header

The ``await`` keyword is used instead of adding the new coroutines to
the loop, because control flow is already inside of a coroutine being
managed by the loop so it isn't necessary to tell the loop to manage
the new coroutines.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'asyncio_coroutine_chain.py', line_break_mode='wrap'))
.. }}}

::

	$ python3 asyncio_coroutine_chain.py
	
	in outer
	waiting for result1
	in phase1
	waiting for result2
	in phase2
	return value: ('result1', 'result2 derived from result1')

.. {{{end}}}
