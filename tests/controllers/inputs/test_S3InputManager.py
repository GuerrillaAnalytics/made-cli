import tempfile

from made.controllers.config import Config
from made.controllers.inputs.input_manager_factory import S3InputManager


def test_constructor():
    location = tempfile.mkdtemp()
    configuration = Config(location)
    manager = S3InputManager(configuration)

