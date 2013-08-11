import os

import paver.doctools  # noqa
from paver.doctools import cog
from paver.easy import options, Bunch, task, consume_args, sh
from paver.path import path
from paver.setuputils import setup

from sphinxcontrib import paverutils  # noqa

# What is the current module being documented?
MODULE = path('module').text().rstrip()
os.environ['MODULE'] = MODULE


setup(
    name="PyMOTW-3",
    packages=[],
    version="0.0",
    url="http://pymotw.com/3/",
    author="Doug Hellmann",
    author_email="doug.hellmann@gmail.com"
)

options(
    sphinx=Bunch(
        docroot='.',
        builddir='build',
        sourcedir='source',
    ),
    cog=Bunch(
        beginspec='{{{cog',
        endspec='}}}',
        endoutput='{{{end}}}',
    ),
    # pdf=Bunch(
    #     builder='latex',
    #     docroot='.',
    #     builddir='build',
    #     sourcedir='source',
    # ),
)


def remake_directories(*dirnames):
    """Remove the directories and recreate them.
    """
    for d in dirnames:
        d = path(d)
        if d.exists():
            d.rmtree()
        d.mkdir()
    return


@task
def html(options):
    "Generate HTML files."
    paverutils.html(options)
    return


@task
def html_clean(options):
    """Remove sphinx output directories before building the HTML.
    """
    remake_directories(options.sphinx.builddir)
    html(options)
    return


def _flake8(infile):
    """Run flake8 against the input file"""
    return sh('flake8 %s' % infile)


@task
def flake8(options):
    """Run flake8 against all of the input files"""
    _flake8(options.sphinx.sourcedir)
    _flake8('pavement.py')


@task
@consume_args
def update(options):
    """Run cog against the named module, then re-build the HTML.

    Examples::

      $ paver update atexit
    """
    options.order('update', 'sphinx', add_rest=True)
    args = getattr(options, 'args', [])
    if args:
        module = args[0]
    else:
        module = MODULE
    module_dir = os.path.join(options.sphinx.sourcedir, module)
    if path(module_dir).isdir():
        _flake8(module_dir)
    options.order('cog', 'sphinx', add_rest=True)
    options.args = [module_dir]
    cog(options)
    html(options)
    return


# @task
# def pdf():
#     """Generate the PDF book.
#     """
#     options.order('pdf', 'sphinx', add_rest=True)
#     paverutils.pdf(options)
#     return
