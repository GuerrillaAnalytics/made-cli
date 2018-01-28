"""Tests of the Config class."""

import os
import tempfile

from made.controllers.config import Config


def test_constructor():
    """Test that the constructor runs correctly."""
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # Check the defaults are set correctly
    assert test_config.config_file_name == "made.config"
    assert test_config.section_wp == "work_products"
    assert test_config.section_inputs == "inputs"
    assert test_config.section_project == "project"


def test_add_option_input_s3bucket():
    """Test that an S3 option can be added correctly."""
    location = tempfile.mkdtemp()
    test_config = Config(location)
    test_config.add_option_inputs_S3bucket("bucket_value")
    assert test_config.get_S3bucket_name() == "bucket_value"


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
