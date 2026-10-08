from __future__ import annotations
import json
from pathlib import Path
from typing import Any

AVAILABLE = {"IN_STOCK", "PICKUP_AVAILABLE", "PREORDER"}

class StateStore:
    def __init__(self, path: str = "state.json") -> None:
        self.path = Path(path)
        self.data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists(): return {"stores": {}}
        try: return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError): return {"stores": {}}

    def get(self, key: str) -> dict[str, Any] | None:
        return self.data.get("stores", {}).get(key)

    def should_notify(self, key: str, current_status: str, modes: set[str]) -> bool:
        previous = self.get(key)
        if not previous:
            return current_status in AVAILABLE
        old_status = previous.get("status")
        old_modes = set(previous.get("modes", []))
        if current_status in AVAILABLE and old_status in {"OUT_OF_STOCK", "UNKNOWN", "BLOCKED"}:
            return True
        if current_status in AVAILABLE and old_status in AVAILABLE and current_status != old_status:
            return True
        return current_status in AVAILABLE and modes > old_modes

    def update(self, key: str, status: str, modes: set[str]) -> bool:
        new = {"status": status, "modes": sorted(modes)}
        changed = self.get(key) != new
        self.data.setdefault("stores", {})[key] = new
        return changed

    def save_if_changed(self, changed: bool) -> None:
        if changed:
            self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
