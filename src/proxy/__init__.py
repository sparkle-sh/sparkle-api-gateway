from .midpoint_proxy import setup_midpoint_proxy


async def setup_proxies(app, cfg):
    app.blueprint(await setup_midpoint_proxy(cfg.midpoint))
