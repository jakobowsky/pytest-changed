# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock

from pytest_changed import get_changed_files_with_functions

GIT_DIFF_WITH_CHANGES = b'diff --git a/tests/dummy_test.py b/tests/dummy_test.py\n' \
                        b'index 6575e440acc807efabcbc156b8683c6344b6fda4..11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
                        b'--- a/tests/dummy_test.py\n' \
                        b'+++ b/tests/dummy_test.py\n' \
                        b'@@ -4,6 +4,7 @@ import pytest\n' \
                        b' class TestClassOne:\n' \
                        b'+\n' \
                        b'     @pytest.fixture(autouse=True)\n' \
                        b'     def fixture_one(self, db):\n' \
                        b'         db.init()\n' \
                        b'         yield\n' \
                        b'         db.quit()\n'

GIT_DIFF_NO_CHANGES = b'diff --git a/tests/dummy_test.py b/tests/dummy_test.py\n' \
                      b'index 6575e440acc807efabcbc156b8683c6344b6fda4..11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
                      b'--- a/tests/dummy_test.py\n' \
                      b'+++ b/tests/dummy_test.py\n' \
                      b'@@ -4,6 +4,7 @@ import pytest\n' \
                      b' class TestClassOne:\n' \
                      b'     @pytest.fixture(autouse=True)\n' \
                      b'     def fixture_one(self, db):\n' \
                      b'         db.init()\n' \
                      b'         yield\n' \
                      b'         db.quit()\n'


def test_shows_changed_tests(testdir):
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files..." in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_get_changed_files(get_changed_files_mock, testdir):
    diff = MagicMock()
    diff.diff = GIT_DIFF_WITH_CHANGES
    diff.a_path = "tests/dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    config_mock = MagicMock()
    config_mock.rootdir = testdir.tmpdir

    config_mock._getini = MagicMock()
    config_mock._getini.return_value = ["test_*.py", "*_test.py"]

    get_changed_files_mock.return_value = (modified_mock, added_mock)
    with patch("pytest_changed.Repo"):
        changed = get_changed_files_with_functions(config=config_mock)
        assert changed == {f'{testdir.tmpdir}/tests/dummy_test.py': ['TestClassOne']}


@patch("pytest_changed.get_changed_files")
def test_get_changed_files_output(get_changed_files_mock, testdir):
    diff = MagicMock()
    diff.diff = GIT_DIFF_WITH_CHANGES
    diff.a_path = "dummy_test.py"

    testdir.makepyfile(".py", dummy_test="""
        def dummy_test():
            assert True
    """)

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    config_mock = MagicMock()
    config_mock.rootdir = testdir
    config_mock._getini = MagicMock()
    config_mock._getini.return_value = ["test_*.py", "*_test.py"]

    get_changed_files_mock.return_value = (modified_mock, added_mock)
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1. {{'{}/dummy_test.py': ['TestClassOne']}}".format(
            testdir.tmpdir) in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_get_changed_files_output_no_changes(get_changed_files_mock, testdir):

    testdir.makepyfile(".py", dummy_test="""
        def dummy_test():
            assert True
    """)

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    config_mock = MagicMock()
    config_mock.rootdir = testdir
    config_mock._getini = MagicMock()
    config_mock._getini.return_value = ["test_*.py", "*_test.py"]

    get_changed_files_mock.return_value = (modified_mock, added_mock)
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 0." in result.stdout.str()
