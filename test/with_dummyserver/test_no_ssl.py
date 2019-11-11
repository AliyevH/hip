"""
Test connections without the builtin ssl module

Note: Import urllib3 inside the test functions to get the importblocker to work
"""
import pytest
from ..test_no_ssl import TestWithoutSSL

from dummyserver.testcase import HTTPDummyServerTestCase, HTTPSDummyServerTestCase

import pytest
import urllib3

# Retry failed tests
pytestmark = pytest.mark.flaky


class TestHTTPWithoutSSL(HTTPDummyServerTestCase, TestWithoutSSL):
    @pytest.mark.skip(
        reason=(
            "TestWithoutSSL mutates sys.modules."
            "This breaks the backend loading code which imports modules at runtime."
            "See discussion at https://github.com/python-trio/urllib3/pull/42"
        )
    )
    def test_simple(self):
        with urllib3.HTTPConnectionPool(self.host, self.port) as pool:
            r = pool.request("GET", "/")
            assert r.status == 200, r.data


class TestHTTPSWithoutSSL(HTTPSDummyServerTestCase, TestWithoutSSL):
    def test_simple(self):
        try:
            pool = urllib3.HTTPSConnectionPool(self.host, self.port, cert_reqs="NONE")
        except urllib3.exceptions.SSLError as e:
            assert "SSL module is not available" in str(e)
        finally:
            pool.close()
