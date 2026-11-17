import random
import unittest

from calculator import FORMULAS, generate_values, summarize, transform_values


class CalculatorTests(unittest.TestCase):
    def test_generator_creates_fifty_values_in_range(self):
        values = generate_values(rng=random.Random(7))

        self.assertEqual(len(values), 50)
        self.assertTrue(all(10 <= value <= 100 for value in values))

    def test_summary_includes_statistics_and_sorted_values(self):
        result = summarize([8, 2, 5, 1])

        self.assertEqual(result["minimum"], 1)
        self.assertEqual(result["maximum"], 8)
        self.assertEqual(result["average"], 4)
        self.assertEqual(result["median"], 3.5)
        self.assertEqual(result["ordered"], (1, 2, 5, 8))

    def test_each_formula_transforms_every_value(self):
        values = [20, 40]

        self.assertEqual(transform_values(values, "x × 1.25 + 10"), [35, 60])
        self.assertEqual(transform_values(values, "x × 0.80"), [16, 32])
        self.assertEqual(transform_values(values, "x + 15"), [35, 55])
        self.assertEqual(len(FORMULAS), 3)

    def test_empty_input_and_unknown_formula_are_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])
        with self.assertRaises(ValueError):
            transform_values([1], "x / 0")


if __name__ == "__main__":
    unittest.main()
