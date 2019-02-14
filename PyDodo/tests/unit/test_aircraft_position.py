
import pytest
from pydodo.aircraft_position import aircraft_position
from pydodo.utils import ping_bluebird

@pytest.mark.parametrize(
    "aircraft_id",
    [123, "", [], [""], [["TEST1"]], ["TEST1", 123]]
    )
def test_aircraft_id(aircraft_id):
    """
    Check incorrectly formatted aircraft_id raises error
    """
    with pytest.raises(AssertionError):
        aircraft_position(aircraft_id)
