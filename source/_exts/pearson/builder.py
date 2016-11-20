# -*- coding: utf-8 -*-
"""LaTeX builder using Pearson style templates.
"""

import os
from os import path
import warnings

from six import iteritems
from docutils import nodes
from docutils.io import FileOutput
from docutils.utils import new_document
from docutils.frontend import OptionParser

from sphinx import package_dir, addnodes
from sphinx.util import texescape
from sphinx.util import jsonimpl, copy_static_entry, copy_extra_entry
from sphinx.errors import SphinxError
from sphinx.locale import _
from sphinx.builders import Builder
from sphinx.environment import NoUri
from sphinx.theming import Theme
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import SEP, copyfile
from sphinx.util.console import bold, darkgreen

from pearson import writer


_package_dir = path.abspath(path.dirname(__file__))


class PearsonLaTeXBuilder(Builder):
    """
    Builds LaTeX output to create PDF.
    """
    name = 'pearson'
    format = 'latex'
    supported_image_types = ['application/pdf', 'image/png', 'image/jpeg']
    usepackages = []

    # Modified by init_templates()
    theme = None

    def init(self):
        self.info('loading builder from Pearson extension')
        self.docnames = []
        self.document_data = []
        self.init_templates()
        texescape.init()
        self.check_options()

    def check_options(self):
        if self.config.latex_toplevel_sectioning not in (None, 'part', 'chapter', 'section'):
            self.warn('invalid latex_toplevel_sectioning, ignored: %s' %
                      self.config.latex_top_sectionlevel)
            self.config.latex_top_sectionlevel = None

        if self.config.latex_use_parts:
            warnings.warn('latex_use_parts will be removed at Sphinx-1.5. '
                          'Use latex_toplevel_sectioning instead.',
                          DeprecationWarning)

            if self.config.latex_toplevel_sectioning:
                self.warn('latex_use_parts conflicts with latex_toplevel_sectioning, ignored.')

    def get_outdated_docs(self):
        return 'all documents'  # for now

    def get_target_uri(self, docname, typ=None):
        if docname not in self.docnames:
            raise NoUri
        else:
            return '%' + docname

    def get_relative_uri(self, from_, to, typ=None):
        # ignore source path
        return self.get_target_uri(to, typ)

    def get_theme_config(self):
        return self.config.pearson_theme, self.config.pearson_theme_options

    def init_templates(self):
        Theme.init_themes(
            self.confdir,
            [path.join(_package_dir, 'themes')] + self.config.pearson_theme_path,
            warn=self.warn,
        )
        themename, themeoptions = self.get_theme_config()
        self.theme = Theme(themename, warn=self.warn)
        self.theme_options = themeoptions.copy()
        self.create_template_bridge()
        self.templates.init(self, self.theme)

    def init_chapters(self):
        chapters = list(self.config.pearson_chapters)
        if not chapters:
            self.warn('no "pearson_chapters" config value found; no documents '
                      'will be written')
            return

        for chap in chapters:
            if chap not in self.env.all_docs:
                self.warn('"pearson_chapters" config value references unknown '
                          'document %s' % chap)
                continue
            self.document_data.append(chap)

    # def init_document_data(self):
    #     preliminary_document_data = [list(x) for x in self.config.latex_documents]
    #     if not preliminary_document_data:
    #         self.warn('no "latex_documents" config value found; no documents '
    #                   'will be written')
    #         return
    #     # assign subdirs to titles
    #     self.titles = []
    #     for entry in preliminary_document_data:
    #         docname = entry[0]
    #         if docname not in self.env.all_docs:
    #             self.warn('"latex_documents" config value references unknown '
    #                       'document %s' % docname)
    #             continue
    #         self.document_data.append(entry)
    #         if docname.endswith(SEP+'index'):
    #             docname = docname[:-5]
    #         self.titles.append((docname, entry[2]))

    def _render_template(self, template_name, file_name, context):
        self.info('writing {}'.format(file_name))
        output = FileOutput(
            destination_path=file_name,
            encoding='utf-8',
        )
        try:
            body = self.templates.render(template_name, context)
        except Exception as err:
            self.info(bold('Failed to render template {}: {} at {}'.format(
                template_name, err, err.lineno))
            )
            raise
        output.write(body)
        return body

    def write(self, *ignored):
        docwriter = writer.PearsonLaTeXWriter(self)
        docsettings = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,),
            read_config_files=True).get_default_values()

        self.init_chapters()

        # Build up a context object for the templates.
        global_context = {
            'title': self.config.pearson_title,
            'subtitle': self.config.pearson_subtitle,
            'author': self.config.pearson_author,
            'chapter_names': [],
        }

        self._render_template(
            'half-title.tex',
            path.join(self.outdir, 'half-title.tex'),
            global_context,
        )
        self._render_template(
            'title.tex',
            path.join(self.outdir, 'title.tex'),
            global_context,
        )

        chap_name_fmt = 'chap{:02d}'
        if len(self.document_data) >= 100:
            chap_name_fmt = 'chap{:03d}'

        for chap_num, docname in enumerate(self.document_data, 1):
            toctree_only = False
            chap_name = chap_name_fmt.format(chap_num)
            global_context['chapter_names'].append(chap_name)
            destination = FileOutput(
                destination_path=path.join(self.outdir, chap_name + '.tex'),
                encoding='utf-8')
            self.info('writing {} to {}.tex ... '.format(docname, chap_name), nonl=1)
            toctrees = self.env.get_doctree(docname).traverse(addnodes.toctree)
            if toctrees:
                if toctrees[0].get('maxdepth') > 0:
                    tocdepth = toctrees[0].get('maxdepth')
                else:
                    tocdepth = None
            else:
                tocdepth = None
            doctree = self.assemble_doctree(
                docname,
                toctree_only,
                appendices=[],
                #appendices=((docclass != 'howto') and self.config.latex_appendices or [])
            )
            doctree['tocdepth'] = tocdepth
            self.post_process_images(doctree)
