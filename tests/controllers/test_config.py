"""Tests of the Config class."""

import os
import tempfile

import pytest

from made.controllers.config import Config
from made.exceptions.madeExceptions import MadeException


def test_constructor():
    """Test that the constructor runs correctly."""
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # Check the defaults are set correctly
    assert test_config.config_file_name == "made.config"
    assert test_config.section_wp == "work_products"
    assert test_config.section_inputs == "inputs"
    assert test_config.section_project == "project"


def test_get_wp_prefix():
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # wp prefix should be blank if nothing has been specified yet
    assert test_config.get_option_wp_prefix() == ''

    # make sure the correct prefix is now returned
    test_config.add_option_wp_prefix('tt')
    assert test_config.get_option_wp_prefix() == 'tt'


def test_add_option_input_s3bucket():
    """Test that an S3 option can be added correctly."""
    location = tempfile.mkdtemp()
    test_config = Config(location)
    test_config.add_option_inputs_S3bucket("bucket_value")
    assert test_config.get_option_s3_bucket_name() == "bucket_value"


def test_add_option_inputs_storage():
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # check exception is raised when no value has been set
    with pytest.raises(MadeException):
        test_config.get_option_inputs_storage()

    # test that value is returned after it has been set
    test_config.add_option_inputs_storage(option_value='s3')
    assert test_config.get_option_inputs_storage() == 's3'


def test_write():
    """Check that file is written out."""
    location = tempfile.mkdtemp()

    # Config file should not exist yet
    assert not os.path.isfile(os.path.join(location, Config.config_file_name))

    test_config = Config(location)
    test_config.write()

    # Config file should exist now
    assert os.path.isfile(os.path.join(location, Config.config_file_name))


def test_get_project_name():
    """Test that the correct project name is returned."""
    temp_location = tempfile.mkdtemp()
    project_folder = os.path.join(temp_location, "test_project_folder")
    test_config = Config(project_folder)
    test_config.add_option_project_name("test_project")
    assert test_config.get_project_name() == os.path.basename("test_project")
