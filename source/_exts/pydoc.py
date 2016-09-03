#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2016 Doug Hellmann.  All rights reserved.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software
# and its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Doug Hellmann not be used in advertising or publicity
# pertaining to distribution of the software without specific,
# written prior permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
"""Extension to allow references to Python documentation.

Use the ``:pydoc:`` role in-line, specifying the name of the
module to link to.

For example::

    :pydoc:`xml.etree.ElementTree`

"""

import sys

from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes


PYTHON_VERSION = '{}.{}'.format(*(sys.version_info[:2]))
URL_TEMPLATE = (
    'http://docs.python.org/' +
    PYTHON_VERSION +
    '/library/{}.html'
)
TITLE_TEMPLATE = 'Standard library documentation for {}'


def make_link_node(rawtext, app, module_name, options):
    """Create a link.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param module_name: The real name of the module
    :param options: Options dictionary passed to role func
    """
    set_classes(options)
    node = nodes.reference(
        rawtext,
        TITLE_TEMPLATE.format(module_name),
        refuri=URL_TEMPLATE.format(module_name.lower()),
        **options)
    return node


def pydoc_role(name, rawtext, text, lineno, inliner,
               options={}, content=[]):
    """Link to a Python module documentation page.

    Returns 2 part tuple containing list of nodes to insert into
    the document and a list of system messages.  Both are allowed
    to be empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the
                   input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    module_name = text.strip()
    if not module_name:
        msg = inliner.reporter.error(
            'Module name must not be empty; '
            '%r is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    app = inliner.document.settings.env.app
    # app.info('stdlib module link {!r}\n'.format(text))
    node = make_link_node(rawtext, app, module_name, options)
    return [node], []


def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.info('Initializing BitBucket plugin')
    app.add_role('pydoc', pydoc_role)
