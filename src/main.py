from __future__ import annotations

import logging

from .config import discord_webhook_url, load_config
from .discord_notifier import send_discord
from .models import ProductObservation
from .state import StateStore
from .stores import CarrefourAdapter, ElCorteInglesAdapter, HipercorAdapter

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOG = logging.getLogger(__name__)

ADAPTERS = {
    "elcorteingles": ElCorteInglesAdapter,
    "hipercor": HipercorAdapter,
    "carrefour": CarrefourAdapter,
}


def check_store(store_key: str, urls: list[str], config) -> list[ProductObservation]:
    adapter = ADAPTERS[store_key](config.product_name, config.postal_code, config.city)
    results = []
    for url in dict.fromkeys(urls):
        LOG.info("Checking %s...", adapter.name)
        observation = adapter.check(url)
        if observation.error:
            LOG.warning("%s: %s", adapter.name, observation.error)
        LOG.info("Product status: %s", observation.status.value)
        if observation.price is not None:
            LOG.info("Price: %.2f EUR", observation.price)
        results.append(observation)
    return results


def run() -> int:
    config = load_config()
    state = StateStore()
    webhook = None
    changed = False

    for store_key, urls in config.products.items():
        if store_key not in ADAPTERS:
            LOG.warning("Unknown store configured: %s", store_key)
            continue
        if not urls:
            LOG.info("Skipping %s: no product URL configured", store_key)
            continue

        for observation in check_store(store_key, urls, config):
            key = f"{store_key}:{observation.url}"
            notify = state.should_notify(
                key, observation.status.value, observation.relevant_modes()
            )
            if notify:
                try:
                    if webhook is None:
                        webhook = discord_webhook_url()
                    send_discord(webhook, observation)
                    LOG.info("Discord notification sent")
                except Exception as exc:
                    LOG.error("Could not send Discord notification: %s", exc)
                    continue

            changed = state.update(
                key, observation.status.value, observation.relevant_modes()
            ) or changed

    state.save_if_changed(changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
