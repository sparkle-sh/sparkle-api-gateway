import json
import os
import dataclasses
from core import error


API_DEFAULT_HOST = "0.0.0.0"
API_DEFAULT_PORT = 7775


@dataclasses.dataclass
class NetAddress(object):
    host: str
    port: int


@dataclasses.dataclass
class DbData(object):
    host: str
    port: int
    name: str
    user: str


def parse_dataclass(payload, keywords, Model):
    for keyword in keywords:
        if keyword not in payload:
            raise error.ConfigError("Config file is corrupted")
    args = (payload.get(keyword) for keyword in keywords)
    return Model(*args)


def parse_net_address(address) -> NetAddress:
    required_keywords = ['host', 'port']
    return parse_dataclass(address, required_keywords, NetAddress)


def parse_db_data(data) -> DbData:
    required_keywords = ['host', 'port', 'name', 'user']
    return parse_dataclass(data, required_keywords, DbData)


class Config(object):
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise error.ConfigError(f"Could not find configuration file: {path}")

        cfg = {}
        with open(path, 'r') as f:
            cfg = json.loads(f.read())
        self.load_api(cfg)
        self.load_db(cfg)
        self.load_services(cfg)

    def load_api(self, cfg):
        if 'api' not in cfg:
            cfg['api'] = {}

        self.api = NetAddress(cfg['api'].get('host', API_DEFAULT_HOST), cfg['api'].get('port', API_DEFAULT_PORT))
    
    def load_db(self, cfg):
        if 'db' not in cfg:
            raise error.ConfigError("Config file is corrupted")
        
        self.db = parse_db_data(cfg.get('db'))

    def load_services(self, cfg):
        if 'services' not in cfg:
            raise error.ConfigError("Config file is corrupted")
        
        services = cfg.get("services")

        if 'midpoint' not in services:
            raise error.ConfigError("Config file is corrupted")

        self.midpoint = parse_net_address(services.get('midpoint')) 

