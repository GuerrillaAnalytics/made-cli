import tempfile

from made.controllers.inputs import input_manager_factory
from made.controllers.config import Config
from made.controllers.inputs.input_manager_factory import S3InputManager


def test_constructor():
    location = tempfile.mkdtemp()
    configuration = Config(location)
    manager = S3InputManager(configuration)

def test_create_s3_folder():
    location = tempfile.mkdtemp()
    configuration = Config(location)
    manager = S3InputManager(configuration)
    configuration.add_option_inputs_S3bucket("bucket-name")

    # test_value\
    #     =input_manager_factory.create_s3_folder(bucket="bucket-name",source_id="45",
    #                                             source_label="transactions",version="02")
    # assert test_value=="S3://bucket-name/45_transactions/02/raw/data"