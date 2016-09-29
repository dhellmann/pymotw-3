===========================================
 random --- Pseudorandom Number Generators
===========================================

.. module:: random
    :synopsis: Pseudorandom number generators

:Purpose: Implements several types of pseudorandom number generators.

The :mod:`random` module provides a fast pseudorandom number generator
based on the *Mersenne Twister* algorithm.  Originally developed to
produce inputs for Monte Carlo simulations, Mersenne Twister generates
numbers with nearly uniform distribution and a large period, making it
suited for a wide range of applications.

Generating Random Numbers
=========================

The :func:`random` function returns the next random floating point
value from the generated sequence.  All of the return values fall
within the range ``0 <= n < 1.0``.

.. literalinclude:: random_random.py
   :caption:
   :start-after: #end_pymotw_header

Running the program repeatedly produces different sequences of
numbers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_random.py'))
.. cog.out(run_script(cog.inFile, 'random_random.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 random_random.py
	
	0.859 0.297 0.554 0.985 0.452 

	$ python3 random_random.py
	
	0.797 0.658 0.170 0.297 0.593 

.. {{{end}}}

To generate numbers in a specific numerical range, use :func:`uniform`
instead.

.. literalinclude:: random_uniform.py
   :caption:
   :start-after: #end_pymotw_header

Pass minimum and maximum values, and :func:`uniform` adjusts the
return values from :func:`random` using the formula ``min + (max -
min) * random()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_uniform.py'))
.. }}}

.. code-block:: none

	$ python3 random_uniform.py
	
	12.428 93.766 95.359 39.649 88.983 

.. {{{end}}}


Seeding
=======

:func:`random` produces different values each time it is called and
has a very large period before it repeats any numbers.  This is useful
for producing unique values or variations, but there are times when
having the same data set available to be processed in different ways is
useful.  One technique is to use a program to generate random values
and save them to be processed by a separate step.  That may not be
practical for large amounts of data, though, so :mod:`random` includes
the :func:`seed` function for initializing the pseudorandom generator
so that it produces an expected set of values.

.. literalinclude:: random_seed.py
   :caption:
   :start-after: #end_pymotw_header

The seed value controls the first value produced by the formula used
to produce pseudorandom numbers, and since the formula is
deterministic it also sets the full sequence produced after the seed
is changed.  The argument to :func:`seed` can be any hashable object.
The default is to use a platform-specific source of randomness, if one
is available.  Otherwise, the current time is used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_seed.py'))
.. cog.out(run_script(cog.inFile, 'random_seed.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 random_seed.py
	
	0.134 0.847 0.764 0.255 0.495 

	$ python3 random_seed.py
	
	0.134 0.847 0.764 0.255 0.495 

.. {{{end}}}


Saving State
============

The internal state of the pseudorandom algorithm used by
:func:`random` can be saved and used to control the numbers produced
in subsequent runs.  Restoring the previous state before continuing
reduces the likelihood of repeating values or sequences of values from
the earlier input.  The :func:`getstate` function returns data that
can be used to re-initialize the random number generator later with
:func:`setstate`.

.. literalinclude:: random_state.py
   :caption:
   :start-after: #end_pymotw_header

The data returned by :func:`getstate` is an implementation detail, so
this example saves the data to a file with :mod:`pickle` but otherwise
treats it as a black box.  If the file exists when the program starts,
it loads the old state and continues.  Each run produces a few numbers
before and after saving the state, to show that restoring the state
causes the generator to produce the same values again.

.. {{{cog
.. import os; os.system('rm -f source/random/state.dat')
.. cog.out(run_script(cog.inFile, 'random_state.py'))
.. cog.out(run_script(cog.inFile, 'random_state.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 random_state.py
	
	No state.dat, seeding
	0.134 0.847 0.764 
	
	After saving state:
	0.255 0.495 0.449 

	$ python3 random_state.py
	
	Found state.dat, initializing random module
	0.255 0.495 0.449 
	
	After saving state:
	0.652 0.789 0.094 

.. {{{end}}}


Random Integers
===============

:func:`random` generates floating point numbers.  It is possible to
convert the results to integers, but using :func:`randint` to generate
integers directly is more convenient.

.. literalinclude:: random_randint.py
   :caption:
   :start-after: #end_pymotw_header

The arguments to :func:`randint` are the ends of the inclusive range
for the values.  The numbers can be positive or negative, but the
first value should be less than the second.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_randint.py'))
.. }}}

.. code-block:: none

	$ python3 random_randint.py
	
	[1, 100]: 98 75 34 
	[-5, 5]: 4 0 5 

.. {{{end}}}

:func:`randrange` is a more general form of selecting values from a
range.  

.. literalinclude:: random_randrange.py
   :caption:
   :start-after: #end_pymotw_header

:func:`randrange` supports a *step* argument, in addition to start and
stop values, so it is fully equivalent to selecting a random value
from ``range(start, stop, step)``.  It is more efficient, because the
range is not actually constructed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_randrange.py'))
.. }}}

.. code-block:: none

	$ python3 random_randrange.py
	
	15 20 85 

.. {{{end}}}


Picking Random Items
====================

One common use for random number generators is to select a random item
from a sequence of enumerated values, even if those values are not
numbers.  :mod:`random` includes the :func:`choice` function for
making a random selection from a sequence.  This example simulates
flipping a coin 10,000 times to count how many times it comes up heads
and how many times tails.

.. literalinclude:: random_choice.py
   :caption:
   :start-after: #end_pymotw_header

There are only two outcomes allowed, so rather than use numbers and
convert them the words "heads" and "tails" are used with
:func:`choice`.  The results are tabulated in a dictionary using the
outcome names as keys.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_choice.py'))
.. }}}

