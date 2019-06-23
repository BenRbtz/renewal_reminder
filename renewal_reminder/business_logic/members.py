from dataclasses import dataclass
from datetime import date


@dataclass
class Member:
    name: str
    grade: str
    licence_expiry: date
