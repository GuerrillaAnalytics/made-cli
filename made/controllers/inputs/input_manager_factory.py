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

    @abc.abstractmethod
    def list_inputs(self):
        """List all inputs in a project."""
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

    def list_inputs(self):
        print("not implemented yet")


class S3InputManager(InputManager):
    """
    Class for managing inputs folders on S3
    """

    def get_matching_s3_objects(self, bucket, prefix='', suffix=''):
        """
        Generate objects in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch objects whose key starts with
            this prefix (optional).
        :param suffix: Only fetch objects whose keys end with
            this suffix (optional).
        From https://alexwlchan.net/2018/01/listing-s3-keys-redux/
        """
        s3 = boto3.client('s3')
        kwargs = {'Bucket': bucket}

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = s3.list_objects_v2(**kwargs)

            try:
                contents = resp['Contents']
            except KeyError:
                return

            for obj in contents:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield obj

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def get_matching_s3_keys(bucket, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).

        From https://alexwlchan.net/2018/01/listing-s3-keys-redux/
        """
        for obj in get_matching_s3_objects(bucket, prefix, suffix):
            yield obj['Key']

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

    def list_inputs(self):
        print("not implemented yet")


if __name__ == "__main__":
    config = Config(os.getcwd())
    test = S3InputManager(config)

    for key in test.get_matching_s3_keys("js-dpp-lab-ds1-data-dev", "projects"):
        print(key)
