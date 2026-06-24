import importlib

from . import colors
from . import decorators
from . import matrix
from . import misc
from . import io

from .misc import get_mypkg_path, num2str, str2num
from .io import load_yaml, load_pkl, save_pkl, load_pkl_folder2dict, save_pkl_dict2folder


from .version import __version__

__all__ = ['colors', 'decorators', 'matrix', 'misc', 'io', 'rpy2_utils', '__version__']


def __getattr__(name):
    if name == 'rpy2_utils':
        return importlib.import_module('.rpy2_utils', __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")