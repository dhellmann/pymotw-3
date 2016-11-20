from pearson import builder

from sphinx.ext import graphviz


def setup(app):
    app.info('initializing Pearson extension')
    app.add_builder(builder.PearsonLaTeXBuilder)
    # Tell the application which translator to use, which lets other
    # extensions register new nodes to work with that translator.
    app.set_translator('pearson', writer.PearsonLaTeXTranslator)
    # Tell the application to use the graphviz visitor for this
    # builder, too.
    app.add_node(
        graphviz.graphviz,
        pearson=(graphviz.latex_visit_graphviz, None),
    )
