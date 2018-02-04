import abc
import logging
import os

import boto3
import botocore

from made.controllers.config import Config


class InputManagerFactory(object):
    """
    Class to manage creation of appropriate input managers
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

    def create_folder_path(self, project_name, source_id, source_label, version):
        """
        Create the full folder path to an input starting at 'projects'
        """

        # Ensure there is a trailing / so a folder is created in S3
        # instead of a file
        s = \
            "/".join(
                ["projects", project_name,
                 "inputs",
                 str(source_id) + "_" + source_label,
                 version, "raw", "data",
                 ""])
        return s

    @abc.abstractmethod
    def create_new_source(self, source_id, source_label):
        """
        Create an input source within an
        input folder with the right folder path and structure
        """
        pass

    @abc.abstractmethod
    def create_new_source_version(self):
        """
        Create an input source version within an
        input source with the right folder path and structure
        """
        pass

    @abc.abstractmethod
    def audit(self):
        """Do sense checks on given input folder"""
        pass


class FileInputManager(InputManager):
    def create_new_source(self, source_id, source_label):
        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_inputs_root()
        logging.getLogger("my logger").debug(
            "Inputs root is: " + inputs_root)
        # TODO Check the source ID is provided and correct

        # Check the source label is provided and correct
        from made.controllers.inputs.inputs_functions \
            import validate_source_label
        validate_source_label(source_label)

        # Build path to new source
        project_name = self.configuration.get_project_name()
        version = "01"
        s = self.create_folder_path(project_name, source_id, source_label, version)
        s = os.path.join(self.configuration.get_option_files_root(), s)
        print("path is: " + s)
        if not os.path.exists(s):
            try:
                os.makedirs(s)
                logging.getLogger('my logger'). \
                    debug("FileInputManager created file input folder: " + s)
            except Exception as e:
                logging.getLogger('my logger'). \
                    exception("Could not create new source at " + s)

    def create_new_source_version(self):
        print("not implemented yet")

    def audit(self):
        print("not implemented yet")


class S3InputManager(InputManager):
    def create_new_source(self, source_id, source_label):
        """Create a new S3 source folder"""

        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_inputs_root()
        logging.getLogger("my logger").debug(
            "Inputs root is: " + inputs_root)
        # TODO Check the source ID is provided and correct

        # Check the source label is provided and correct
        from made.controllers.inputs.inputs_functions \
            import validate_source_label
        validate_source_label(source_label)

        # Build path to new source
        project_name = self.configuration.get_project_name()
        version = "01"
        s = self.create_folder_path(project_name, source_id, source_label, version)
        logging.getLogger('my logger').debug("s3 input folder: " + s)

        # TODO Check new source does not exist already
        # Create new folder at target path
        # add first version and subfolder
        profile_name_configured = self.configuration.get_option_s3_profile()
        dev = boto3.session.Session(profile_name=profile_name_configured)
        client = dev.client('s3')
        try:
            response = client.put_object(
                Bucket=self.configuration.get_option_s3_bucket_name(),
                Body='',
                Key=s,
                ServerSideEncryption=self.configuration.get_option_s3_encryption())
            logging.getLogger('my logger').info(response)
        except botocore.exceptions.ClientError:
            logging.getLogger('my logger') \
                .exception("Problem creating folder in s3 bucket. "
                           "Check your profile permissions and "
                           "encryption settings")

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
