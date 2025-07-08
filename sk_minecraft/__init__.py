""" sk_minecraft package """
from pathlib import Path

from sk_minecraft.kern import verbinden
from sk_minecraft.main import *

_blocks_file = Path(__file__).parent/"block.py"

if not _blocks_file.exists():

    import importlib
    import sys

    from sk_minecraft._generate_blocks import _make_block_file
    _make_block_file(_blocks_file)

    spec = importlib.util.spec_from_file_location("block", _blocks_file)
    generated_module = importlib.util.module_from_spec(spec)
    sys.modules[_blocks_file] = generated_module
    spec.loader.exec_module(generated_module)

from sk_minecraft.block import *
