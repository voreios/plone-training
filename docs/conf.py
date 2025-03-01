# Configuration file for the Sphinx documentation builder.
# Mastering Plone documentation build configuration file


# -- Path setup --------------------------------------------------------------

from datetime import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "Plone Training"
copyright = """The text and illustrations in this website are licensed
 by the Plone Foundation under a Creative Commons Attribution 4.0
 International license."""
author = "Plone Community"
trademark_name = "Plone"

now = datetime.now()
year = str(now.year)
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = year
# The full version, including alpha/beta/rc tags.
release = year

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ""
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = "%B %d, %Y"


# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*")
# or your custom ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxcontrib.spelling",
    "sphinxext.opengraph",
]

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # You will be able to utilise definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "linkify",  # Identify “bare” web URLs and add hyperlinks.
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
]

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx.pygments_styles.PyramidStyle"
pygments_style = "sphinx"

# Options for the linkcheck builder
# Ignore localhost
linkcheck_ignore = [
    r"http://localhost",
    r"http://127.0.0.1",
    r"http://example.com",
    r"https://github.com/plone/training/issues/new/choose",  # requires auth
    r"https://www.linode.com",  # linkcheck makes a HEAD request, which is 403
    r"https://www.virtualbox.org",  # times out often
    r"https://docs.github.com/en/get-started/.*",  # GitHub docs require auth
    r"https://github.com/plone/mockup/blob/master/mockup/.jshintrc",  # TODO: remove when javascript/development-process.md is updated. See https://github.com/plone/training/issues/611
    r"https://www.chef.io/products/chef-infra/",  # Site works but creates SSLError
    r"https://plonedemo.kitconcept.com",  # Did Not Connect: Potential Security Issue
    r"https://www.packtpub.com/.*",  # test say 500 Server Error but manually they work
    r"https://www.dipf.de/.*",  # a timeout from time to time
    r"https?://plone-conference.localhost.*",
    # Example domain
    "https://domain-a.com/data.json",
    "https://domain-b.com/data.json",
    # ### Start of list of anchored links
    # Prior to each PloneConf, uncomment these lines to verify that the links work,
    # although the anchor cannot be found.
    # GitHub rewrites anchors with JavaScript.
    # See https://github.com/plone/training/issues/598#issuecomment-1105168109
    "https://github.com/collective/awesome-volto#addons",
    "https://github.com/collective/collective.easyform#collectivez3cformnorobots-support",
    "https://github.com/collective/collective.easyform#recaptcha-support",
    "https://github.com/collective/collective.recipe.solrinstance/blob/master/README.rst#multi-core-solr",
    "https://github.com/nvm-sh/nvm#install-script",
    "https://github.com/plone/plone.app.contentlisting/#methods-of-contentlistingobjects",
    "https://github.com/plone/plone.app.contenttypes#changing-the-base-class-for-existing-objects",
    "https://github.com/plone/plone.recipe.zope2instance#advanced-logging-options-for-wsgi",
    "https://github.com/repoze/repoze.catalog/blob/master/docs/usage.rst#query-objects",
    "https://plone.github.io/mockup/dev/#pattern/autotoc",
    "https://plone.github.io/mockup/dev/#pattern/modal",
    "https://plone.github.io/mockup/dev/#pattern/moment",
    "https://github.com/collective/collective.exportimport#faq-tips-and-tricks",
    "https://github.com/plone/plone.app.contenttypes/tree/2.2.x#migration",
    "https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Keywords",
    "https://solr.apache.org/guide/8_2/updatehandlers-in-solrconfig.html#UpdateHandlersinSolrConfig-commitWithin",
    "https://www.npmjs.com/package/axios#example",
    "https://github.com/plone/plone.restapi/blob/afde2a940d2518e061eb3fe30093093af55e3a50/src/plone/restapi/services/content/configure.zcml#L15-L20",
    "https://github.com/plone/plone.rest#cors",
    "https://github.com/plone/plone.docker#for-basic-usage",
    "https://github.com/nodejs/release#release-schedule",
    # ### End of list of anchored links
]
linkcheck_allowed_redirects = {
    # All HTTP redirections from the source URI to the canonical URI will be treated as "working".
    r"https://chrome\.google\.com/webstore/detail/.*": r"https://consent\.google\.com/.*",
}
linkcheck_anchors = True
linkcheck_timeout = 10
linkcheck_retries = 2

# This is our wordlist with known words, like Github or Plone ...
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_ignore_pypi_package_names = True

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
}

# The encoding of source files.
# source_encoding = "utf-8-sig"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "spelling_wordlist.txt",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"

html_css_files = ["custom.css", ("print.css", {"media": "print"})]
html_js_files = [
    "patch_scrollToActive.js",
]

html_extra_path = [
    "robots.txt",
]

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://training.plone.org/5"
sitemap_url_scheme = "{link}"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "repository_url": "https://github.com/plone/training",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "extra_navbar": f"""
        <p class="ploneorglink">
            <a href="https://plone.org">
                <img src="{html_baseurl}/_static/logo.svg" alt="plone.org" /> plone.org</a>
        </p>""",
}


# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
intersphinx_mapping = {
    "plonedocs": ("https://docs.plone.org/", None),
    "plone6docs": ("https://6.dev-docs.plone.org/", None),
    "python": ("https://docs.python.org/3/", None),
}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://training.plone.org/5/"
ogp_description_length = 200
ogp_image = "https://training.plone.org/5/_static/Plone_logo_square.png"
ogp_site_name = "Plone Training"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]

# -- sphinx_copybutton -----------------------
copybutton_prompt_text = r"^ {0,2}\d{1,3}"
copybutton_prompt_is_regexp = True


# -- sphinx.ext.todo -----------------------
todo_include_todos = True  # Uncomment to show todos.


# An extension that allows replacements for code blocks that
# are not supported in `rst_epilog` or other substitutions.
# https://stackoverflow.com/a/56328457/2214933
def source_replace(app, docname, source):
    result = source[0]
    for key in app.config.source_replacements:
        result = result.replace(key, app.config.source_replacements[key])
    source[0] = result


# Dict of replacements.
source_replacements = {
    "{PLONE_BACKEND_VERSION}": "6.0.0b3",
}


def setup(app):
    app.add_config_value("source_replacements", {}, True)
    app.connect("source-read", source_replace)
