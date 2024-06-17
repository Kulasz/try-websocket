"""Models for order"""

from typing import Dict, Optional

from pydantic import BaseModel


class Order(BaseModel):
    """Model for basic order"""

    id: Optional[str] = None
    status: Optional[str] = "PENDING"
    details: Optional[Dict] = {}
