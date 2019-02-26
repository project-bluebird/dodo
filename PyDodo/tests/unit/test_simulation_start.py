"""
Test load_scenario and reset_simulation functions
"""


import pytest
from pydodo.reset_simulation import reset_simulation
from pydodo.load_scenario import load_scenario
from pydodo.utils import ping_bluebird

from requests.exceptions import HTTPError

bb_resp = ping_bluebird()

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_reset_simulation():
    """
    Check returns True
    """
    resp = reset_simulation()
    assert resp == True

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_load_scenario():
    """
    Check returns True if valid file path is provided
    """
    resp = load_scenario("scenario/8.scn")
    assert resp == True

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_load_scenario():
    """
    Check fails if no scenario file is provided
    """
    with pytest.raises(AssertionError):
        resp = load_scenario("")

@pytest.mark.skipif(not bb_resp, reason="Can't connect to bluebird")
def test_load_scenario():
    """
    Check exception is raised if invalid file path is provided
    """
    with pytest.raises(HTTPError):
         resp = load_scenario("hello")
