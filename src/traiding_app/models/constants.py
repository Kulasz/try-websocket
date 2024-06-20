"""Constants"""

from enum import StrEnum


class Status(StrEnum):
    """Available statuses"""

    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELLED"
