import os
import tempfile

from made.controllers.config import Config
from made.controllers.inputs.input_manager_factory import FileInputManager


def test_create_new_source():
    location = tempfile.mkdtemp()
    configuration = Config(os.getcwd())
    configuration.add_option_project_name(option_value='my_project')
    configuration.add_option_inputs_storage(option_value='file')
    configuration.add_option_files_root(location)
    test_class = FileInputManager(config=configuration)
    expected_path = os.path.join(location, 'projects',
                                 'my_project',
                                 'inputs',
                                 '45_my_source',
                                 '01',
                                 'raw',
                                 'data')

    # try to create the new source folder
    test_class.create_new_source(source_id='45', source_label='my_source')
    assert os.path.exists(expected_path)
