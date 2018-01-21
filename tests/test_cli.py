# -*- coding: utf-8 -*-
"""Tests for the Config class."""

from click.testing import CliRunner

from made import cli

import pytest


@pytest.fixture
def runner():
    """TODO."""
    return CliRunner()


def test_cli(runner):
    """Tests that the cli can be launched."""
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert not result.exception
    # assert result.output.strip() == 'Hello, world.'
    print(result.output.strip())
