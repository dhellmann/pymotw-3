===========================================
 random -- Pseudorandom number generators
===========================================

.. module:: random
    :synopsis: Pseudorandom number generators

:Purpose: Implements several types of pseudorandom number generators.
:Available In: 1.4 and later

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

.. include:: random_random.py
   :literal:
   :start-after: #end_pymotw_header

Running the program repeatedly produces different sequences of
numbers.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_random.py'))
.. cog.out(run_script(cog.inFile, 'random_random.py', include_prefix=False))
.. }}}

::

	$ python random_random.py
	
	0.182
	0.155
	0.097
	0.175
	0.008

	$ python random_random.py
	
	0.851
	0.607
	0.700
	0.922
	0.496

.. {{{end}}}

To generate numbers in a specific numerical range, use :func:`uniform`
instead.  

.. include:: random_uniform.py
   :literal:
   :start-after: #end_pymotw_header

Pass minimum and maximum values, and :func:`uniform` adjusts the
return values from :func:`random` using the formula ``min + (max -
min) * random()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_uniform.py'))
.. }}}

::

	$ python random_uniform.py
	
	6.899
	14.411
	96.792
	18.219
	63.386

.. {{{end}}}


Seeding
=======

:func:`random` produces different values each time it is called, and
has a very large period before it repeats any numbers.  This is useful
for producing unique values or variations, but there are times when
having the same dataset available to be processed in different ways is
useful.  One technique is to use a program to generate random values
and save them to be processed by a separate step.  That may not be
practical for large amounts of data, though, so :mod:`random` includes
the :func:`seed` function for initializing the pseudorandom generator
so that it produces an expected set of values.

.. include:: random_seed.py
   :literal:
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

	$ python random_seed.py
	
	0.134
	0.847
	0.764
	0.255
	0.495

	$ python random_seed.py
	
	0.134
	0.847
	0.764
	0.255
	0.495

.. {{{end}}}


Saving State
============

Another technique useful for controlling the number sequence is to
save the internal state of the generator between test runs.  Restoring
the previous state before continuing reduces the likelyhood of
repeating values or sequences of values from the earlier input.  The
:func:`getstate` function returns data that can be used to
re-initialize the random number generator later with :func:`setstate`.

.. include:: random_state.py
   :literal:
   :start-after: #end_pymotw_header

The data returned by :func:`getstate` is an implementation detail, so
this example saves the data to a file with :mod:`pickle` but otherwise
treats it as a black box.  If the file exists when the program starts,
it loads the old state and continues.  Each run produces a few numbers
before and after saving the state, to show that restoring the state
causes the generator to produce the same values again.

.. {{{cog
.. (path(cog.inFile).dirname() / 'state.dat').unlink()
.. cog.out(run_script(cog.inFile, 'random_state.py'))
.. cog.out(run_script(cog.inFile, 'random_state.py', include_prefix=False))
.. }}}

::

	$ python random_state.py
	
	No state.dat, seeding
	0.134
	0.847
	0.764
	
	After saving state:
	0.255
	0.495
	0.449

	$ python random_state.py
	
	Found state.dat, initializing random module
	0.255
	0.495
	0.449
	
	After saving state:
	0.652
	0.789
	0.094

.. {{{end}}}


Random Integers
===============

:func:`random` generates floating point numbers.  It is possible to
convert the results to integers, but using :func:`randint` to generate
integers directly is more convenient.

.. include:: random_randint.py
   :literal:
   :start-after: #end_pymotw_header

The arguments to :func:`randint` are the ends of the inclusive range
for the values.  The numbers can be positive or negative, but the
first value should be less than the second.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_randint.py'))
.. }}}

::

	$ python random_randint.py
	
	[1, 100]:
	3
	47
	72
	
	[-5, 5]:
	4
	1
	-3

.. {{{end}}}

:func:`randrange` is a more general form of selecting values from a
range.  

.. include:: random_randrange.py
   :literal:
   :start-after: #end_pymotw_header

:func:`randrange` supports a *step* argument, in addition to start and
stop values, so it is fully equivalent to selecting a random value
from ``range(start, stop, step)``.  It is more efficient, because the
range is not actually constructed.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_randrange.py'))
.. }}}

::

	$ python random_randrange.py
	
	50
	55
	45

.. {{{end}}}


Picking Random Items
====================

One common use for random number generators is to select a random item
from a sequence of enumerated values, even if those values are not
numbers.  :mod:`random` includes the :func:`choice` function for
making a random selection from a sequence.  This example simulates
flipping a coin 10,000 times to count how many times it comes up heads
and how many times tails.

.. include:: random_choice.py
   :literal:
   :start-after: #end_pymotw_header

There are only two outcomes allowed, so rather than use numbers and
convert them the words "heads" and "tails" are used with
:func:`choice`.  The results are tabulated in a dictionary using the
outcome names as keys.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_choice.py'))
.. }}}

::

	$ python random_choice.py
	
	Heads: 5069
	Tails: 4931

.. {{{end}}}


Permutations
============

A simulation of a card game needs to mix up the deck of cards and then
"deal" them to the players, without using the same card more than
once.  Using :func:`choice` could result in the same card being dealt
twice, so instead the deck can be mixed up with :func:`shuffle` and
then individual cards removed as they are dealt.

