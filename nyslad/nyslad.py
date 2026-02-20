import csv
import os
import re
from datetime import date
from typing import Callable, List, Optional

from models import Coordinate, LiquorLicense

DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "Current_Liquor_Authority_Active_Licenses_20260219.csv",
)


def _parse_date(value: str) -> Optional[date]:
    if not value:
        return None
    month, day, year = value.split("/")
    return date(int(year), int(month), int(day))


def _parse_georeference(value: str) -> Optional[Coordinate]:
    if not value:
        return None
    match = re.match(r"POINT \(([^ ]+) ([^ ]+)\)", value)
    if not match:
        return None
    lng, lat = float(match.group(1)), float(match.group(2))
    return Coordinate(x=lat, y=lng)


def _optional(value: str) -> Optional[str]:
    return value if value else None


def read_nyslad_dataset(
    csv_path: str = DEFAULT_CSV_PATH,
    filter_fn: Optional[Callable[[LiquorLicense], bool]] = None,
) -> List[LiquorLicense]:
    licenses: List[LiquorLicense] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            license = LiquorLicense(
                license_permit_id=row["License Permit ID"],
                premises_county=row["Premises County"],
                license_type=int(row["Type"]),
                license_class=row["Class"],
                description=row["Description"],
                legal_name=row["LegalName"],
                dba=_optional(row["DBA"]),
                address=row["Actual Address Of Premises"],
                additional_address=_optional(row["Additional Address Information"]),
                city=row["City"],
                state=row["State Name"],
                zip_code=row["Zip Code"],
                original_issue_date=_parse_date(row["Original Issue Date"]),
                last_issue_date=_parse_date(row["Last Issue Date"]),
                effective_date=_parse_date(row["Effective Date"]),
                expiration_date=_parse_date(row["Expiration Date"]),
                parent_license_id=_optional(row["Parent License ID"]),
                legacy_serial_number=_optional(row["Legacy Serial Number"]),
                aka_address=_optional(row["AKA Address"]),
                georeference=_parse_georeference(row["Georeference"]),
            )
            if filter_fn is None or filter_fn(license):
                licenses.append(license)

    return licenses
