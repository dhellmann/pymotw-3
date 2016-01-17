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

::

	$ python3 random_random.py
	
	0.215 0.423 0.595 0.567 0.488 

	$ python3 random_random.py
	
	0.796 0.368 0.999 0.037 0.722 

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

::

	$ python3 random_uniform.py
	
	60.362 12.397 15.175 49.360 39.348 

.. {{{end}}}


Seeding
=======

:func:`random` produces different values each time it is called, and
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
is available.  Otherwise the current time is used.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_seed.py'))
.. cog.out(run_script(cog.inFile, 'random_seed.py', include_prefix=False))
.. }}}

::

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
.. state_file = path(cog.inFile).dirname() / 'state.dat'
.. if state_file.exists():
..   state_file.unlink()
.. cog.out(run_script(cog.inFile, 'random_state.py'))
.. cog.out(run_script(cog.inFile, 'random_state.py', include_prefix=False))
.. }}}

::

	$ python3 random_state.py
	
	Found state.dat, initializing random module
	0.217 0.422 0.029 
	
	After saving state:
	0.222 0.438 0.496 

	$ python3 random_state.py
	
	Found state.dat, initializing random module
	0.222 0.438 0.496 
	
	After saving state:
	0.233 0.231 0.219 

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

::

	$ python3 random_randint.py
	
	[1, 100]: 55 43 96 
	[-5, 5]: -2 1 -3 

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

::

	$ python3 random_randrange.py
	
	75 15 20 

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

::

	$ python3 random_choice.py
	
	Heads: 5035
	Tails: 4965

.. {{{end}}}


Permutations
============

A simulation of a card game needs to mix up the deck of cards and then
deal them to the players, without using the same card more than
once.  Using :func:`choice` could result in the same card being dealt
twice, so instead the deck can be mixed up with :func:`shuffle` and
then individual cards removed as they are dealt.

.. literalinclude:: random_shuffle.py
   :caption:
   :start-after: #end_pymotw_header

The cards are represented as tuples with the face value and a letter
indicating the suit.  The dealt "hands" are created by adding one card
at a time to each of four lists, and removing it from the deck so it
cannot be dealt again.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_shuffle.py'))
.. }}}

::

	$ python3 random_shuffle.py
	
	Initial deck:
	 2H  2D  2C  2S  3H  3D  3C  3S  4H  4D  4C  4S  5H 
	 5D  5C  5S  6H  6D  6C  6S  7H  7D  7C  7S  8H  8D 
	 8C  8S  9H  9D  9C  9S 10H 10D 10C 10S  JH  JD  JC 
	 JS  QH  QD  QC  QS  KH  KD  KC  KS  AH  AD  AC  AS 
	
	Shuffled deck:
	 JS  4H  2H  3H  QD  9S  AD  2C  7H  QC  8D  6C  KS 
	 KD  3D  KH  5D  AC  JD  JH  9D 10D  5S  7C  7D  AH 
	 4D  4S  8S  8H  AS  9H 10H  3C  QS 10C  5C  6H  9C 
	 5H  6D  QH 10S  4C  KC  2D  3S  7S  8C  JC  2S  6S 
	
	Hands:
	1:  6S  7S  4C  5H 10C 
	2:  2S  3S 10S  9C  QS 
	3:  JC  2D  QH  6H  3C 
	4:  8C  KC  6D  5C 10H 
	
	Remaining deck:
	 JS  4H  2H  3H  QD  9S  AD  2C  7H  QC  8D  6C  KS 
	 KD  3D  KH  5D  AC  JD  JH  9D 10D  5S  7C  7D  AH 
	 4D  4S  8S  8H  AS  9H 

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

::

	$ python random_sample.py

	pleasureman
	consequency
	docibility
	youdendrift
	Ituraean

	$ python random_sample.py

	jigamaree
	readingdom
	sporidium
	pansylike
	foraminiferan


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

::

	$ python3 random_random_class.py
	
	Default initializiation:
	
	0.827  0.300
	0.733  0.864
	0.168  0.322
	
	Same seed:
	
	0.337  0.337
	0.102  0.102
	0.847  0.847

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

::

	$ python3 random_system_random.py
	
	Default initializiation:
	
	0.286  0.889
	0.350  0.723
	0.737  0.001
	
	Same seed:
	
	0.172  0.293
	0.330  0.617
	0.353  0.635

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

    `random <http://docs.python.org/library/random.html>`_
        The standard library documentation for this module.

    Mersenne Twister: A 623-dimensionally equidistributed uniform pseudorandom number generator
        Article by M. Matsumoto and T. Nishimura from *ACM
        Transactions on Modeling and Computer Simulation* Vol. 8,
        No. 1, January pp.3-30 1998.

    `Wikipedia: Mersenne Twister <http://en.wikipedia.org/wiki/Mersenne_twister>`_
        Article about the pseudorandom generator algorithm used by Python.

    `Wikipedia: Uniform distribution <http://en.wikipedia.org/wiki/Uniform_distribution_(continuous)>`_
        Article about continuous uniform distributions in statistics.
