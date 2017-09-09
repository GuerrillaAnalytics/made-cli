import os
import shutil
import tempfile
import errno
import pytest

from made.commands.inputs_grp.inputs_functions import input_audit_path
from made.commands.inputs_grp.inputs_functions import input_build_name


def test_input_build_name():
    """Test that created path ends in 'data' folder"""

    test_path = input_build_name(source_id="23", source_name="my_label", version=3)
    expected_path = "23_my_label/003/raw/data"

    assert expected_path == test_path


def test_input_build_name_Value_Exception():
    with pytest.raises(ValueError) as excinfo:
        input_build_name(source_id="23", source_name="my_label", version=3, raw_or_formatted="fail")

    assert str(excinfo.value) == "raw_or_formatted: must have value 'raw' or 'formatted'"


def test_input_audit_path_wrong_subfolder():
    location = tempfile.mkdtemp()
    os.chdir(location)

    subfolder_names = ["001", "002", "error"]
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(location, subfolder_name))

    result = input_audit_path(input_base_folder=location)
    shutil.rmtree(location)

    assert len(result) == 1
    assert result[0][0] == "ERR0002"


def test_input_audit_path_file_in_subfolder():
    location = tempfile.mkdtemp()
    os.chdir(location)

    # Create correct subfolders
    subfolder_names = ["001", "002"]
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(location, subfolder_name))

    # Create a file that should cause an error
    try:
        os.open("error_file.txt", os.O_CREAT)
    except OSError as e:
        if e.errno == errno.EEXIST:  # Failed as the file already exists.
            pass
        else:  # Something unexpected went wrong so reraise the exception.
            raise

    result = input_audit_path(input_base_folder=location)
    shutil.rmtree(location)

    assert len(result) == 1
    assert result[0][0] == "ERR0001"


def test_input_audit_path_empty_subfolder():
    location = tempfile.mkdtemp()
    os.chdir(location)

    result = input_audit_path(input_base_folder=location)
    shutil.rmtree(location)

    assert len(result) == 1
    assert result[0][0] == "ERR0003"
