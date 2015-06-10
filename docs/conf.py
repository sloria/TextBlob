# -*- coding: utf-8 -*-
import datetime as dt
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
import textblob
sys.path.append(os.path.abspath("_themes"))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx_issues',
]

primary_domain = 'py'
default_role = 'py:obj'

issues_github_path = 'sloria/TextBlob'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'TextBlob'
copyright = u'{0:%Y} <a href="http://stevenloria.com/">Steven Loria</a>'.format(
    dt.datetime.utcnow()
)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = release = textblob.__version__
exclude_patterns = ['_build']
pygments_style = 'flask_theme_support.FlaskyStyle'
html_theme = 'kr'
html_theme_path = ['_themes']

html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    'index':    ['side-primary.html', 'searchbox.html'],
    '**':       ['side-secondary.html', 'localtoc.html',
                 'relations.html', 'searchbox.html']
}
# Output file base name for HTML help builder.
htmlhelp_basename = 'textblobdoc'


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', 'TextBlob.tex', u'textblob Documentation',
    u'Steven Loria', 'manual'),
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'textblob', u'textblob Documentation',
     [u'Steven Loria'], 1)
]
# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'textblob', u'TextBlob Documentation',
   u'Steven Loria', 'textblob', 'Simplified Python text-processing.',
   'Natural Language Processing'),
]
