import unittest
from unittest.mock import patch

import pypokedex


class HelperTests(unittest.TestCase):
    def test_slug_and_roman_generation(self):
        from pypokedex.client import _slug, _roman
        self.assertEqual(_slug("Mr. Mime"), "mr-mime")
        self.assertEqual(_roman(4), "iv")
        self.assertEqual(_roman(9), "ix")

    def test_random_bounds(self):
        with self.assertRaises(ValueError):
            pypokedex.random_pokemon(10, 2)
        with self.assertRaises(ValueError):
            pypokedex.random_pokemon(0, 2)

    def test_search_validation(self):
        with self.assertRaises(ValueError):
            pypokedex.search_pokemon(" ")
        with self.assertRaises(ValueError):
            pypokedex.search_pokemon("pikachu", 0)


if __name__ == "__main__":
    unittest.main()
