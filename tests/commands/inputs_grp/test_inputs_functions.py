import os
import sys

from made.commands.inputs_grp.input_functions import  validate_input_version
from made.controllers.config import Config

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import errno
import os
import shutil
import tempfile
import pytest

from made.controllers.inputs.inputs_functions import input_audit_path


def test_validate_input_version():
    assert validate_input_version('34') == True
    assert validate_input_version('wp34') == False
    assert validate_input_version('') == False
    assert validate_input_version(' 45 ') == False
    assert validate_input_version('-45') == False

def test_input_audit_path_wrong_subfolder():
    location = tempfile.mkdtemp()
    os.chdir(location)

    subfolder_names = ["001", "002", "error"]
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(location, subfolder_name))

    result = input_audit_path(input_base_folder=location)
    shutil.rmtree(location)

    assert len(result) >= 1
    assert any("ERR0002" in code for code in result)


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

    assert len(result) >= 1
    assert any("ERR0001" in code for code in result)


def test_input_audit_path_empty_subfolder():
    location = tempfile.mkdtemp()
    os.chdir(location)

    result = input_audit_path(input_base_folder=location)
    shutil.rmtree(location)

    assert len(result) >= 1
    assert result[0][0] == "ERR0003"

