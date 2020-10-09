import os
from sparkle_test_base.base import TestBase


class ApiGatewayTestBase(TestBase):
    def setUp(self):
        super().setUp()
        if self.is_test_env():
            self.start_database()
            self.wait_for_database()

            self.start_api_gateway()
            self.wait_for_api_gateway()

    def tearDown(self):
        super().tearDown()