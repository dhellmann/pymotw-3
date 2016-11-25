from pearson import builder

from sphinx.ext import graphviz


def setup(app):
    app.info('initializing Pearson extension')

    # Define a list option with the names of the files making up the
    # chapters.
    app.add_config_value('pearson_chapters', [], 'env')
    app.add_config_value('pearson_title', 'The Book', 'env')
    app.add_config_value('pearson_subtitle', '', 'env')
    app.add_config_value('pearson_theme_path', [], 'env')
    app.add_config_value('pearson_theme', 'generic', 'env')
    app.add_config_value('pearson_theme_options', {}, 'env')
    app.add_config_value('pearson_author', '', 'env')
    app.add_config_value('pearson_output_base', 'book', 'env')
    app.add_config_value('pearson_pdflatex', 'xelatex', 'env')

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
