import configparser
import functools
import http.server
import os
import subprocess
import sys

from paver.easy import options, Bunch, task, consume_args, sh, info, error, cmdopts, dry, needs
from paver.path import path
from paver.setuputils import setup

import pyquery

from sphinxcontrib import paverutils  # noqa
from sphinxcontrib.paverutils import cog, run_script

import wordpress_xmlrpc
import wordpress_xmlrpc.exceptions

import pybitbucket.auth as pybb_auth
import pybitbucket.bitbucket as pybb_bb
import pybitbucket.repository as pybb_repo
import uritemplate
import urllib.parse
import pprint

# Set PYTHONHASHSEED so ensure the "randomness" for mapping-related
# items is always the same between runs to avoid unnecessary cog
# updates.
os.environ['PYTHONHASHSEED'] = '19710329'


setup(
    name="PyMOTW-3",
    packages=[],
    version="1.1",
    url="https://pymotw.com/3/",
    author="Doug Hellmann",
    author_email="doug@doughellmann.com"
)

options(

    sphinx=Bunch(
        docroot='.',
        builddir='build',
        sourcedir='source',
        warnerror=True,
    ),

    # Some of the files include [[[ as part of a nested list data
    # structure, so change the tags cog looks for to something
    # less likely to appear.
    cog=Bunch(
        beginspec='{{{cog',
        endspec='}}}',
        endoutput='{{{end}}}',
    ),

    pdf=Bunch(
        builder='latex',
        docroot='.',
        builddir='build',
        sourcedir='source',
        pdflatex='xelatex',
        pygments_style='bw',
        warnerror=False,
    ),

    linkcheck=Bunch(
        builder='linkcheck',
        docroot='.',
        builddir='build',
        sourcedir='source',
        warnerror=False,
    ),

    website=Bunch(
        # What server hosts the website?
        server='pymotw.com',
        server_path='/home/douhel3shell/pymotw.com/3/',
    ),

    testsite=Bunch(
        # Where do we put the files for local testing?
        local_path='/Users/dhellmann/Sites/pymotw.com/3',
    ),

    sitemap_gen=Bunch(
        # Where is the config file for sitemap_gen.py?
        config='sitemap_gen_config.xml',
    ),

    migrate=Bunch(
        old_locs=[
            '../../Python2/book-git/PyMOTW/',
            '../../Python2/src/PyMOTW/',
        ],
    ),

    blog=Bunch(
        outdir='blog_posts',
        in_file='index.html',
        out_file='blog.html',
        no_edit=False,
        url_base='https://pymotw.com/3/',
    ),

)


def _elide_path_prefix(infile, line):
    """Replace any absolute path references to my working dir with ...
    """
    rundir = os.path.abspath(path(infile).dirname())
    line = line.replace(rundir, '...')
    if 'VIRTUAL_ENV' in os.environ:
        line = line.replace(os.environ['VIRTUAL_ENV'], '...')
    line = line.replace(
        '/Library/Frameworks/Python.framework/Versions/{}.{}'.format(
            *sys.version_info[:2]),
        '...')
    return line


def _truncate_lines(infile, line, c):
    """Replace long sequences of single characters with a shorter version.
    """
    if set(line) == set(c) and len(line) > 64:
        line = c * 64
    return line


# Replace run_script with local wrapper
def run_script(input_file, script_name, break_lines_at=64, **kwds):
    if 'line_cleanups' not in kwds:
        kwds['line_cleanups'] = [
            _elide_path_prefix,
            functools.partial(_truncate_lines, c='-'),
            functools.partial(_truncate_lines, c='='),
            functools.partial(_truncate_lines, c='*'),
        ]
    return paverutils.run_script(input_file, script_name,
                                 break_lines_at=break_lines_at,
                                 **kwds)

def safe_unlink(pathname):
    "Remove a file, but only if it exists."
    print('safe_unlink({})'.format(pathname))
    p = path(pathname)
    if not p.exists():
        return
    if p.isdir():
        p.rmtree()
    else:
        p.unlink()


# Stuff commonly used symbols into the builtins so we don't have to
# import them in all of the cog blocks where we want to use them.
__builtins__['run_script'] = run_script
__builtins__['path'] = path
__builtins__['sh'] = sh
__builtins__['unlink'] = safe_unlink


