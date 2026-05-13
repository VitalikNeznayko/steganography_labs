import unittest
from pvd import clamp_value, get_interval
import math


class TestPVD(unittest.TestCase):

    def test_get_interval(self):
        print("\n=== TEST get_interval ===")

        cases = [5, 10, 20, 50, 100, 200]

        for d in cases:
            result = get_interval(d)
            print(f"d={d} -> interval={result}")
            self.assertIsNotNone(result)

    def test_clamp(self):
        print("\n=== TEST clamp ===")

        cases = [-10, 300, 128]

        for v in cases:
            result = clamp_value(v)
            print(f"clamp({v}) -> {result}")
            self.assertTrue(0 <= result <= 255)

    def test_n_bits(self):
        print("\n=== TEST n_bits ===")

        ranges = [(0,7), (8,15), (16,31), (32,63), (64,127), (128,255)]

        for l, u in ranges:
            n = int(math.log2(u - l + 1))
            print(f"range=({l},{u}) -> n={n}")
            self.assertGreater(n, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)