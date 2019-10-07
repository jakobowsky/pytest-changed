# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock

from pytest_changed import get_changed_files_with_functions

GIT_DIFF_WITH_CHANGES = b'diff --git a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                        b'index 6575e440acc807efabcbc156b8683c6344b6fda4..11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
                        b'--- a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                        b'+++ b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                        b'@@ -4,6 +4,7 @@ import pytest\n' \
                        b' class TestLogInFeature:\n' \
                        b'     @pytest.fixture(scope=\'function\', autouse=True)\n' \
                        b'     def _setup_teardown(self, master):\n' \
                        b'+\n' \
                        b'         master.main_screen.logout()  # setup\n' \
                        b'         yield  # test execution\n' \
                        b'         # teardown\n'

GIT_DIFF_WITH_CHANGES_2 = b'diff --git a/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py b/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py\n' \
                          b'index 8e833cd726424aa0961fa62d54b53a8f37aee227..78f3f3f68074b8f072b54622d7d7aec22557f0fe 100644\n' \
                          b'--- a/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py\n' \
                          b'+++ b/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py\n' \
                          b'@@ -4,6 +4,7 @@ from framework.qa_constants.qa_waiters.qa_waiters import QAWaiters\n' \
                          b' \n' \
                          b' \n' \
                          b' class TestLogoutFeature:\n' \
                          b'+\n' \
                          b'     def test_logout_via_employee_menu(self, master):\n' \
                          b'         master.main_screen.employee_button.tap()\n' \
                          b'         master.main_screen.employee_choice_popover.logout_button.tap()\n'

GIT_DIFF_NO_CHANGES = b'diff --git a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'index 6575e440acc807efabcbc156b8683c6344b6fda4..11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
                      b'--- a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'+++ b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'@@ -4,6 +4,7 @@ import pytest\n' \
                      b' class TestLogInFeature:\n' \
                      b'     @pytest.fixture(scope=\'function\', autouse=True)\n' \
                      b'     def _setup_teardown(self, master):\n' \
                      b'         master.main_screen.logout()  # setup\n' \
                      b'         yield  # test execution\n' \
                      b'         # teardown\n'


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
        assert changed == {f'{testdir.tmpdir}/tests/dummy_test.py': ['TestLogoutFeature']}


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
        assert "Changed test files... 1. {{'{}/dummy_test.py': ['TestLogoutFeature']}}".format(
            testdir.tmpdir) in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_get_changed_files_output_no_changes(get_changed_files_mock, testdir):
    diff = MagicMock()
    diff.diff = GIT_DIFF_NO_CHANGES
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
        assert "Changed test files... 0." in result.stdout.str()
