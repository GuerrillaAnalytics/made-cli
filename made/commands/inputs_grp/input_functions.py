import string


def validate_input_version(input_version):
    """Check that an input id is a number without spaces"""
    if ' ' in input_version: return False

    # create a set of invalid characters
    return str(input_version).isdigit()


def format_input_version(input_version):
    """Format an input version to have leading zeroes"""
    return str(input_version).zfill(2)