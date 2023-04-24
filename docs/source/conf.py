import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'callingcards.config')
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'callingcards'
copyright = '2023, Chase Mateusiak'
author = 'Chase Mateusiak'
release = '2023-04-17'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
