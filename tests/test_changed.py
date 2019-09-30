# -*- coding: utf-8 -*-
from unittest.mock import patch

GIT_DIFF_NO_CHANGES = b'diff --git a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'index 6575e440acc807efabcbc156b8683c6344b6fda4..11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
                      b'--- a/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'+++ b/tests/app/test_basic_functions/log_in_log_out/log_in_feature_test.py\n' \
                      b'@@ -4,6 +4,7 @@ import pytest\n' \
                      b' class TestLogInFeature:\n' \
                      b'     @pytest.fixture(scope=\'function\', autouse=True)\n' \
                      b'     def _setup_teardown(self, master):\n+\n' \
                      b'         master.main_screen.logout()  # setup\n' \
                      b'         yield  # test execution\n' \
                      b'         # teardown\n' \
                      b'diff --git a/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py b/tests/app/test_basic_functions/log_in_log_out/log_out_feature_test.py\n' \
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


def test_shows_changed_tests(testdir):
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files..." in result.stdout.str()
