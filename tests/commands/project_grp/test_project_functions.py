from made.commands.project_grp.project_functions import project_create_folder
from made.commands.project_grp.project_functions import project_audit_name

# from made.commands.project_grp.project_functions import project_init_wp
import os
import tempfile
import shutil
# import click
# from click.testing import CliRunner


def test_project_create_folder():

    location = tempfile.mkdtemp()
    os.chdir(location)
    new_folder = project_create_folder(id="ds134", label="project")
    expected_path = os.path.join(location, "ds134" + "_" + "project")
    shutil.rmtree(location)

    assert expected_path == new_folder


def test_project_audit_name_spaces():
    """Test that auditing project name returns correct results"""
    test_name = "ds045_  rest of name"
    result = project_audit_name(project_folder=test_name)
    assert result is False


def test_project_audit_name_case():
    """Test that auditing project name returns correct results"""
    test_name = "ds045_withUpperCase"
    result = project_audit_name(project_folder=test_name)
    assert result is False


def test_project_audit_name_correct():
    """Test that auditing project name returns correct results"""
    test_name = "ds056_corectname"
    result = project_audit_name(project_folder=test_name)
    assert result is True