.. code-block:: none

	$ python3 random_choice.py
	
	Heads: 5091
	Tails: 4909

.. {{{end}}}


Permutations
============

A simulation of a card game needs to mix up the deck of cards and then
deal them to the players, without using the same card more than
once.  Using :func:`choice` could result in the same card being dealt
twice, so instead, the deck can be mixed up with :func:`shuffle` and
then individual cards removed as they are dealt.

.. literalinclude:: random_shuffle.py
   :caption:
   :start-after: #end_pymotw_header

The cards are represented as strings with the face value and a unicode symbol
indicating the suit.  The dealt "hands" are created by adding one card
at a time to each of four lists, and removing it from the deck so it
cannot be dealt again.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_shuffle.py'))
.. }}}

.. code-block:: none

	$ python3 random_shuffle.py
	
	Initial deck:
	 2♥  2♦  2♣  2♠  3♥  3♦  3♣  3♠  4♥  4♦  4♣  4♠  5♥ 
	 5♦  5♣  5♠  6♥  6♦  6♣  6♠  7♥  7♦  7♣  7♠  8♥  8♦ 
	 8♣  8♠  9♥  9♦  9♣  9♠ 10♥ 10♦ 10♣ 10♠  J♥  J♦  J♣ 
	 J♠  Q♥  Q♦  Q♣  Q♠  K♥  K♦  K♣  K♠  A♥  A♦  A♣  A♠ 
	
	Shuffled deck:
	 K♦  5♦  6♦  9♦ 10♦  4♦  4♣  K♠  A♦  Q♠ 10♥  K♥ 10♣ 
	 A♥  7♥  8♦  9♥  7♦  A♠  6♥  K♣  3♥  2♣  4♠  5♣  J♥ 
	 J♦  3♠  4♥  7♣  5♥  Q♦  J♠  6♠  2♠  3♣  8♣  7♠  8♥ 
	 5♠  3♦ 10♠  A♣  Q♣  2♦  Q♥  J♣  8♠  9♠  6♣  9♣  2♥ 
	
	Hands:
	1:  2♥  8♠  Q♣  5♠  3♣ 
	2:  9♣  J♣  A♣  8♥  2♠ 
	3:  6♣  Q♥ 10♠  7♠  6♠ 
	4:  9♠  2♦  3♦  8♣  J♠ 
	
	Remaining deck:
	 K♦  5♦  6♦  9♦ 10♦  4♦  4♣  K♠  A♦  Q♠ 10♥  K♥ 10♣ 
	 A♥  7♥  8♦  9♥  7♦  A♠  6♥  K♣  3♥  2♣  4♠  5♣  J♥ 
	 J♦  3♠  4♥  7♣  5♥  Q♦ 

.. {{{end}}}

Sampling
========

Many simulations need random samples from a population of input
values.  The :func:`sample` function generates samples without
repeating values and without modifying the input sequence.  This
example prints a random sample of words from the system dictionary.

.. literalinclude:: random_sample.py
   :caption:
   :start-after: #end_pymotw_header

The algorithm for producing the result set takes into account the
sizes of the input and the sample requested to produce the result as
efficiently as possible.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_sample.py'))
.. cog.out(run_script(cog.inFile, 'random_sample.py', include_prefix=False))
.. }}}

.. code-block:: none

	$ python3 random_sample.py
	
	streamlet
	impestation
	violaquercitrin
	mycetoid
	plethoretical

	$ python3 random_sample.py
	
	nonseditious
	empyemic
	ultrasonic
	Kyurinish
	amphide

.. {{{end}}}


Multiple Simultaneous Generators
================================

