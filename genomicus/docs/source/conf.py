# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# AJOUT 
import os
import sys
import django
sys.path.insert(0, os.path.abspath('../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'genomicus.settings'
django.setup()

project = 'Genomicus'
copyright = '2023, Ambre Baumann - Lindsay Goulet - George Marchment - Clémence Sebe'
author = 'Ambre Baumann - Lindsay Goulet - George Marchment - Clémence Sebe'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://sphinx-themes.org/

#html_theme = 'alabaster'
#html_theme ='nature'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
