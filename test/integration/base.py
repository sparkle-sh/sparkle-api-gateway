import os
from sparkle_test_base.base import TestBase


class ApiGatewayTestBase(TestBase):
    def setUp(self):
        super().setUp()
        if self.is_test_env():
            self.start_api_gateway()
            self.wait_for_api_gw()

    def tearDown(self):
        super().tearDown()