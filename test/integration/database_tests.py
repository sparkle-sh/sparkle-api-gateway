from sparkle_test_base.base import TestBase


class DatabaseTests(TestBase):
    def setUp(self):
        super().setUp()
        if self.is_test_env():
            self.start_database()
            self.wait_for_database()

    def tearDown(self):
        super().tearDown()
        self.db_conn.close()

    def test_check_tables(self):
        cursor = self.get_db_cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        self.assertEqual(tables[0][0], "users")