#            import pdb; pdb.set_trace()
            self.info("writing... ", nonl=1)
            doctree.settings = docsettings
            # doctree.settings.author = author
            # doctree.settings.title = title
            doctree.settings.contentsname = self.get_contentsname(docname)
            doctree.settings.docname = docname
            # doctree.settings.docclass = docclass
            docwriter.write(doctree, destination)
            self.info("done")

    def get_contentsname(self, indexfile):
        tree = self.env.get_doctree(indexfile)
        contentsname = None
        for toctree in tree.traverse(addnodes.toctree):
            if 'caption' in toctree:
                contentsname = toctree['caption']
                break

        return contentsname

    def assemble_doctree(self, indexfile, toctree_only, appendices):
        self.docnames = set([indexfile] + appendices)
        self.info(darkgreen(indexfile) + " ", nonl=1)
        tree = self.env.get_doctree(indexfile)
        tree['docname'] = indexfile
        if toctree_only:
            # extract toctree nodes from the tree and put them in a
            # fresh document
            new_tree = new_document('<latex output>')
            new_sect = nodes.section()
            new_sect += nodes.title(u'<Set title in conf.py>',
                                    u'<Set title in conf.py>')
            new_tree += new_sect
            for node in tree.traverse(addnodes.toctree):
                new_sect += node
            tree = new_tree
        largetree = inline_all_toctrees(self, self.docnames, indexfile, tree,
                                        darkgreen, [indexfile])
        largetree['docname'] = indexfile
        for docname in appendices:
            appendix = self.env.get_doctree(docname)
            appendix['docname'] = docname
            largetree.append(appendix)
        self.info()
        self.info("resolving references...")
        self.env.resolve_references(largetree, indexfile, self)
        # resolve :ref:s to distant tex files -- we can't add a cross-reference,
        # but append the document name
        for pendingnode in largetree.traverse(addnodes.pending_xref):
            docname = pendingnode['refdocname']
            sectname = pendingnode['refsectname']
            newnodes = [nodes.emphasis(sectname, sectname)]
            for subdir, title in self.titles:
                if docname.startswith(subdir):
                    newnodes.append(nodes.Text(_(' (in '), _(' (in ')))
                    newnodes.append(nodes.emphasis(title, title))
                    newnodes.append(nodes.Text(')', ')'))
                    break
            else:
                pass
            pendingnode.replace_self(newnodes)
        return largetree

    def finish(self):
        # then, copy over theme-supplied static files
        if self.theme:
            self.info(bold('copying static files...'), nonl=1)
            ctx = {}
            themeentries = [path.join(themepath, 'static')
                            for themepath in self.theme.get_dirchain()[::-1]]
            for entry in themeentries:
                self.info(' ' + entry)
                copy_static_entry(entry, self.outdir,
                                  self, ctx)

        # copy image files
        if self.images:
            self.info(bold('copying images...'), nonl=1)
            for src, dest in iteritems(self.images):
                self.info(' '+src, nonl=1)
                copyfile(path.join(self.srcdir, src),
                         path.join(self.outdir, dest))
            self.info()

        # copy TeX support files from texinputs
        self.info(bold('copying TeX support files...'))
        staticdirname = path.join(package_dir, 'texinputs')
        for filename in os.listdir(staticdirname):
            if not filename.startswith('.'):
                copyfile(path.join(staticdirname, filename),
                         path.join(self.outdir, filename))

        # copy additional files
        if self.config.latex_additional_files:
            self.info(bold('copying additional files...'), nonl=1)
            for filename in self.config.latex_additional_files:
                self.info(' '+filename, nonl=1)
                copyfile(path.join(self.confdir, filename),
                         path.join(self.outdir, path.basename(filename)))
            self.info()

        # the logo is handled differently
        if self.config.latex_logo:
            logobase = path.basename(self.config.latex_logo)
            logotarget = path.join(self.outdir, logobase)
            if not path.isfile(path.join(self.confdir, self.config.latex_logo)):
                raise SphinxError('logo file %r does not exist' % self.config.latex_logo)
            elif not path.isfile(logotarget):
                copyfile(path.join(self.confdir, self.config.latex_logo), logotarget)
        self.info('done')

    def cleanup(self):
        # clean up theme stuff
        if self.theme:
            self.theme.cleanup()
