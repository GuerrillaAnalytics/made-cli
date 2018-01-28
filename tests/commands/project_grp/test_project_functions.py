"""Tests for all project functions."""
import os
import shutil
import tempfile

from made.commands.project_grp.project_functions \
    import project_create_folder, validate_project_name


def test_project_create_folder():
    """Test that the project folder is created in the right format."""
    location = tempfile.mkdtemp()
    os.chdir(location)
    new_folder = project_create_folder(id="ds134", label="project")
    expected_path = os.path.join(location, "ds134" + "_" + "project")
    shutil.rmtree(location)

    assert expected_path == new_folder


def test_validate_project_name():
    """Test that the validate project name function works."""
    # name has a space should fail
    assert validate_project_name('ds 045') is False
    assert validate_project_name('Ds_045') is False

    # name has a special character should fail
    assert validate_project_name('ds#234') is False
    assert validate_project_name('ds!234') is False
    assert validate_project_name('ds$234') is False
    assert validate_project_name('ds£234') is False
    assert validate_project_name('ds&234') is False
    assert validate_project_name('ds*234') is False
    assert validate_project_name('ds(234') is False
    assert validate_project_name('ds)234') is False