def remake_directories(*dirnames):
    """Remove the directories and recreate them.
    """
    for d in dirnames:
        safe_unlink(d)
        path(d).mkdir()
    return


@task
def clean(options):
    remake_directories(options.sphinx.builddir)


@task
def css(options):
    "Generate CSS from less"
    src_path = 'source/_themes/pymotw/static/'
    file_base = 'pymotw'
    outfile = path(src_path + file_base + '.css')
    rebuild = False
    if not outfile.exists() or path(src_path + file_base + '.less').mtime > outfile.mtime:
        rebuild = True
    elif path(src_path + 'vars.less').mtime > outfile.mtime:
        rebuild = True
    if rebuild:
        sh('lessc %(file_base)s.less > %(file_base)s.css' % {
            'file_base': src_path + file_base,
        })
        path(src_path + file_base + '.css').copy(
            options.sphinx.builddir + '/html/_static/pymotw.css')


@task
def html(options):
    "Generate HTML files."
    paverutils.html(options)
    css(options)
    return


@task
def html_clean(options):
    """Remove sphinx output directories before building the HTML.
    """
    clean(options)
    html(options)
    return


def _get_branch_name():
    """Look at git for our branch name."""
    out = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
    )
    out = out.strip()
    return out.decode('utf-8')


def _get_module(options):
    """Return the name of module passed as arg or the default.
    """
    module = None
    args = getattr(options, 'args', [])
    if args:
        module = args[0]
        info('using argument for module: %s' % module)
    branch = _get_branch_name()
    if branch.startswith('module/'):
        module = branch.partition('/')[-1]
        info('using git branch for module: %s' % module)
    if not module:
        try:
            module = path('module').text().rstrip()
        except:
            pass
        else:
            info('read module from file: %s' % module)
    if not module:
        error('could not determine the module')
    return module


def _flake8(infile):
    """Run flake8 against the input file"""
    return sh('flake8 -v %s' % infile)


@task
def flake8(options):
    """Run flake8 against all of the input files"""
    options.order('flake8', 'sphinx', add_rest=True)
    module = _get_module(options)
    if module:
        module_dir = os.path.join(options.sphinx.sourcedir, module)
        _flake8(module_dir)
    else:
        _flake8(options.sphinx.sourcedir)


@task
@consume_args
def update(options):
    """Run cog against the named module, then re-build the HTML.

    Examples::

      $ paver update atexit
    """
    options.order('update', 'sphinx', add_rest=True)
    module = _get_module(options)
    module_dir = os.path.join(options.sphinx.sourcedir, module)
    if path(module_dir).isdir():
        _flake8(module_dir)
    options.order('cog', 'sphinx', add_rest=True)
    options.args = [module_dir]
    cog(options)
    html(options)
    return


@task
def pdf():
    """Generate the PDF book.
    """
    options.order('pdf', 'sphinx', add_rest=True)
    os.environ['_PYGMENTS_STYLE'] = options.pygments_style
    os.environ['_BUILDING_BOOK'] = 'True'
    paverutils.pdf(options)
    return


@task
def linkcheck():
    """Check outgoing links
    """
    options.order('linkcheck', 'sphinx', add_rest=True)
    paverutils.run_sphinx(options, 'linkcheck')
    return


@task
def rsyncwebsite(options):
    # Copy to the server
    os.environ['RSYNC_RSH'] = '/usr/bin/ssh'
    src_path = path(options.sphinx.builddir) / 'html'
    sh('(cd %s; rsync --archive --delete --verbose . %s:%s)' %
        (src_path, options.website.server,
         options.website.server_path))
    return


@task
def test(options):
    # Copy to the local site
    src_path = path(options.sphinx.builddir) / 'html'
    os.chdir(src_path)
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address,
                                   http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()
    return


@task
def buildsitemap(options):
    sh('python2 ./bin/sitemap_gen.py --testing --config=%s' %
       options.sitemap_gen.config)
    return


@task
def notify_google(options):
    # Tell Google there is a new sitemap. This is sort of hacky,
    # since we regenerate the sitemap locally but Google fetches
    # the one we just copied to the remote site.
    # sh('python2 ./bin/sitemap_gen.py --config=%s'
    #    % options.sitemap_gen.config)
    return


