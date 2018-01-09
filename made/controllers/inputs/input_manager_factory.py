import os
import abc


def input_build_name(source_id, source_name, version, raw_or_formatted="raw"):
    """create an input folder path for a given input"""

    valid = {"raw", "formatted"}
    if raw_or_formatted not in valid:
        raise ValueError("raw_or_formatted: must have value 'raw' or 'formatted'")

    source_id = source_id.lower()
    version = str(version).zfill(3)

    path = os.path.join(source_id + "_" + source_name,
                        version, raw_or_formatted, "data")
    return path


class InputManagerFactory(object):
    """ Class to manage creation of appropriate input managers
    """

    def create(type):
        if type == "s3":
            return S3InputManager()
        if type == "file":
            return FileInputManager()
        assert 0, "Bad manager creation: " + type

    factory = staticmethod(create)


class InputManager(abc.ABC):

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


class S3InputManager(InputManager):

    def create_new_source(self):
        print("not implemented yet")

    def create_new_source_version(self):
        print("not implemented yet")

    def audit(self):
        print("not implemented yet")


class FileInputManager(InputManager):

    def create_new_source(self):
        print("not implemented yet")

        # TODO Get the root path for the input and check it exists
        # TODO Check the source ID is provided and correct
        # TODO Check the source label is provided and correct
        # TODO Build path to new source
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