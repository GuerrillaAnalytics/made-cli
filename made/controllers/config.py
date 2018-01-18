import configparser
import os
import logging

class Config(object):
    """ Class to manage accessing and writing a configuration
    """

    config_file_name = "made.config"
    section_wp = 'work_products'
    section_inputs = 'inputs'
    section_project = 'project'
    section_pipeline = 'pipeline'

    def __init__(self, folder):
        self.project_folder = folder
        self.config = configparser.ConfigParser()
        self.path = os.path.join(folder, self.config_file_name)
        self.config.read(self.path)

        logging.getLogger("my logger").debug("Configuring from: " + self.path)

        # add the section if it does not already exist
        if not self.config.has_section(self.section_inputs):
            self.config.add_section(self.section_inputs)

        if not self.config.has_section(self.section_wp):
            self.config.add_section(self.section_wp)

        if not self.config.has_section(self.section_project):
            self.config.add_section(self.section_project)

        if not self.config.has_section(self.section_pipeline):
            self.config.add_section(self.section_pipeline)

    def has_config_file(self):
        if os.path.exists(self.path):
            logging.getLogger("my logger").info("Config file already exists")
            return True
        else:
            logging.getLogger("my logger").debug("Config file does not exist")
            return False

    def get_path(self):
        return self.config.get('templates', 'path')

    def has_section_wp(self):
        return self.config.has_section(self.section_wp)

    def add_section_wp(self):
        return self.config.add_section(self.section_wp)

    def add_section_pipeline(self):
        return self.config.add_section(self.section_pipeline)

    def add_option_wp_prefix(self, option_value='wp'):
        self.config.set(self.section_wp, 'prefix', option_value)

    def get_project_name(self):
        """Return the project name (inferred from project folder name"""
        return os.path.basename(self.project_folder)

    def get_option_wp_prefix(self):
        if not self.config.has_option(self.section_wp, 'prefix'):
            self.add_option_wp_prefix()

        return self.config.get(self.section_wp, 'prefix')

    def add_option_inputs_root(self, option_value='s3'):
        """ Input folder type (S3 or file) """
        self.config.set(self.section_inputs, 'root', option_value)

    def add_option_inputs_S3bucket(self, option_value):
        self.config.set(self.section_inputs, 'bucket', option_value)

    def get_S3bucket_name(self):
        return self.config.get(Config.section_inputs,'bucket')

    def get_inputs_root(self):
        return self.config.get(Config.section_inputs,'root')

    def write(self):

        print(self.path)
        cfgfile = open(self.path, 'w')

        """Save configuration to file"""
        self.config.write(cfgfile)
        cfgfile.close()


if __name__ == '__main__':
    c = Config(os.getcwd())
    c.add_option_wp_prefix()
    c.add_option_inputs_root()
    print(c.get_option_wp_prefix())
    c.write()