# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys


import datetime
import cebra


def get_years(start_year=2021):
    year = datetime.datetime.now().year
    if year > start_year:
    else:


# -- Project information -----------------------------------------------------
# The full version, including alpha/beta/rc tags
release = cebra.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "IPython.sphinxext.ipython_console_highlighting",
    # "sphinx_panels", # Note: package to avoid: no longer maintained.
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinx.ext.doctest",
    "sphinx_gallery.load_style",
]

coverage_show_missing_items = True
panels_add_bootstrap_css = False

# NOTE(stes): All configuration options for the napoleon package
#   The package is used to configure rendering of Google-style
#   docstrings used throughout the CEBRA package.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
# napoleon_include_init_with_doc = False
# napoleon_include_private_with_doc = True
# napoleon_include_special_with_doc = True
# napoleon_use_admonition_for_examples = True
# napoleon_use_admonition_for_notes = True
# napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
# napoleon_use_keyword = True
napoleon_use_param = True
# napoleon_use_rtype = True
# napoleon_preprocess_types = False
# napoleon_type_aliases = None
napoleon_attr_annotations = True

intersphinx_mapping = {
    "sklearn": ("https://scikit-learn.org/stable", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/dev", None),
    "scipy": ("http://docs.scipy.org/doc/scipy/reference/", None),
    "joblib": ("https://joblib.readthedocs.io/en/latest/", None),
}

# Config is documented here: https://sphinx-copybutton.readthedocs.io/en/latest/
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

autodoc_mock_imports = [
    "torch",
    "nlb_tools",
    "tqdm",
    "h5py",
    "pandas",
    "matplotlib",
]

# Add any paths that contain templates here, relative to this directory.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "demo_notebooks/README.rst"
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "pydata_sphinx_theme"

# More info on theme options:
# https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/configuring.html
html_theme_options = {
            "url": "https://github.com/AdaptiveMotorControlLab/CEBRA",
        # {
        #     "name": "DockerHub",
        #     "url": "https://hub.docker.com/r/stffsc/cebra",
        #     "icon": "fab fa-docker",
        # },
            "url": "https://api.semanticscholar.org/CorpusID:247939478",
    "external_links": [
    ],
    "collapse_navigation": False,
    "navigation_depth": 4,
    "show_nav_level": 2,
    "navbar_align": "content",
}

html_context = {"default_mode": "dark"}
html_favicon = "_static/img/logo_small.png"
html_logo = "_static/img/logo_large.png"

# Remove the search field for now
html_sidebars = {
}

# Disable links for embedded images
html_scaled_image_link = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_css_files = ["css/custom.css"]

# See discussion here: https://github.com/sphinx-doc/sphinx/issues/6895#issuecomment-570759798
# Right now, only python module types are problematic, in cebra.registry
nitpick_ignore = [
    ("py:class", "module"),
]

nbsphinx_thumbnails = {
    "demo_notebooks/Demo_primate_reaching":
        "_static/thumbnails/ForelimbS1.png",
    "demo_notebooks/Demo_hippocampus":
        "_static/thumbnails/encodingSpace.png",
    "demo_notebooks/Demo_Allen":
        "_static/thumbnails/DecodingVideos.png",
    "demo_notebooks/Demo_conv-pivae":
        "_static/thumbnails/TechconvpiVAE.png",
    "demo_notebooks/Demo_hippocampus_multisession":
        "_static/thumbnails/TechMultiSession.png",
    "demo_notebooks/Demo_learnable_temperature":
        "_static/thumbnails/TechLearningTemp.png",
    "demo_notebooks/Demo_primate_reaching_mse_loss":
        "_static/thumbnails/TechMSE.png",
    "demo_notebooks/Demo_synthetic_exp":
        "_static/thumbnails/SyntheticBenchmark.png",
    "demo_notebooks/Demo_consistency":
        "_static/thumbnails/consistency.png",
    "demo_notebooks/Demo_decoding":
        "_static/thumbnails/decoding.png",
    "demo_notebooks/Demo_hypothesis_testing":
        "_static/thumbnails/hypothesis.png",
    "demo_notebooks/Demo_cohomology":
        "_static/thumbnails/cohomology.png",
}

rst_prolog = r"""

.. |Default:| raw:: html

    <div class="default-value-section"> <span class="default-value-label">Default:</span>

"""


# Download link for the notebook, see
# https://nbsphinx.readthedocs.io/en/0.3.0/prolog-and-epilog.html
nbsphinx_prolog = r"""

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        {% if 'demo_notebooks' in env.docname %}
        You can download and run the notebook locally or run it with Google Colaboratory:

        :raw-html:`<a href="/docs/{{ env.docname }}.ipynb"><img alt="Download jupyter notebook" src="https://img.shields.io/badge/download-jupyter%20notebook-bf1bb9" style="vertical-align:text-bottom"></a>`
        :raw-html:`<a href="https://colab.research.google.com/github/AdaptiveMotorControlLab/CEBRA-demos/blob/main/{{ env.doc2path(env.docname, base=None)|basename }}"><img alt="Run on Colab" src="https://colab.research.google.com/assets/colab-badge.svg" style="vertical-align:text-bottom"></a>`
        {% else %}
        You can download and run the notebook locally:

        :raw-html:`<a href="/docs/{{ env.docname }}.ipynb"><img alt="Download jupyter notebook" src="https://img.shields.io/badge/download-jupyter%20notebook-bf1bb9" style="vertical-align:text-bottom"></a>`
        {% endif %}

----
"""
