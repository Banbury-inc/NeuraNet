# test_example.py
import unittest
from src import generate


class TestExample(unittest.TestCase):
    def test_generate(self):
        self.assertEqual(src.generate(2, 3), 5)


if __name__ == "__main__":
    unittest.main()
