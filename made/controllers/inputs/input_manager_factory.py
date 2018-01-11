import os
import abc
import boto3
import logging

from made.controllers import config
from made.controllers.config import Config

def create_s3_folder(bucket,source_id,source_label,version):
    s = \
        "/".join(
            ["S3://" + bucket, source_id + "_" + source_label, version, "raw/data"])
    return s


class InputManagerFactory(object):
    """ Class to manage creation of appropriate input managers
    """

    def create(config):
        type = config.config.get(Config.section_inputs, "root")

        if type == "s3":
            logging.getLogger("my logger").debug("Creating an s3 input manager")
            return S3InputManager(config)
        if type == "file":
            logging.getLogger("my logger").debug("Creating an file input manager")
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

    def create_new_source(self,source_id,source_label):
        """ Create a new S3 source folder"""

        print("not implemented yet")

        # TODO Get the root path for the input and check it exists
        inputs_root = self.configuration.get_inputs_root()
        logger = logging.getLogger("my logger").debug("Inputs root is: " + inputs_root)
        # TODO Check the source ID is provided and correct
        # TODO Check the source label is provided and correct
        # TODO Build path to new source

        version = "01"
        s=create_s3_folder(self.configuration.get_S3bucket_name(),source_id,source_label,version)
        logging.getLogger('my logger').debug("Input folder: " + s)
        # TODO Check new source does not exist already
        # TODO Create new folder at target path
        # TODO add first version and subfolder

    def create_new_source_version(self):
        print("not implemented yet")

    def audit(self):
        print("not implemented yet")


if __name__ == "__main__":

    # Create object using factory.
    obj = InputManagerFactory.create("s3")
    obj.create_new_source()

    obj = InputManagerFactory.create("file")
    obj.create_new_source()

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('js-dpp-lab-ds1-data-dev')
    for object in my_bucket.objects.all():
        print(object)