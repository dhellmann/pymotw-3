# -*- coding: utf-8 -*-
"""LaTeX builder using Pearson style templates.
"""

import copy
import os
from os import path
import textwrap
import warnings

from six import iteritems, itervalues, text_type
from docutils import nodes
from docutils.io import FileOutput
from docutils.utils import new_document
from docutils.frontend import OptionParser

from sphinx import highlighting
from sphinx import package_dir, addnodes
from sphinx.builders import Builder
from sphinx.environment import NoUri
from sphinx.errors import SphinxError
from sphinx.locale import _
from sphinx.theming import Theme
from sphinx.util import copy_static_entry
from sphinx.util import texescape
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import SEP, copyfile

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
        # NOTE: Assume that we always have access to all documents,
        # and return a value target.
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

    def write(self, *ignored):
        docwriter = writer.PearsonLaTeXWriter(self)
        docsettings = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,),
            read_config_files=True).get_default_values()

        self.init_chapters()
        self.processed_docs = {}

        # Build the template context before rendering the
        # non-templated files so we can include those file names in a
        # context parameter.
        global_context = self.theme.get_options(self.config.pearson_theme_options)
        global_context.update({
            'chapter_names': [],
            'appendices': [],
            'indices': [],
        })

        # HACK:
        # Compute the full document and use it to process
        # cross-references, which we then save to use when processing
        # individual chapters.
        toctrees = self.env.get_doctree(global_context['input_base']).traverse(addnodes.toctree)
        if toctrees:
            if toctrees[0].get('maxdepth') > 0:
                tocdepth = toctrees[0].get('maxdepth')
            else:
                tocdepth = None
        else:
            tocdepth = None
        doctree = self.assemble_doctree(
            global_context['input_base'],
            True,  # toctree_only
            appendices=self.config.latex_appendices,
        )
        std_domain_data = copy.deepcopy(self.env.domains['std'].data)

        def process_doc(name_fmt, num, docname, doctype):
            name = name_fmt.format(num)
            destination = FileOutput(
                destination_path=path.join(self.outdir, name + '.tex'),
                encoding='utf-8')
            self.info('writing {} to {}.tex ... '.format(docname, name), nonl=1)
            toctrees = self.env.get_doctree(docname).traverse(addnodes.toctree)
            if toctrees:
                if toctrees[0].get('maxdepth') > 0:
                    tocdepth = toctrees[0].get('maxdepth')
                else:
                    tocdepth = None
            else:
                tocdepth = None
            # HACK:
            # Stuff the full domain data back into the domain so the
            # xref data is present.
            self.env.domains['std'].data = copy.deepcopy(std_domain_data)
            doctree = self.assemble_doctree(
                docname,
                False,  # toctree_only
                appendices=[],
            )
            doctree['tocdepth'] = tocdepth
            self.post_process_images(doctree)
            doctree.settings = docsettings
            # doctree.settings.author = author
            # doctree.settings.title = title
            doctree.settings.contentsname = self.get_contentsname(docname)
            doctree.settings.docname = docname
            doctree.settings.doctype = doctype
            # doctree.settings.docclass = docclass
            self.processed_docs[docname] = doctree
            docwriter.write(doctree, destination)
            self.info("done")
            return name

        # First generate the chapters
        chap_name_fmt = 'chap{:02d}'
        if len(self.document_data) >= 100:
            chap_name_fmt = 'chap{:03d}'

        for chap_num, docname in enumerate(self.document_data, 1):
            name = process_doc(chap_name_fmt, chap_num, docname, 'chapter')
            global_context['chapter_names'].append(name)

        # Then any appendices
        app_name_fmt = 'app{:02d}'
        if len(self.config.latex_appendices) >= 100:
            app_name_fmt = 'app{:03d}'

        for app_num, docname in enumerate(self.config.latex_appendices, 1):
            name = process_doc(app_name_fmt, app_num, docname, 'startappendix')
            global_context['appendices'].append(name)

        # Then any index files
        indices = self.generate_indices(list(sorted(self.env.all_docs.keys())))
        for name, body in indices:
            global_context['indices'].append(name)
            file_name = path.join(self.outdir, name + '.tex')
            self.info('writing {}'.format(file_name))
            output = FileOutput(
                destination_path=file_name,
                encoding='utf-8',
            )
            output.write(body)

        # Finally the templates pages
        global_context['external_docs'] = (
            global_context['chapter_names'] +
            global_context['appendices']
        )

        templated_pages = [
            ('half-title.tex', 'half-title.tex'),
            ('title.tex', 'title.tex'),
            ('book.tex', global_context['output_base'] + '.tex'),
            ('CIP.tex', 'CIP.tex'),
            ('Makefile', 'Makefile'),
        ]

        for template_name, outname in templated_pages:
            file_name = path.join(self.outdir, outname)
            self.info('writing {}'.format(file_name))
            output = FileOutput(
                destination_path=file_name,
                encoding='utf-8',
            )
            try:
                body = self.templates.render(template_name, global_context)
            except Exception as err:
                self.info(bold('Failed to render template {}: {} at {}'.format(
                    template_name, err, err.lineno))
                )
                raise
            output.write(body)

    index_commands = {
        'py-modindex': 'moduleindex',
    }

    def generate_indices(self, docnames):
        docwriter = writer.PearsonLaTeXWriter(self)
        # To construct a translator we need a processed document, so
        # just pick the first one we've procssed.
        random_doc = self.processed_docs[self.config.pearson_chapters[0]]
        translator = writer.PearsonLaTeXTranslator(random_doc, self)

        def generate(indexname, content, collapsed):
            ret = []
            index_command = self.index_commands.get(indexname, 'theindex')
            ret.append('\\begin{%s}\n' % index_command)
            ret.append('\\footnotesize\n')

            for i, (letter, entries) in enumerate(content):
                if i > 0:
                    ret.append('\n  \\indexspace\n')
                ret.append('{\\sffamily\\bfseries{%s}}\\nopagebreak\n\n' % 
                           text_type(letter).translate(texescape.tex_escape_map))
                for entry in entries:
                    if not entry[3]:
                        continue
                    ret.append('  \\item {\\texttt{%s}}' % translator.encode(entry[0]))
                    if entry[4]:
                        # add "extra" info
                        ret.append(' \\emph{(%s)}' % translator.encode(entry[4]))
                    ret.append(', \\pageref{%s:%s}\n' %
                               (entry[2], translator.idescape(entry[3])))
            ret.append('\\end{%s}\n' % index_command)
            return ret

        indices = []

        # latex_domain_indices can be False/True or a list of index names
        indices_config = self.config.latex_domain_indices
        if indices_config:
            for domain in itervalues(self.env.domains):
                for indexcls in domain.indices:
                    indexname = '%s-%s' % (domain.name, indexcls.name)
                    if isinstance(indices_config, list):
                        if indexname not in indices_config:
                            continue
                    # deprecated config value
                    if indexname == 'py-modindex' and \
                       not self.config.latex_use_modindex:
                        continue
                    content, collapsed = indexcls(domain).generate(docnames)
                    if not content:
                        continue
                    results = generate(indexname, content, collapsed)
                    indices.append((indexname, ''.join(results)))

        return indices

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
        # copy image files
        if self.images:
            self.info(bold('copying images...'), nonl=1)
            for src, dest in iteritems(self.images):
                self.info(' '+src, nonl=1)
                copyfile(path.join(self.srcdir, src),
                         path.join(self.outdir, dest))
            self.info()

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

        # finally, copy over theme-supplied static files, some of which
        # might override the files copied earlier
        if self.theme:
            self.info(bold('copying static files...'), nonl=1)
            ctx = {}
            themeentries = [path.join(themepath, 'static')
                            for themepath in self.theme.get_dirchain()[::-1]]
            for entry in themeentries:
                self.info(' ' + entry)
                copy_static_entry(entry, self.outdir,
                                  self, ctx)

        self.info('done')

    def cleanup(self):
        # clean up theme stuff
        if self.theme:
            self.theme.cleanup()
