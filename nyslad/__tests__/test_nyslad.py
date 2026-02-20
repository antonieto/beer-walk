import os
import tempfile
import unittest
from datetime import date

from models import Coordinate, LiquorLicense
from nyslad.nyslad import read_nyslad_dataset, _parse_date, _parse_georeference

HEADER = (
    '"License Permit ID","Premises County","Type","Class","Description",'
    '"LegalName","DBA","Actual Address Of Premises",'
    '"Additional Address Information","City","State Name","Zip Code",'
    '"Original Issue Date","Last Issue Date","Effective Date","Expiration Date",'
    '"Parent License ID","Legacy Serial Number","AKA Address","Georeference"'
)

FULL_ROW = (
    '"0002-23-113553","New York","1","0002","Wholesale Beer",'
    '"SUNDAY BEER CO","The Sunday Spot","1027 GRAND ST",'
    '"STE 410","NEW YORK","New York","10001",'
    '"07/18/2025","07/18/2025","07/18/2025","06/30/2026",'
    '"PARENT-001","1301987","1027 GRAND","POINT (-73.93417 40.71354)"'
)

MINIMAL_ROW = (
    '"0011-23-223824","Kings","1","0011","Importer",'
    '"SLAMMIT WHISKY INC",,"115 CONTINUUM DR",'
    ',"BROOKLYN","New York","13202",'
    '"05/05/2023","05/05/2023","05/05/2023","04/30/2026",'
    ',"2234730",,'
)


def _write_csv(rows: list[str]) -> str:
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    )
    f.write(HEADER + "\n")
    for row in rows:
        f.write(row + "\n")
    f.close()
    return f.name


class TestParseDate(unittest.TestCase):
    def test_valid_date(self):
        self.assertEqual(_parse_date("07/18/2025"), date(2025, 7, 18))

    def test_empty_string(self):
        self.assertIsNone(_parse_date(""))


class TestParseGeoreference(unittest.TestCase):
    def test_valid_point(self):
        coord = _parse_georeference("POINT (-73.93417 40.71354)")
        self.assertIsNotNone(coord)
        self.assertAlmostEqual(coord.x, 40.71354)
        self.assertAlmostEqual(coord.y, -73.93417)

    def test_empty_string(self):
        self.assertIsNone(_parse_georeference(""))

    def test_invalid_format(self):
        self.assertIsNone(_parse_georeference("not a point"))


class TestReadNysladDataset(unittest.TestCase):
    def test_full_row(self):
        path = _write_csv([FULL_ROW])
        try:
            results = read_nyslad_dataset(csv_path=path)
            self.assertEqual(len(results), 1)
            lic = results[0]
            self.assertEqual(lic.license_permit_id, "0002-23-113553")
            self.assertEqual(lic.premises_county, "New York")
            self.assertEqual(lic.license_type, 1)
            self.assertEqual(lic.license_class, "0002")
            self.assertEqual(lic.description, "Wholesale Beer")
            self.assertEqual(lic.legal_name, "SUNDAY BEER CO")
            self.assertEqual(lic.dba, "The Sunday Spot")
            self.assertEqual(lic.address, "1027 GRAND ST")
            self.assertEqual(lic.additional_address, "STE 410")
            self.assertEqual(lic.city, "NEW YORK")
            self.assertEqual(lic.state, "New York")
            self.assertEqual(lic.zip_code, "10001")
            self.assertEqual(lic.original_issue_date, date(2025, 7, 18))
            self.assertEqual(lic.expiration_date, date(2026, 6, 30))
            self.assertEqual(lic.parent_license_id, "PARENT-001")
            self.assertEqual(lic.legacy_serial_number, "1301987")
            self.assertEqual(lic.aka_address, "1027 GRAND")
            self.assertIsNotNone(lic.georeference)
            self.assertAlmostEqual(lic.georeference.x, 40.71354)
            self.assertAlmostEqual(lic.georeference.y, -73.93417)
        finally:
            os.unlink(path)

    def test_minimal_row_optional_fields_are_none(self):
        path = _write_csv([MINIMAL_ROW])
        try:
            results = read_nyslad_dataset(csv_path=path)
            self.assertEqual(len(results), 1)
            lic = results[0]
            self.assertIsNone(lic.dba)
            self.assertIsNone(lic.additional_address)
            self.assertIsNone(lic.parent_license_id)
            self.assertIsNone(lic.aka_address)
            self.assertIsNone(lic.georeference)
        finally:
            os.unlink(path)

    def test_multiple_rows(self):
        path = _write_csv([FULL_ROW, MINIMAL_ROW])
        try:
            results = read_nyslad_dataset(csv_path=path)
            self.assertEqual(len(results), 2)
        finally:
            os.unlink(path)

    def test_filter_fn(self):
        path = _write_csv([FULL_ROW, MINIMAL_ROW])
        try:
            results = read_nyslad_dataset(
                csv_path=path,
                filter_fn=lambda lic: lic.premises_county == "New York",
            )
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].premises_county, "New York")
        finally:
            os.unlink(path)

    def test_empty_csv(self):
        path = _write_csv([])
        try:
            results = read_nyslad_dataset(csv_path=path)
            self.assertEqual(len(results), 0)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