@task
@needs('setuptools.command.sdist')
def sdist(options):
    for archive in path('dist').glob('*.tar.gz'):
        archive.copy(options.sphinx.builddir + '/html')


@task
def deploy(options):
    """Rebuild and copy website files to the remote server.
    """
    # Rebuild
    html_clean(options)
    # Copy the sdist into the html output directory.
    sdist(options)
    # Rebuild the site-map
    buildsitemap(options)
    # Install
    rsyncwebsite(options)
    # Update Google
    notify_google(options)
    return


@task
def push(options):
    """Push changes to remote git repository.
    """
    sh('git push')


@task
def publish(options):
    deploy(options)
    push(options)


@task
def common_cleanups(options):
    module = _get_module(options)
    sh('sed -i "" -e "s/.. include::/.. literalinclude::/g" source/%s/*.rst' % module)
    sh('sed -i "" -e "s/:literal:/:caption:/g" source/%s/*.rst' % module)
    sh("sed -i '' -e '/:Python Version:/d' source/%s/index.rst" % module)
    sh("sed -i '' -e 's/()`/`/g' source/%s/*.rst" % module)
    if path('source/{}'.format(module)).glob('*.py'):
        sh("sed -i '' -e 's|#!/usr/bin/env python$|#!/usr/bin/env python3|' source/%s/*.py" % module)
        sh("sed -i '' -e '/__version__ = \"$Id$\"/d' source/%s/*.py" % module)
        sh("sed -i '' -e '/__module_id__ = \'$Id$\'/d' source/%s/*.py" % module)
    else:
        print('*** skipping changes to *.py, no python modules found')

@task
def manual_review_cleanups(options):
    module = _get_module(options)
    if not path('source/{}'.format(module)).glob('*.py'):
        print('*** skipping changes to *.py, no python modules found')
        return
    sh("sed -i '' -e 's|print \(.*\)|print(\\1)|g' source/%s/*.py" % module)
    sh("sed -i '' -e 's|print$|print()|g' source/%s/*.py" % module)
    sh("sed -i '' -e 's|(object):|:|g' source/%s/*.py" % module)
    sh("sed -i '' -e 's/^ *$//g' source/%s/*.py" % module)


@task
@consume_args
def migrate(options):
    "Copy old content into place to prepare for updating"
    args = getattr(options, 'args', [])
    options.order('update', 'sphinx', add_rest=True)
    module = _get_module(options)
    # The source module name might be different from the destination
    # module name, so look for an explicit argument for the source.
    source = module
    args = getattr(options, 'args', [])
    if args:
        source = args[0]
    dest = path('source/' + module)
    if dest.exists():
        raise ValueError('%s already exists' % dest)
    for src_path in options.migrate.old_locs:
        the_src = path(src_path + '/' + source)
        if not the_src.exists():
            print('did not find {}'.format(the_src))
            continue
        the_src.copytree(dest)
        break
    (dest + '/__init__.py').remove()
    if source != module:
        # Rename any modules that have the old source module name to
        # use the new source module name. Since some modules are now
        # part of packages, replace '.' with _' in the example
        # filenames.
        module_prefix = module.replace('.', '_')
        for srcfile in dest.glob(source + '_*.py'):
            newname = srcfile.name.replace(source + '_', module_prefix + '_')
            srcfile.rename(dest + '/' + newname)
    sh('git add ' + dest)
    sh('git commit -m "%s: initial import"' % module)
    common_cleanups(options)
    sh('git add ' + dest)
    sh('git commit -m "%s: common cleanups"' % module)
    manual_review_cleanups(options)


def get_post_title(filename):
    with open(filename, 'r') as f:
        body = f.read()

    doc = pyquery.PyQuery(body)
    h1 = doc('h1')
    return h1.text


