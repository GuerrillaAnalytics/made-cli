import configparser
import os


class Config(object):

    config_file_name = "made.config"
    section_wp = 'work_products'
    section_inputs = 'inputs'
    section_project = 'project'

    def __init__(self, folder):
        self.config = configparser.ConfigParser()
        self.path = os.path.join(folder, self.config_file_name)
        self.config.read(self.path)

        # add the section if it does not already exist
        if not self.config.has_section(self.section_inputs):
            self.config.add_section(self.section_inputs)

        if not self.config.has_section(self.section_wp):
            self.config.add_section(self.section_wp)

        if not self.config.has_section(self.section_project):
            self.config.add_section(self.section_project)

    def get_path(self):
        return self.config.get('templates', 'path')

    def has_section_wp(self):
        return self.config.has_section(self.section_wp)

    def add_section_wp(self):
        return self.config.add_section(self.section_wp)

    def add_option_wp_prefix(self, option_value='wp'):
        self.config.set(self.section_wp, 'prefix', option_value)

    def get_option_wp_prefix(self):
        return self.config.get(self.section_wp, 'prefix')

    def add_option_inputs_root(self, option_value='s3'):
        self.config.set(self.section_inputs, 'root', option_value)

    def add_option_project_root(self, option_value=os.getcwd()):
        self.config.set(self.section_project, 'root', option_value)

    def write(self):
        """Save configuration to file"""
        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)
            print(self.path)


if __name__ == '__main__':
    c = Config(os.getcwd())
    c.add_option_wp_prefix()
    c.add_option_inputs_root()
    print(c.get_option_wp_prefix())
    c.write()
