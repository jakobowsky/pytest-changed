try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import pytest

pytest_plugins = 'pytester'


@pytest.fixture(autouse=True)
def create_dummy_test_file(testdir):
    testdir.makepyfile(".py", dummy_test="""
        class TestClassOne:

            def test_class_one_test_one(self):
                assert 1 + 1 == 2

            def test_class_one_test_two(self):
                assert 1 + 1 == 2


        class TestClassTwo:

            def test_class_two_test_one(self):
                assert 1 + 1 == 2

            def test_class_two_test_two(self):
                assert 1 + 1 == 2
    """)
    testdir.makepyfile(".py", dummy_2_test="""
        class TestClassOne:

            def test_class_one_test_one(self):
                assert 1 + 1 == 2

            def test_class_one_test_two(self):
                assert 1 + 1 == 2
    """)


@pytest.fixture
def config_mock(testdir):
    config_mock = MagicMock()
    config_mock.rootdir = testdir.tmpdir
    config_mock._getini = MagicMock()
    config_mock._getini.return_value = ["test_*.py", "*_test.py"]
    return config_mock
