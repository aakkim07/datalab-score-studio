import random
import unittest

from calculator import calculate, generate_values, summarize, transform_values


class CalculatorTests(unittest.TestCase):
    def test_generator_creates_fifty_values_in_range(self):
        values = generate_values(rng=random.Random(7))

        self.assertEqual(len(values), 50)
        self.assertTrue(all(10 <= value <= 100 for value in values))

    def test_summary_calculates_statistics_and_sorts(self):
        result = summarize([8, 2, 5, 1])

        self.assertEqual(result["minimum"], 1)
        self.assertEqual(result["maximum"], 8)
        self.assertEqual(result["average"], 4)
        self.assertEqual(result["ordered"], (1, 2, 5, 8))

    def test_formula_works_for_input_and_array(self):
        self.assertEqual(calculate(10), 30)
        self.assertEqual(calculate(2.5), 15)
        self.assertEqual(transform_values([20, 40]), [50, 90])

    def test_invalid_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])
        with self.assertRaises(ValueError):
            generate_values(0)


if __name__ == "__main__":
    unittest.main()
