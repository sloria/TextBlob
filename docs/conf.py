# -*- coding: utf-8 -*-
import datetime as dt
import importlib.metadata

import os
import sys

sys.path.append(os.path.abspath("_themes"))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx_issues",
]

primary_domain = "py"
default_role = "py:obj"

issues_github_path = "sloria/TextBlob"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "TextBlob"
copyright = '<a href="http://stevenloria.com/">Steven Loria</a> and contributors'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = release = importlib.metadata.version("textblob")
exclude_patterns = ["_build"]
pygments_style = "flask_theme_support.FlaskyStyle"
html_theme = "kr"
html_theme_path = ["_themes"]

html_static_path = ["_static"]

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    "index": ["side-primary.html", "searchbox.html"],
    "**": ["side-secondary.html", "localtoc.html", "relations.html", "searchbox.html"],
}
# Output file base name for HTML help builder.
htmlhelp_basename = "textblobdoc"


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ("index", "TextBlob.tex", "textblob Documentation", "Steven Loria", "manual"),
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "textblob", "textblob Documentation", ["Steven Loria"], 1)]
# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "textblob",
        "TextBlob Documentation",
        "Steven Loria",
        "textblob",
        "Simplified Python text-processing.",
        "Natural Language Processing",
    ),
]