In addition to module-level functions, :mod:`random` includes a
:class:`Random` class to manage the internal state for several random
number generators.  All of the functions described earlier are available
as methods of the :class:`Random` instances, and each instance can be
initialized and used separately, without interfering with the values
returned by other instances.

.. literalinclude:: random_random_class.py
   :caption:
   :start-after: #end_pymotw_header

On a system with good native random value seeding, the instances start
out in unique states.  However, if there is no good platform random
value generator, the instances are likely to have been seeded with the
current time, and therefore produce the same values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_random_class.py'))
.. }}}

.. code-block:: none

	$ python3 random_random_class.py
	
	Default initializiation:
	
	0.862  0.390
	0.833  0.624
	0.252  0.080
	
	Same seed:
	
	0.466  0.466
	0.682  0.682
	0.407  0.407

.. {{{end}}}

SystemRandom
============

Some operating systems provide a random number generator that has
access to more sources of entropy that can be introduced into the
generator.  :mod:`random` exposes this feature through the
:class:`SystemRandom` class, which has the same API as :class:`Random`
but uses :func:`os.urandom` to generate the values that form the basis
of all of the other algorithms.

.. literalinclude:: random_system_random.py
   :caption:
   :start-after: #end_pymotw_header

Sequences produced by :class:`SystemRandom` are not reproducible
because the randomness is coming from the system, rather than software
state (in fact, :func:`seed` and :func:`setstate` have no effect at
all).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_system_random.py'))
.. }}}

.. code-block:: none

	$ python3 random_system_random.py
	
	Default initializiation:
	
	0.110  0.481
	0.624  0.350
	0.378  0.056
	
	Same seed:
	
	0.634  0.731
	0.893  0.843
	0.065  0.177

.. {{{end}}}


Non-uniform Distributions
=========================

While the uniform distribution of the values produced by
:func:`random` is useful for a lot of purposes, other distributions
more accurately model specific situations.  The :mod:`random` module
includes functions to produce values in those distributions, too.
They are listed here, but not covered in detail because their uses
tend to be specialized and require more complex examples.

Normal
------

The *normal* distribution is commonly used for non-uniform continuous
values such as grades, heights, weights, etc.  The curve produced by
the distribution has a distinctive shape which has lead to it being
nicknamed a "bell curve."  :mod:`random` includes two functions for
generating values with a normal distribution, :func:`normalvariate`
and the slightly faster :func:`gauss` (the normal distribution is also
called the Gaussian distribution).

The related function, :func:`lognormvariate` produces pseudorandom
values where the logarithm of the values is distributed normally.
Log-normal distributions are useful for values that are the product of
several random variables which do not interact.

Approximation
-------------

The *triangular* distribution is used as an approximate distribution
for small sample sizes.  The "curve" of a triangular distribution has
low points at known minimum and maximum values, and a high point at
and the mode, which is estimated based on a "most likely" outcome
(reflected by the mode argument to :func:`triangular`).

Exponential
-----------

:func:`expovariate` produces an exponential distribution useful for
simulating arrival or interval time values for in homogeneous Poisson
processes such as the rate of radioactive decay or requests coming
into a web server.

The Pareto, or power law, distribution matches many observable
phenomena and was popularized by *The Long Tail*, by Chris Anderson.
The :func:`paretovariate` function is useful for simulating allocation
of resources to individuals (wealth to people, demand for musicians,
attention to blogs, etc.).

Angular
-------

The von Mises, or circular normal, distribution (produced by
:func:`vonmisesvariate`) is used for computing probabilities of cyclic
values such as angles, calendar days, and times.

Sizes
-----

:func:`betavariate` generates values with the Beta distribution, which
is commonly used in Bayesian statistics and applications such as task
duration modeling.

The Gamma distribution produced by :func:`gammavariate` is used for
modeling the sizes of things such as waiting times, rainfall, and
computational errors.

The Weibull distribution computed by :func:`weibullvariate` is used in
failure analysis, industrial engineering, and weather forecasting.  It
describes the distribution of sizes of particles or other discrete
objects.


.. seealso::

   * :pydoc:`random`

   * "Mersenne Twister: A 623-dimensionally equidistributed uniform
     pseudorandom number generator" -- Article by M. Matsumoto
     and T. Nishimura from *ACM Transactions on Modeling and Computer
     Simulation* Vol. 8, No. 1, January pp.3-30 1998.

   * `Wikipedia: Mersenne Twister
     <https://en.wikipedia.org/wiki/Mersenne_twister>`_ -- Article
     about the pseudorandom generator algorithm used by Python.

   * `Wikipedia: Uniform distribution
     <https://en.wikipedia.org/wiki/Uniform_distribution_(continuous)>`_
     -- Article about continuous uniform distributions in statistics.
