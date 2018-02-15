"""Tests of the S3 Input Manager class."""

import tempfile

from made.controllers.config import Config
from made.controllers.inputs.input_manager_factory import S3InputManager


def test_constructor():
    """Test that the constructor works correctly."""
    location = tempfile.mkdtemp()
    configuration = Config(location)
    manager = S3InputManager(configuration)
    assert manager is not None
