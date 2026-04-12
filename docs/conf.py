# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from collections.abc import Callable
from sphinx.util import inspect
import types
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeIs

# -- Project information -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "modCAM Python bindings"
author = ""
copyright = "contributors to the modCAM project"
version = release = "latest"

# -- General configuration -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "modcam-docs": ("https://modcam-docs.readthedocs.io/", None),
    "modcam-cpp": ("https://modcam-docs.readthedocs.io/projects/modcam-cpp/", None),
}
intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/modCAM/modcam-python",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/modCAM/modcam-python",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/modcam/",
            "icon": "https://img.shields.io/pypi/dw/modcam",
            "type": "url",
        },
    ],
}

# -- Napoleon configuration ----------------------------------------------------

# Enforce NumPy style
napoleon_google_docstring = False


# Sphinx on its own does not detect nanobind functions. See
# - https://github.com/sphinx-doc/sphinx/issues/13868
# - https://github.com/wjakob/nanobind/discussions/1147
# We have to modify its function inspection logic ourselves.
def wrap_sphinx_inspect(
    sphinx_inspect: Callable[[Any], TypeIs[types.FunctionType]],
) -> Callable[[Any], TypeIs[types.FunctionType]]:
    def sphinx_inspect_wrapper(obj: Any) -> TypeIs[types.FunctionType]:
        if obj.__repr__().startswith("<nanobind.nb_func"):
            return True
        return sphinx_inspect(obj)

    return sphinx_inspect_wrapper


inspect.isfunction = wrap_sphinx_inspect(inspect.isfunction)
