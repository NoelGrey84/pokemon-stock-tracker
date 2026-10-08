from __future__ import annotations
import json
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AppConfig:
    product_name: str
    postal_code: str
    city: str
    interval_minutes: int
    max_price: float | None
    products: dict[str, list[str]]
    search_urls: dict[str, list[str]]

def load_config(path: str = "config.json") -> AppConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return AppConfig(
        product_name=data["product_name"],
        postal_code=data.get("postal_code", ""),
        city=data.get("city", ""),
        interval_minutes=int(data.get("interval_minutes", 5)),
        max_price=data.get("max_price"),
        products={k: list(v) for k, v in data.get("products", {}).items()},
        search_urls={k: list(v) for k, v in data.get("search_urls", {}).items()},
    )

def discord_webhook_url() -> str:
    value = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not value:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured")
    return value
