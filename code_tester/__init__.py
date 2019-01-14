__version__ = '0.0.7'
__mod_name__ = 'code_tester'


"""
so that we can include things like
from code_tester import rand

"""
from .genlib.srb_random import *
from .genlib.srbIo import *

from .lib.comp_files import comp_files
