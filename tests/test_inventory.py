import json
import os
import tempfile
import unittest

import inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "inv.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_device_appends_item(self):
        items = inventory.add_device([], "Router", "SN-1")
        self.assertEqual(items, [{"name": "Router", "serial": "SN-1"}])

    def test_serial_number_is_unique(self):
        items = inventory.add_device([], "Router", "SN-1")
        with self.assertRaises(ValueError):
            inventory.add_device(items, "Switch", "SN-1")
        self.assertEqual(len(items), 1)

    def test_serial_uniqueness_ignores_case_and_spaces(self):
        items = inventory.add_device([], "Router", "sn-1")
        with self.assertRaises(ValueError):
            inventory.add_device(items, "Switch", "  SN-1 ")

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            inventory.add_device([], "   ", "SN-1")

    def test_blank_serial_is_rejected(self):
        with self.assertRaises(ValueError):
            inventory.add_device([], "Router", "")

    def test_serial_is_normalized_to_upper_case(self):
        items = inventory.add_device([], "Router", "ab-12")
        self.assertEqual(items[0]["serial"], "AB-12")

    def test_find_device_returns_item(self):
        items = inventory.add_device([], "Router", "SN-1")
        self.assertEqual(inventory.find_device(items, "sn-1")["name"], "Router")

    def test_find_device_returns_none_for_unknown(self):
        self.assertIsNone(inventory.find_device([], "SN-404"))

    def test_load_missing_file_returns_empty_list(self):
        self.assertEqual(inventory.load_inventory(self.path), [])

    def test_save_and_load_roundtrip(self):
        data = [{"name": "Принтер", "serial": "P-7"}]
        inventory.save_inventory(self.path, data)
        self.assertEqual(inventory.load_inventory(self.path), data)

    def test_load_rejects_non_list_json(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"a": 1}, f)
        with self.assertRaises(ValueError):
            inventory.load_inventory(self.path)

    def test_main_add_and_duplicate_exit_codes(self):
        base = ["--file", self.path, "add", "--name", "Router", "--serial", "SN-1"]
        self.assertEqual(inventory.main(base), 0)
        self.assertEqual(inventory.main(base), 2)

    def test_main_find_unknown_returns_1(self):
        self.assertEqual(
            inventory.main(["--file", self.path, "find", "--serial", "X"]), 1)


if __name__ == "__main__":
    unittest.main()
