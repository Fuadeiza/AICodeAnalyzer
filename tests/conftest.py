# tests/conftest.py

import sys
from pathlib import Path
import pytest
from xvfbwrapper import Xvfb

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session", autouse=True)
def xvfb_server():
    vdisplay = Xvfb()
    vdisplay.start()
    yield
    vdisplay.stop()
