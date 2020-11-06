from .midpoint_proxy import setup_midpoint_proxy
from core.log import get_logger

log = get_logger("proxy")


def setup_proxies(app, cfg):
    log.info("Setting up proxies")
    midpoint_blueprints = setup_midpoint_proxy(cfg.midpoint)
    for midpoint_blueprint in midpoint_blueprints:
        app.blueprint(midpoint_blueprint)