.. include:: random_shuffle.py
   :literal:
   :start-after: #end_pymotw_header

The cards are represented as tuples with the face value and a letter
indicating the suit.  The dealt "hands" are created by adding one card
at a time to each of four lists, and removing it from the deck so it
cannot be dealt again.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_shuffle.py'))
.. }}}

::

	$ python random_shuffle.py
	
	Initial deck:
	 2H  2D  2C  2S  3H  3D  3C  3S  4H  4D  4C  4S  5H
	 5D  5C  5S  6H  6D  6C  6S  7H  7D  7C  7S  8H  8D
	 8C  8S  9H  9D  9C  9S 10H 10D 10C 10S  JH  JD  JC
	 JS  QH  QD  QC  QS  KH  KD  KC  KS  AH  AD  AC  AS
	
	Shuffled deck:
	 4C  3H  AD  JH  7D  3D  5C  6D  5D  7S  5S  KH  8S
	 QC  5H  7C  4D  4S  2H  JD  KD  AH 10S  KC  6C  6H
	 8H 10H  QD  AC  2S  7H  JC  9S  AS  8C  QH  9D  4H
	 8D  JS  2D  3S  9C 10D  3C  6S  2C  QS  KS 10C  9H
	
	Hands:
	1:  9H  2C  9C  8D  8C
	2: 10C  6S  3S  4H  AS
	3:  KS  3C  2D  9D  9S
	4:  QS 10D  JS  QH  JC
	
	Remaining deck:
	 4C  3H  AD  JH  7D  3D  5C  6D  5D  7S  5S  KH  8S
	 QC  5H  7C  4D  4S  2H  JD  KD  AH 10S  KC  6C  6H
	 8H 10H  QD  AC  2S  7H

.. {{{end}}}

Many simulations need random samples from a population of input
values.  The :func:`sample` function generates samples without
repeating values and without modifying the input sequence.  This
example prints a random sample of words from the system dictionary.

.. include:: random_sample.py
   :literal:
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
number generators.  All of the functions described above are available
as methods of the :class:`Random` instances, and each instance can be
initialized and used separately, without interfering with the values
returned by other instances.

.. include:: random_random_class.py
   :literal:
   :start-after: #end_pymotw_header

On a system with good native random value seeding, the instances start
out in unique states.  However, if there is no good platform random
value generator, the instances are likely to have been seeded with the
current time, and therefore produce the same values.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_random_class.py'))
.. }}}

::

	$ python random_random_class.py
	
	Default initializiation:
	
	0.171  0.711
	0.184  0.558
	0.818  0.113
	
	Same seed:
	
	0.857  0.857
	0.925  0.925
	0.040  0.040

.. {{{end}}}

To ensure that the generators produce values from different parts of
the random period, use :func:`jumpahead` to shift one of them away
from its initial state.

.. include:: random_jumpahead.py
   :literal:
   :start-after: #end_pymotw_header

The argument to :func:`jumpahead` should be a non-negative integer
based the number of values needed from each generator.  The internal
state of the generator is scrambled based on the input value, but not
simply by incrementing it by the number of steps given.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_jumpahead.py'))
.. }}}

::

	$ python random_jumpahead.py
	
	0.405  0.159
	0.592  0.765
	0.501  0.764

.. {{{end}}}

SystemRandom
============

Some operating systems provide a random number generator that has
access to more sources of entropy that can be introduced into the
generator.  :mod:`random` exposes this feature through the
:class:`SystemRandom` class, which has the same API as :class:`Random`
but uses :func:`os.urandom` to generate the values that form the basis
of all of the other algorithms.

.. include:: random_system_random.py
   :literal:
   :start-after: #end_pymotw_header

Sequences produced by :class:`SystemRandom` are not reproducable
because the randomness is coming from the system, rather than software
state (in fact, :func:`seed` and :func:`setstate` have no effect at
all).

.. {{{cog
.. cog.out(run_script(cog.inFile, 'random_system_random.py'))
.. }}}

::

	$ python random_system_random.py
	
	Default initializiation:
	
	0.374  0.932
	0.002  0.022
	0.692  1.000
	
	Same seed:
	
	0.182  0.939
	0.154  0.430
	0.649  0.970

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
phenomena and was popularized by Chris Anderon's book, *The Long
Tail*.  The :func:`paretovariate` function is useful for simulating
allocation of resources to individuals (wealth to people, demand for
musicians, attention to blogs, etc.).

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

    `random <http://docs.python.org/2.7/library/random.html>`_
        The standard library documentation for this module.

    Mersenne Twister: A 623-dimensionally equidistributed uniform pseudorandom number generator
        Article by M. Matsumoto and T. Nishimura from *ACM
        Transactions on Modeling and Computer Simulation* Vol. 8,
        No. 1, January pp.3-30 1998.

    `Wikipedia: Mersenne Twister <http://en.wikipedia.org/wiki/Mersenne_twister>`_
        Article about the pseudorandom generator algorithm used by Python.

    `Wikipedia: Uniform distribution <http://en.wikipedia.org/wiki/Uniform_distribution_(continuous)>`_
        Article about continuous uniform distributions in statistics.
