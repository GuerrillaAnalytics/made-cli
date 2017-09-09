from made.commands.inputs_grp.inputs_functions import input_build_name
import pytest


def test_input_build_name():
    """Test that created path ends in 'data' folder"""

    test_path = input_build_name(source_id="23", source_name="my_label", version=3)
    expected_path = "23_my_label/003/raw/data"

    assert expected_path == test_path


def test_input_build_name_Value_Exception():
    with pytest.raises(ValueError) as excinfo:
        input_build_name(source_id="23", source_name="my_label", version=3, raw_or_formatted="fail")

    assert str(excinfo.value) == "raw_or_formatted: must have value 'raw' or 'formatted'"