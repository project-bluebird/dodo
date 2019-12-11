import pytest
import os

from pydodo import episode_log
from pydodo.bluebird_connect import ping_bluebird

bb_resp = ping_bluebird()


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_eplog():
    filepath = episode_log()
    assert isinstance(filepath, str)

    assert os.path.exists(filepath)
