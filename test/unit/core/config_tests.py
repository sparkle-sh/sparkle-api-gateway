import os
import json
import unittest
import ddt
from core import config, error

TEST_CONFIG = f'{os.getenv("UTILS_PATH")}/test_config.json'
CORRUPTED_CONFIGS = [
    {},
    {
        'api': {}
    },
    {
        'api': {
            'host': 'localhost'
        }
    },
    {
        'api': {
            'port': 1111
        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {}
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost"
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "port": 1111
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111,
            "name": "database"
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111,
            "name": "database",
            "user": "username"
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111,
            "name": "database",
            "user": "username"
        },
        "services": {}
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111,
            "name": "database",
            "user": "username"
        },
        "services": {
            "midpoint": {}
        }
    },
    {
        "api": {
            "host": "localhost",
            "port": 1111
        },
        "db": {
            "host": "localhost",
            "port": 1111,
            "name": "database",
            "user": "username"
        },
        "services": {
            "midpoint": {
                "host": "localhost"
            }
        }
    }
]

@ddt.ddt
class ConfigTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        if os.path.isfile(TEST_CONFIG):
            os.remove(TEST_CONFIG)
        super().setUp()

    def create_config_file(self, cfg):
        with open(TEST_CONFIG, 'w+') as f:
            f.write(json.dumps(cfg))

    def test_read_config_from_invalid_path_expect_throw(self):
        self.assertRaises(error.ConfigError, lambda: config.Config("invalid_path"))
    
    @ddt.data(*CORRUPTED_CONFIGS)
    def test_read_corrupted_config_expect_throw(self,cfg):
        self.create_config_file(cfg)
        self.assertRaises(error.ConfigError, lambda: config.Config(TEST_CONFIG))

    def test_read_valid_config_expect_correct_fields(self):
        raw_cfg = {
            "api": {
                "host": "localhost",
                "port": 1111
            },
            "db": {
                "host": "localhost",
                "port": 1111,
                "name": "database",
                "user": "username"
            },
            "services": {
                "midpoint": {
                    "host": "localhost",
                    "port": 1111
                }
            }
        }

        self.create_config_file(raw_cfg)
        cfg = config.Config(TEST_CONFIG)

        self.assertEqual(cfg.api.host, raw_cfg['api']['host'])
        self.assertEqual(cfg.api.port, raw_cfg['api']['port'])
        self.assertEqual(cfg.db.host, raw_cfg['db']['host'])
        self.assertEqual(cfg.db.port, raw_cfg['db']['port'])
        self.assertEqual(cfg.db.name, raw_cfg['db']['name'])
        self.assertEqual(cfg.db.user, raw_cfg['db']['user'])
        self.assertEqual(cfg.midpoint.host, raw_cfg['services']['midpoint']['host'])
        self.assertEqual(cfg.midpoint.port, raw_cfg['services']['midpoint']['port'])
    
    def test_read_config_without_api_key_expect_default_api_values(self):
        raw_cfg = {
            "db": {
                "host": "localhost",
                "port": 1111,
                "name": "database",
                "user": "username"
            },
            "services": {
                "midpoint": {
                    "host": "localhost",
                    "port": 1111
                }
            }
        }
        self.create_config_file(raw_cfg)
        cfg = config.Config(TEST_CONFIG)
        self.assertEqual(cfg.api.host, '0.0.0.0')
        self.assertEqual(cfg.api.port, 7775)
        self.assertEqual(cfg.db.host, raw_cfg['db']['host'])
        self.assertEqual(cfg.db.port, raw_cfg['db']['port'])
        self.assertEqual(cfg.db.name, raw_cfg['db']['name'])
        self.assertEqual(cfg.db.user, raw_cfg['db']['user'])
        self.assertEqual(cfg.midpoint.host, raw_cfg['services']['midpoint']['host'])
        self.assertEqual(cfg.midpoint.port, raw_cfg['services']['midpoint']['port'])



    