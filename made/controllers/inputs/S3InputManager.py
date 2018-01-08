from controllers.inputs.input_manager_factory import InputManager


class S3InputManager(InputManager):
    def create_input(self):
        print("S3 input folder creation.")