def gen_blog_post_from_page(input_file, module, url_base):
    """Generate the blog post body and title
    """
    canonical_url = url_base.rstrip('/') + '/' + module + '/'
    if not input_file.endswith("index.html"):
        canonical_url += input_base

    print('reading from {}'.format(input_file))
    raw_body = input_file.text().strip()
    doc = pyquery.PyQuery(raw_body)

    # Get the title, removing any anchors for the header in the
    # process
    title = doc('h1').remove('a').text()
    if module not in title:
        title = '{} - {}'.format(module, title)
    if 'PyMOTW 3' not in title:
        title = '{} — PyMOTW 3'.format(title)

    # Get the intro paragraph
    intro = doc('p').eq(0)

    # Convert the paragraph to simple text, removing all formatting.
    intro = intro.text().replace('\n', ' ')

    output_body = '''<p>{intro}</p>
<p><a href="{canonical_url}">Read more...</a></p>
<p><small>This post is part of the Python Module of the Week series for Python 3. See <a href="https://pymotw.com/3/">PyMOTW.com</a> for more articles from the series.</small></p>
'''.format(intro=intro, canonical_url=canonical_url)

    return (title, output_body)

def post_draft(title, body):
    cfg_filename = path('~/.wphelper').expanduser()
    cfg = configparser.ConfigParser()
    if not cfg.read(cfg_filename):
        raise RuntimeError('Did not find configuration file {}'.format(cfg_filename))
    site_url = cfg['site']['url']
    xmlrpc_url = site_url + '/xmlrpc.php'
    username = cfg['site']['username']
    password = cfg['site']['password']
    wp = wordpress_xmlrpc.Client(xmlrpc_url, username, password)
    post = wordpress_xmlrpc.WordPressPost()
    post.title = title
    post.content = body
    post.post_status = 'draft'
    post.terms_names = {
        'post_tag': ['PyMOTW', 'python'],
    }
    wp.call(wordpress_xmlrpc.methods.posts.NewPost(post))


@task
@consume_args
@cmdopts([
    ('in-file=', 'b', 'Blog input filename (e.g., "-b index.html")'),
])
def blog(options):
    """Generate the blog post version of the HTML for the current module.

    The default behavior generates the post for the current module using
    its index.html file as input.

    To use a different file within the module directory, use the
    --in-file or -b option::

      paver blog -b communication.html

    To run against a directory other than a module, use the
    -s or --sourcedir option::

      paver blog -s PyMOTW/articles -b text_processing.html
    """
    options.order('blog', 'sphinx', add_rest=True)
    module = _get_module(options)

    # Create output directory
    out = path(options.outdir)
    if not out.exists():
        out.mkdir()

    blog_file = path(options.outdir) / module + '.html'
    title, body = dry(
        'building blog post body',
        gen_blog_post_from_page,
        input_file=path(options.builddir) / 'html' / module / options.in_file,
        module=module,
        url_base=options.url_base,
    )
    print('title {!r}'.format(title))
    post_draft(title, body)
    return


@task
@consume_args
def review_task(options):
    """Create a bitbucket issue for reviewing a module.
    """
    module = _get_module(options)
    if not module:
        raise RuntimeError('could not determine which module to use')

    cfg_filename = path('~/.bitbucketrc').expanduser()
    cfg = configparser.ConfigParser()
    if not cfg.read(cfg_filename):
        raise RuntimeError('Did not find configuration file {}'.format(cfg_filename))

    auth = pybb_auth.OAuth1Authenticator(
        client_key=cfg['bitbucket']['client_key'],
        client_secret=cfg['bitbucket']['client_secret'],
        client_email=cfg['bitbucket']['email'],
    )

    client = pybb_bb.Client(auth)

    repo = pybb_repo.Repository.find_repository_by_name_and_owner(
        repository_name='pymotw-3',
        owner='dhellmann',
        client=client,
    )

    # The client library doesn't have issue support yet, so we have to
    # do it by hand.
    url_template = repo.v1.get_link_template('issues')
    url = uritemplate.expand(
        url_template,
        {'bitbucket_url': client.get_bitbucket_url(),
         'owner': 'dhellmann',
         'repository_name': 'pymotw-3',
        },
    )
    args = {
        'title': 'technical review for {}'.format(module),
        'content': 'Perform the technical review for {}'.format(module),
        'kind': 'task',
        'priority': 'minor',
    }
    encoded = urllib.parse.urlencode(args)

    response = repo.v1.post(
        url=url,
        client=client,
        data=encoded,
    )
    pprint.pprint(response)
    print()
    task_url = 'https://bitbucket.org/dhellmann/pymotw-3/issues/{}'.format(
        response['local_id'])
    print(task_url)
