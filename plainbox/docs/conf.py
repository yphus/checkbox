#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Plainbox documentation build configuration file, created by
# sphinx-quickstart on Wed Feb 13 11:18:39 2013.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    import plainbox
except ImportError as exc:
    raise SystemExit("plainbox has to be importable")
else:
    modules_to_mock = [
        'lxml',
        'xlsxwriter',
        'xlsxwriter.workbook',
        'xlsxwriter.utility',
        'requests',
        'requests.exceptions'
    ]
    # Inject mock modules so that we can build the
    # documentation without having the real stuff available
    from plainbox.vendor import mock
    for mod_name in modules_to_mock:
        sys.modules[mod_name] = mock.Mock()

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.viewcode',
              'plainbox.vendor.sphinxarg.ext']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Plainbox'
copyright = '2012-2014 Canonical Ltd'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "{0[0]}.{0[1]}".format(plainbox.__version__)
# The full version, including alpha/beta/rc tags.
release = "{0[0]}.{0[1]}.{0[2]}.{0[3]}.{0[4]}".format(plainbox.__version__)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# Use our custom theme. For now it only adds Disqus.com support but we may
# customize it further later on. The theme is called 'plainbox' and has one
# option which controls if disqus is active or not.
html_theme = 'plainbox'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# Due to the way disqus works, it's only going to work on
# plainbox.readthedocs.org so only use it if building for readthedocs.

html_theme_options = {
    'show_disqus': 'true' if os.environ.get("READTHEDOCS", None) == 'True' else ''
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['_theme']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Plainboxdoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Plainbox.tex', 'Plainbox Documentation',
   'Zygmunt Krynicki', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
_authors = ['Zygmunt Krynicki & Checkbox Contributors']
man_pages = [
    # Section 1
    ('manpages/plainbox', 'plainbox',
     'toolkit for software and hardware integration testing',
     _authors, 1),
    ('manpages/plainbox-trusted-launcher-1', 'plainbox-trusted-launcher-1',
     'execute job command as another user', _authors, 1),
    ('manpages/plainbox-run', 'plainbox-run',
     'run a test job', _authors, 1),
    ('manpages/plainbox-check-config', 'plainbox-check-config',
     'check and display plainbox configuration', _authors, 1),
    ('manpages/plainbox-startprovider', 'plainbox-startprovider',
     'create a new plainbox provider', _authors, 1),
    ('manpages/plainbox-self-test', 'plainbox-self-test',
     'run unit and integration tests', _authors, 1),
    ('manpages/plainbox-manage.py', 'manage.py',
     'plainbox provider management script', _authors, 1),
    ('manpages/plainbox-session', 'plainbox-session',
     'session management sub-commands', _authors, 1),
    ('manpages/plainbox-session-list', 'plainbox-session-list',
     'list available session', _authors, 1),
    ('manpages/plainbox-session-remove', 'plainbox-session-remove',
     'remove one ore more sessions', _authors, 1),
    ('manpages/plainbox-session-show', 'plainbox-session-show',
     'show a single session', _authors, 1),
    ('manpages/plainbox-session-archive', 'plainbox-session-archive',
     'archive a single session', _authors, 1),
    ('manpages/plainbox-dev', 'plainbox-dev',
     'commands for test developers', _authors, 1),
    ('manpages/plainbox-dev-script', 'plainbox-dev-script',
     'run a command from a job', _authors, 1),
    ('manpages/plainbox-dev-special', 'plainbox-dev-special',
     'special/internal commands', _authors, 1),
    ('manpages/plainbox-dev-analyze', 'plainbox-dev-analyze',
     'analyze how seleted jobs would be executed', _authors, 1),
    ('manpages/plainbox-dev-parse', 'plainbox-dev-parse',
     'parse stdin with the specified parser', _authors, 1),
    ('manpages/plainbox-dev-crash', 'plainbox-dev-crash',
     'crash the application', _authors, 1),
    ('manpages/plainbox-dev-logtest', 'plainbox-dev-logtest',
     'log messages at various levels', _authors, 1),
    ('manpages/plainbox-dev-list', 'plainbox-dev-list',
     'list and describe various objects', _authors, 1),
    # Section 5
    ('manpages/plainbox.conf', 'plainbox.conf',
     'plainbox configuration file', _authors, 5),
    # Section 7
    ('manpages/plainbox-session-structure', 'plainbox-session-structure',
     'structure of per-session directory', _authors, 7),
    ('manpages/plainbox-template-units', 'plainbox-template-units',
     'syntax and semantics of Plainbox template unit type', _authors, 7),
    ('manpages/plainbox-category-units', 'plainbox-category-units',
     'syntax and semantics of Plainbox category unit type', _authors, 7),
    ('manpages/plainbox-file-units', 'plainbox-file-units',
     'syntax and semantics of Plainbox file unit type', _authors, 7),
    ('manpages/PLAINBOX_SESSION_SHARE', 'PLAINBOX_SESSION_SHARE',
     'per-session runtime shared-state directory', _authors, 7),
    ('manpages/PLAINBOX_PROVIDER_DATA', 'PLAINBOX_PROVIDER_DATA',
     'per-provider data directory', _authors, 7),
    ('manpages/CHECKBOX_DATA', 'CHECKBOX_DATA',
     'legacy name for PLAINBOX_SESSION_SHARE', _authors, 7),
    ('manpages/CHECKBOX_SHARE', 'CHECKBOX_SHARE',
     'legacy name for PLAINBOX_PROVIDER_DATA', _authors, 7),
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Plainbox', 'Plainbox Documentation',
   'Zygmunt Krynicki', 'Plainbox', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'
