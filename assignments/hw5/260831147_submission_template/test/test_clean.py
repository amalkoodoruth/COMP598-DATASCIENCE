import unittest
from pathlib import Path
import os, sys
from src.clean import valid_json,validate_title, check_iso, check_author, cast_int, get_tags
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
        dr = os.path.dirname(__file__)
        fixture1_path = os.path.join(dr, "fixtures", "test_1.json")
        fixture2_path = os.path.join(dr, "fixtures", "test_2.json")
        self.fixture3_path = os.path.join(dr, "fixtures", "test_3.json")
        fixture4_path = os.path.join(dr, "fixtures", "test_4.json")
        fixture5_path = os.path.join(dr, "fixtures", "test_5.json")
        fixture6_path = os.path.join(dr, "fixtures", "test_6.json")
        with open(fixture1_path) as f:
            record = f.readline()
            self.fixture1 = json.loads(record)
        with open(fixture2_path) as f:
            record = f.readline()
            self.fixture2 = json.loads(record)
        # with open(fixture3_path) as f:
        #     record = f.readline()
        #     self.fixture3 = json.loads(record)
        with open(fixture4_path) as f:
            record = f.readline()
            self.fixture4 = json.loads(record)
        with open(fixture5_path) as f:
            record = f.readline()
            self.fixture5 = json.loads(record)
        with open(fixture6_path) as f:
            record = f.readline()
            self.fixture6 = json.loads(record)


    def test_title(self):
        # Just an idea for a test; write your implementation
        # print(self.fixture1)
        self.assertEqual(validate_title(self.fixture1), False)

    def test_iso(self):
        self.assertEqual(check_iso(self.fixture2), False)

    def test_valid(self):
        with open(self.fixture3_path) as f:
            record = f.readline()
        self.assertEqual(valid_json(record), False)

    def test_author(self):
        self.assertEqual(check_author(self.fixture4), False)

    def test_cast_int(self):
        self.assertEqual(cast_int(self.fixture5), False)

    def test_tags(self):
        self.assertEqual(len(get_tags(self.fixture6)),4)
    
if __name__ == '__main__':
    unittest.main()