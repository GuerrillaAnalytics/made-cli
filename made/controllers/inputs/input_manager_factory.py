import abc
import logging
import os

import boto3
import botocore

from made.controllers.config import Config
from made.utils.S3Wrapper import S3Wrapper


class InputManagerFactory(object):
    """
    Class to manage creation of appropriate input managers
    """

    def create(config):
        storage_type = config.config.get_option_inputs_storage()

        if storage_type == "s3":
            logging.getLogger("my logger").debug(
                "Creating an s3 input manager")
            return S3InputManager(config)
        if storage_type == "file":
            logging.getLogger("my logger").debug(
                "Creating a file input manager")
            return FileInputManager(config)
        else:
            logging.getLogger("Bad manager creation: " + storage_type)

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

    @abc.abstractmethod
    def list_inputs(self):
        """List all inputs in a project."""
        pass


class FileInputManager(InputManager):
    def create_new_source(self, source_id, source_label):
        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_option_inputs_storage()
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

    def list_inputs(self):
        print("not implemented yet")


class S3InputManager(InputManager):
    """
    Class for managing inputs folders on S3
    """

    def listInputVersions(self, project_name, input_source):
        """Create a list of keys of just the input versions within a given source"""

        s3_wrapper = S3Wrapper(self.configuration.get_option_s3_bucket_name
                               , self.configuration.get_option_s3_profile)
        prefix_path = "projects/" + project_name + '/inputs/' + input_source + '/'
        print("Prefix path: " + prefix_path)
        unique_versions = s3_wrapper.listFolders(parent_key=prefix_path)

        return unique_versions

    def listInputs(self, project_name):
        """Create a list of keys of just the input folders in a project"""

        s3_wrapper = S3Wrapper(self.configuration.get_option_s3_bucket_name
                               , self.configuration.get_option_s3_profile)
        prefix = "projects/" + project_name + '/inputs/'

        unique_inputs = s3_wrapper.listFolders(prefix)
        return unique_inputs

    def create_new_source(self, source_id, source_label):
        """Create a new S3 source folder"""

        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_option_inputs_storage()
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
        """Creates a new version within an existing source"""
        print("not implemented yet")

        # list existing versions within source and get max

        # throw error if version is wrong

        # create path

        # create sources

    def audit(self):
        print("not implemented yet")

    def list_inputs(self):
        print("not implemented yet")


if __name__ == "__main__":
    config = Config(os.getcwd())
    config.add_option_files_root('s3')
    config.add_option_inputs_S3bucket('js-dpp-lab-ds1-data-dev')
    config.add_option_s3_profile('dpp1')
    config.add_option_project_name()
    test = S3InputManager(config)
