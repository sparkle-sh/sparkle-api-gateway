from .midpoint_proxy import setup_midpoint_proxy


def setup_proxies(app, cfg):
    app.blueprint(setup_midpoint_proxy(cfg.midpoint))
