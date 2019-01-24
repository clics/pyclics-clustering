from shutil import copytree
from pathlib import Path

import pytest

from pyclics import Clics


@pytest.fixture
def graph(tmpdir):
    copytree(str(Path(__file__).parent / 'graphs'), str(tmpdir.join('graphs')))
    return Clics(str(tmpdir)).load_graph('network', 1, 'families')
