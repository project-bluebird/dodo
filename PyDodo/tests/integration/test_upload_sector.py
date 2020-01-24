import pytest
import os
import time

import pandas as pd

from pydodo import (
    reset_simulation,
    upload_sector
)
from pydodo.bluebird_connect import ping_bluebird
from pydodo.config_param import config_param

bb_resp = ping_bluebird()
bluesky_sim = config_param("simulator") == config_param("bluesky_simulator")


@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
# @pytest.mark.skipif(not bluesky_sim, reason="Not using BlueSky")
def test_upload_sector(rootdir):
    """
    Create scenario on the simulator host and load.
    Check two aircraft created succesfully with associated route.
    """
    test_sector = "dodo-test-sector"

    test_file = os.path.join(rootdir, test_sector)

    resp = reset_simulation()
    assert resp == True

    resp = upload_sector(filename="{}.geojson".format(test_file), sector_name=test_sector)
    assert resp == True
