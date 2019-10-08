# -*- coding: utf-8 -*-

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

GIT_DIFF_CHANGE_IN_FUNCTION = \
    b'diff --git a/tests/dummy_test.py b/tests/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/tests/dummy_test.py\n' \
    b'+++ b/tests/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n'

GIT_DIFF_CHANGE_IN_CLASS = \
    b'diff --git a/tests/dummy_test.py b/tests/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/tests/dummy_test.py\n' \
    b'+++ b/tests/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'+\n' \
    b'\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'+\n' \
    b'\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'


def test_shows_changed_tests(testdir):
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files..." in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_no_changes(get_changed_files_mock, testdir, config_mock):
    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 0." in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_changed_function(get_changed_files_mock, testdir, config_mock):
    """
    In case of changes just to specific functions only their names
    will be detected.
    """
    diff = MagicMock()
    diff.diff = GIT_DIFF_CHANGE_IN_FUNCTION
    diff.a_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1. {" \
               "'%s/dummy_test.py': [" \
               "'test_class_one_test_one', " \
               "'test_class_two_test_two']}" % str(testdir.tmpdir) in \
               result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_changed_class_and_function(
        get_changed_files_mock,
        testdir,
        config_mock
):
    """
    In case of changes inside the class body, the class names should
    be detected.

    To make sure all tests inside the class are running as changes in the class
    definition may affect test functions defined in the scope of the class.

    When pytest receives a class it will run all test-functions
    that are contained.
    """
    diff = MagicMock()
    diff.diff = GIT_DIFF_CHANGE_IN_CLASS
    diff.a_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1. {" \
               "'%s/dummy_test.py': [" \
               "'TestClassOne', " \
               "'TestClassTwo']}" % str(testdir.tmpdir) in result.stdout.str()
