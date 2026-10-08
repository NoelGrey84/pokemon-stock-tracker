from __future__ import annotations
import requests
from .models import ProductObservation

def format_price(observation: ProductObservation) -> str:
    return "No disponible" if observation.price is None else f"{observation.price:.2f} €".replace(".", ",")

def build_message(observation: ProductObservation) -> str:
    labels = {
        "IN_STOCK": "Disponible para compra",
        "PICKUP_AVAILABLE": "Recogida disponible",
        "PREORDER": "Preventa / reserva disponible",
    }
    modes = []
    if observation.purchase_online: modes.append("compra online")
    if observation.pickup: modes.append("recogida")
    if observation.reservation: modes.append("reserva")
    modality = ", ".join(modes) if modes else "No determinada"
    return (
        "🚨 **POKÉMON DISPONIBLE**\n\n"
        f"**Tienda:** {observation.store}\n"
        f"**Producto:** {observation.product_name}\n"
        f"**Estado:** {labels.get(observation.status.value, observation.status.value)}\n"
        f"**Precio:** {format_price(observation)}\n"
        f"**Modalidad:** {modality}\n\n"
        f"🔗 **Comprar / reservar:** {observation.url}"
    )

def send_discord(webhook_url: str, observation: ProductObservation, timeout: int = 10) -> None:
    response = requests.post(
        webhook_url,
        json={"content": build_message(observation), "allowed_mentions": {"parse": []}},
        timeout=timeout,
    )
    response.raise_for_status()
