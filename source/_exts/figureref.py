#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
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
"""Extension to allow references to figures.
"""

import functools

from docutils import nodes, utils


class figureref(nodes.reference):
    pass


def _role(typ, rawtext, text, lineno, inliner,
          options={}, content=[], nodeclass=None):
    text = utils.unescape(text)
    pnode = nodeclass(
        rawsource=text,
        text='',
        internal=True,
        refuri=text,
    )
    return [pnode], []


def latex_visit_figureref(self, node):
    id = 'figure:' + node['refuri']
    self.body.append(r'Figure~\ref{%s}' % self.idescape(id))
    raise nodes.SkipNode


def latex_depart_figureref(self, node):
    return


def html_visit_figureref(self, node):
    self.body.append(r'the figure')
    raise nodes.SkipNode


def html_depart_figureref(self, node):
    return


def builder_inited(app):
    app.info('defining figure role')
    app.add_role(
        'figure',
        functools.partial(_role, nodeclass=figureref)
    )


def setup(app):
    app.info('initializing figureref')
    app.add_node(
        figureref,
        latex=(latex_visit_figureref, None),
        pearson=(latex_visit_figureref, None),
        html=(html_visit_figureref, html_depart_figureref),
    )
    app.connect('builder-inited', builder_inited)
