from made.utils.config import Config
import tempfile


def test_constructor():
    location = tempfile.mkdtemp()
    test_config = Config(location)

    # Check the defaults are set correctly
    assert test_config.config_file_name == "made.config"
    assert test_config.section_wp == "work_products"
    assert test_config.section_inputs == "inputs"
    assert test_config.section_project == "project"

    assert test_config.has_section_wp() == True