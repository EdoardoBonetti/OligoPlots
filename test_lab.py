# test_demo.py
import pytest
from lab import Measurment, DSC


def test_abstract_base_class():
    with pytest.raises(TypeError):
        Measurment()


def test_implementation():
    implemented_instance = DSC(
        "DSC/RBXRSO/cooling/2perc/231116_RBX_RSO_2perc_B_2st_cooling_raw_data.txt")
    assert isinstance(implemented_instance, Measurment)
    # assert implemented_instance.process() == "PYTHONIC musings"
