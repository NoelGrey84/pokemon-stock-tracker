from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class ProductStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    PICKUP_AVAILABLE = "PICKUP_AVAILABLE"
    PREORDER = "PREORDER"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"

@dataclass
class ProductObservation:
    store: str
    product_name: str
    url: str
    status: ProductStatus
    price: Optional[float] = None
    currency: str = "EUR"
    purchase_online: bool = False
    pickup: bool = False
    reservation: bool = False
    evidence: list[str] = field(default_factory=list)
    http_status: Optional[int] = None
    error: Optional[str] = None

    @property
    def available(self) -> bool:
        return self.status in {ProductStatus.IN_STOCK, ProductStatus.PICKUP_AVAILABLE, ProductStatus.PREORDER}

    def relevant_modes(self) -> set[str]:
        return {m for m, enabled in (
            ("online", self.purchase_online),
            ("pickup", self.pickup),
            ("reservation", self.reservation),
        ) if enabled}
