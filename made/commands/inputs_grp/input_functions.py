import string


def validate_input_id(input_id):

    if ' ' in input_id: return False

    # create a set of invalid characters
    return str(input_id).isdigit()

