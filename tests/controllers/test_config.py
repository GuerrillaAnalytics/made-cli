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

    assert test_config.has_section_wp() == True


def test_write():
    """Check that file is written out"""
    location = tempfile.mkdtemp()

    # Config file should not exist yet
    assert not os.path.isfile(os.path.join(location, Config.config_file_name))

    test_config = Config(location)
    test_config.write()

    # Config file should exist now
    assert os.path.isfile(os.path.join(location, Config.config_file_name))