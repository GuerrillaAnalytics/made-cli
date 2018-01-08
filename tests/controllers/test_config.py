import os
import tempfile

from made.controllers.config import Config


def test_constructor():
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # Check the defaults are set correctly
    assert test_config.config_file_name == "made.config"
    assert test_config.section_wp == "work_products"
    assert test_config.section_inputs == "inputs"
    assert test_config.section_project == "project"
    assert test_config.config.sections().__len__() == 4
    assert test_config.has_section_wp() == True


def test_add_option_input_S3bucket():
    location = tempfile.mkdtemp()
    test_config = Config(location)
    test_config.add_option_input_S3bucket("bucket_value")
    assert test_config.config.get(test_config.section_inputs, 'bucket') == "bucket_value"


def test_write():
    """Check that file is written out"""
    location = tempfile.mkdtemp()

    # Config file should not exist yet
    assert not os.path.isfile(os.path.join(location, Config.config_file_name))

    test_config = Config(location)
    test_config.write()

    # Config file should exist now
    assert os.path.isfile(os.path.join(location, Config.config_file_name))