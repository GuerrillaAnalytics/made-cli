import abc


class InputManagerFactory(object):
    def create(type):
        if type == "s3":
            return S3InputManager()
        if type == "file":
            return FileInputManager()
        assert 0, "Bad manager creation: " + type

    factory = staticmethod(create)


class InputManager(abc.ABC):
    @abc.abstractmethod
    def create_input(self):
        pass

class S3InputManager(InputManager):
    def create_input(self):
        print("S3 input folder creation.")


class FileInputManager(InputManager):
    def create_input(self):
        print("File system folder creation.")

if __name__ == "__main__":

    # Create object using factory.
    obj = InputManagerFactory.create("s3")
    obj.create_input()

    obj = InputManagerFactory.create("file")
    obj.create_input()