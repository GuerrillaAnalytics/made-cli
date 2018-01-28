# -*- coding: utf-8 -*-
"""Tests for the Config class."""

import pytest
from click.testing import CliRunner

from made import cli


@pytest.fixture
def runner():
    """Command line runner for all tests"""
    return CliRunner()


def test_cli(runner):
    """Tests that the cli can be launched."""
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert not result.exception


def test_cli_unconfigured_folder(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, ['project'])
        assert result.exit_code == 1
        # assert result.output ==
        # 'Do you want to configure a project here? [y/N]:\n'
