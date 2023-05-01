"""CEBRA is a library for estimating Consistent Embeddings of high-dimensional Recordings 
using Auxiliary variables. It contains self-supervised learning algorithms implemented in
PyTorch, and has support for a variety of different datasets common in biology and neuroscience.
"""

is_sklearn_available = False
try:
    # TODO(stes): More common integrations people care about (e.g. PyTorch lightning)
    # could be added here.
    from cebra.integrations.sklearn.cebra import CEBRA
    from cebra.integrations.sklearn.decoder import KNNDecoder
    from cebra.integrations.sklearn.decoder import L1LinearRegressor
    is_sklearn_available = True
except ImportError as e:
    # silently fail for now
    pass

is_matplotlib_available = False
try:
    from cebra.integrations.matplotlib import *

    is_matplotlib_available = True
except ImportError as e:
    # silently fail for now
    pass

from cebra.data.load import load as load_data
from cebra.integrations.deeplabcut import load_deeplabcut
import cebra.integrations.sklearn as sklearn

__version__ = "0.1.0"
__all__ = ["CEBRA"]
__allow_lazy_imports = False
__lazy_imports = {}


def allow_lazy_imports():
    """Enables lazy imports of all submodules and packages of cebra.

    If called, references to ``cebra.<module_name>`` will be automatically
    lazily imported when first called in the code, and not raise a warning.
    """
    __allow_lazy_imports = True


def __getattr__(key):
    """Lazy import of cebra submodules and -packages.


    """
    if key == "CEBRA":
        from cebra.integrations.sklearn.cebra import CEBRA
        return CEBRA
    elif key == "KNNDecoder":
        from cebra.integrations.sklearn.decoder import KNNDecoder

        return KNNDecoder
    elif key == "L1LinearRegressor":
        from cebra.integrations.sklearn.decoder import L1LinearRegressor

        return L1LinearRegressor
    elif not key.startswith("_"):
        import importlib
        import warnings
        if key not in __lazy_imports:
            # NOTE(celia): condition needed when testing the string examples
            # so that the function doesn't try to import the testing packages
            # (pytest plugins, SetUpModule and TearDownModule) as cebra.{key}.
            # We just make sure that pytest is installed.
            if any(name in key.lower()
                   for name in ["pytest", "setup", "module"]):
                import pytest

                return importlib.import_module(pytest)
            if not __allow_lazy_imports:
                warnings.warn(
                    f"Your code triggered a lazy import of {__name__}.{key}. "
                    f"While this will (likely) work, it is recommended to "
                    f"add an explicit import statement to you code instead. "
                    f"To disable this warning, you can run "
                    f"``cebra.allow_lazy_imports()``.")
        return __lazy_imports[key]
    raise AttributeError(f"module 'cebra' has no attribute '{key}'. "
                         f"Did you import cebra.{key}?")
