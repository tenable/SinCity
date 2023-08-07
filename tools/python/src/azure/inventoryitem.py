from dataclasses import dataclass
from typing import Optional


@dataclass
class InventoryItem:
    name: Optional[str] = None
    operating_system: Optional[str] = None
    role: Optional[str] = None
    ip: Optional[str] = None

