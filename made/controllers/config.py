import logging
import os

from configobj import ConfigObj


class Config(object):
    """
    Class to manage accessing and writing a configuration
    """

    config_file_name = "made.config"
    section_wp = 'work_products'
    section_inputs = 'inputs'
    section_project = 'project'
    section_pipeline = 'pipeline'

    def __init__(self, folder):
        self.project_folder = folder
        self.config = ConfigObj(os.path.join(folder, self.config_file_name))

        # Make sure all sections exist to avoid errors later
        self.config[self.section_project] = {}
        self.config[self.section_wp] = {}
        self.config[self.section_inputs] = {}
        self.config[self.section_pipeline] = {}

    def has_config_file(self):
        if os.path.exists(self.config.filename):
            logging.getLogger("my logger").info("Config file already exists")
            return True
        else:
            logging.getLogger("my logger").debug("Config file does not exist")
            return False

    def add_section_pipeline(self):
        return self.config.add_section(self.section_pipeline)

    def add_option_wp_prefix(self, option_value='wp'):
        # TODO validate prefix
        self.config[self.section_wp]['prefix'] = option_value

    def get_project_name(self):
        return_value = self.config[self.section_project]['name']
        return return_value

    def add_option_project_name(self, option_value):
        self.config[self.section_project]['name'] = option_value

    def get_option_wp_prefix(self):

        try:
            value = self.config[self.section_wp]['prefix']
            return value
        except KeyError:
            logging.getLogger('my logger') \
                .debug("wp prefix not specified yet")
            return ""

    def add_option_files_root(self, option_value):
        """Parent location where all projects exist"""
        self.config[self.section_inputs]['files_root'] = option_value
        pass

    def get_option_files_root(self):

        try:
            result = self.config[self.section_inputs]['files_root']
            return result
        except KeyError:
            logging.getLogger('my logger') \
                .debug("Files root not configured yet")
            return ''

    def add_option_inputs_S3bucket(self, option_value):
        self.config[self.section_inputs]['bucket'] = option_value

    def get_option_s3_bucket_name(self):

        try:
            result = self.config[self.section_inputs]['bucket']
            return result
        except KeyError:
            logging.getLogger('my logger') \
                .debug("S3 bucket name not configured yet")
            return ''

    def add_option_s3_profile(self, value):
        self.config[self.section_inputs]['profile'] = value
        pass

    def get_option_s3_profile(self):
        try:
            result = self.config[self.section_inputs]['profile']
            return result
        except KeyError:
            logging.getLogger('my logger') \
                .debug('S3 profile not specified yet')
            return ''

    def add_option_s3_encryption(self, value):
        self.config[self.section_inputs]['sse'] = value
        pass

    def get_option_s3_encryption(self):
        try:
            result = self.config[self.section_inputs]['sse']
            return result
        except KeyError:
            logging.getLogger('my logger').debug('SSE not specified yet')
            return ''

    def add_option_inputs_storage(self, option_value='s3'):
        """Input folder root type (S3 or file)"""

        self.config[self.section_inputs]['inputs_storage'] = option_value

    def get_option_inputs_storage(self):

        try:
            result = self.config[self.section_inputs]['inputs_storage']
            return result
        except KeyError:
            return ''

    def write(self):
        self.config.write()


if __name__ == '__main__':
    c = Config(os.getcwd())
    print(c.config_file_name)
    c.add_option_inputs_S3bucket('my-bucket')
    c.write()
