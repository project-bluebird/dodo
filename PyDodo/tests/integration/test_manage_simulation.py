"""
Test load_scenario and reset_simulation functions
- return True if successful
- raise error if invalid input provided
"""

import pytest
from pydodo import reset_simulation, load_scenario, pause_simulation, resume_simulation
from pydodo.utils import ping_bluebird

from requests.exceptions import HTTPError

bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_simulation():
    """
    - Load scenario - check returns True if valid file path is provided (BlueSky)
    - Pause
    - Resume
    - Reset
    """
    resp = load_scenario("scenario/8.scn")
    assert resp == True

    resp = pause_simulation()
    assert resp == True

    resp = resume_simulation()
    assert resp == True

    resp = reset_simulation()
    assert resp == True

def test_load_empty():
    """
    Check fails if no scenario file is provided
    """
    with pytest.raises(AssertionError):
        resp = load_scenario("")

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_load_invalid_file():
    """
    Check exception is raised if invalid file path is provided
    """
    with pytest.raises(HTTPError):
         resp = load_scenario("hello")
