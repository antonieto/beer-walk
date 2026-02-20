import dataclasses
from datetime import date
from typing import Optional


@dataclasses.dataclass
class Coordinate:
    x: float
    y: float


@dataclasses.dataclass
class LiquorLicense:
    license_permit_id: str
    premises_county: str
    license_type: int
    license_class: str
    description: str
    legal_name: str
    dba: Optional[str]
    address: str
    additional_address: Optional[str]
    city: str
    state: str
    zip_code: str
    original_issue_date: Optional[date]
    last_issue_date: Optional[date]
    effective_date: Optional[date]
    expiration_date: Optional[date]
    parent_license_id: Optional[str]
    legacy_serial_number: Optional[str]
    aka_address: Optional[str]
    georeference: Optional[Coordinate]
