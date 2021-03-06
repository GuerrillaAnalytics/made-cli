import os
import abc
import boto3
import logging
import sys
import botocore

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from made.controllers import config
from made.controllers.config import Config


def create_folder_path(project_folder_name, source_id, source_label, version):
    """Create the full folder path to an input"""

    # Ensure there is a trailing / so a folder is created in S3
    # instead of a file
    s = \
        "/".join(
            ["projects", project_folder_name, "inputs", str(source_id) + "_" + source_label, version, "raw", "data", ""])
    return s


class InputManagerFactory(object):
    """ Class to manage creation of appropriate input managers
    """

    def create(config):
        type = config.config.get(Config.section_inputs, "root")

        if type == "s3":
            logging.getLogger("my logger").debug(
                "Creating an s3 input manager")
            return S3InputManager(config)
        if type == "file":
            logging.getLogger("my logger").debug(
                "Creating an file input manager")
            return FileInputManager(config)
        assert 0, "Bad manager creation: " + type

    factory = staticmethod(create)


class InputManager(abc.ABC):
    def __init__(self, config):
        self.configuration = config
        pass

    @abc.abstractmethod
    def create_new_source(self):
        """Create an input source within an
        input folder with the right folder path and structure"""
        pass

    @abc.abstractmethod
    def create_new_source_version(self):
        """Create an input source version within an
        input source with the right folder path and structure"""
        pass

    @abc.abstractmethod
    def audit(self):
        """Do sense checks on given input folder"""
        pass


class FileInputManager(InputManager):
    def __init__(self):
        pass

    def create_new_source(self):
        print("not implemented yet")

    def create_new_source_version(self):
        print("not implemented yet")

    def audit(self):
        print("not implemented yet")


class S3InputManager(InputManager):
    def create_new_source(self, source_id, source_label):
        """ Create a new S3 source folder"""

        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_inputs_root()
        logger = logging.getLogger("my logger").debug(
            "Inputs root is: " + inputs_root)
        # TODO Check the source ID is provided and correct
        # TODO Check the source label is provided and correct
        # TODO Build path to new source
        project_name = 'enda'
        project_name = self.configuration.get_project_name()
        version = "01"
        s = create_folder_path(project_name, source_id, source_label, version)
        logging.getLogger('my logger').debug("s3 input folder: " + s)
        # TODO Check new source does not exist already
        # TODO Create new folder at target path
        # TODO add first version and subfolder
        dev = boto3.session.Session(profile_name='dpp1')
        client = dev.client('s3')
        try:
            response = client.put_object(
                Bucket=self.configuration.get_S3bucket_name(),
                Body='',
                Key=s,
                ServerSideEncryption='AES256')
            logging.getLogger('my logger').info(response)
        except botocore.exceptions.ClientError:
            logging.getLogger('my logger') \
                .exception("Problem creating folder in s3 bucket"
                           " Check your profile permissions and encryption settings")

    def create_new_source_version(self):
        print("not implemented yet")

    def audit(self):
        print("not implemented yet")


if __name__ == "__main__":
    # Create object using factory.
    # config=Config(os.getcwd())
    # config.add_option_inputs_root('s3')
    # config.add_option_inputs_S3bucket('js-dpp-lab-ds1-data-dev')
    # obj = InputManagerFactory.create(config)
    # obj.create_new_source(45,'transactions')
    dev = boto3.session.Session(profile_name='dpp1')
    client = dev.client('s3')
    result = client.list_objects(
        Bucket="js-dpp-lab-ds1-data-dev",
        Prefix="projects/")
    print(result)
    print("")
    dev = boto3.session.Session(profile_name='dpp1')
    client = dev.client('s3')

    response = client.put_object(
        Bucket='js-dpp-lab-ds1-data-dev',
        Body='',
        Key='projects/test_folder/',
        ServerSideEncryption='AES256')
