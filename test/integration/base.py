import os
from sparkle_test_base.base import TestBase
from sparkle_test_base.config import API_GW_API_BASE


class ApiGatewayTestBase(TestBase):
    def setUp(self):
        super().setUp()
        self.url = API_GW_API_BASE
        if self.is_test_env():
            self.start_database()
            self.wait_for_database()

            self.start_api_gateway()
            self.wait_for_api_gateway()
