# SPDX-License-Identifier: Apache-2.0
"""Known-answer vectors plus exact Fraction rounding cross-check."""
from fractions import Fraction
import unittest

from edge_npu_reference import gemm_int8, rescale_int32, round_shift_even


class ReferenceTests(unittest.TestCase):
    def test_signed_endpoints(self):
        self.assertEqual(gemm_int8([[-128, 127, -1]], [[-128], [127], [1]]),
                         [[32512]])

    def test_non_square_tail_and_bias(self):
        a = [[1, -2, 3, 0, 4], [-1, 0, 2, 5, -3]]
        b = [[1, 2, -1], [0, 1, 2], [-1, 0, 3], [2, -2, 1], [1, 1, 0]]
        self.assertEqual(gemm_int8(a, b, [1, -1, 2]),
                         [[3, 3, 6], [5, -16, 14]])

    def test_bias_applied_once(self):
        accum = gemm_int8([[2]], [[3]], [4])[0]
        self.assertEqual(rescale_int32(accum, [1], [0]), [10])

    def test_matrix_shape_errors(self):
        for a, b in [([], [[1]]), ([[]], [[1]]), ([[1, 2]], [[1]]),
                     ([[1], [1, 2]], [[1]]), ([[1]], [[1], [2]]),
                     ([[1, 2]], [[1, 2], [3]])]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                gemm_int8(a, b)

    def test_integer_and_operand_bounds(self):
        for value in [-129, 128, True, 1.0]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                gemm_int8([[value]], [[1]])

    def test_bias_length_and_overflow(self):
        for bias in [[], [1, 2], [2**31], [2**31-1]]:
            with self.subTest(bias=bias), self.assertRaises(ValueError):
                gemm_int8([[1]], [[1]], bias)

    def test_positive_negative_halfway(self):
        self.assertEqual([round_shift_even(x, 1) for x in [1, 3, 5, 7]],
                         [0, 2, 2, 4])
        self.assertEqual([round_shift_even(x, 1) for x in [-1, -3, -5, -7]],
                         [0, -2, -2, -4])

    def test_rounding_against_exact_rational(self):
        # Independent Python Fraction.__round__, no float or DUT result.
        for shift in range(9):
            for value in range(-257, 258):
                self.assertEqual(round_shift_even(value, shift),
                                 round(Fraction(value, 2**shift)))

    def test_shift_and_int64_limits(self):
        self.assertEqual(round_shift_even(-(2**63), 31), -(2**32))
        self.assertEqual(round_shift_even(2**63-1, 31), 2**32)
        for value, shift in [(0, -1), (0, 32), (0, True), (2**63, 0)]:
            with self.subTest(value=value, shift=shift), self.assertRaises(ValueError):
                round_shift_even(value, shift)

    def test_per_channel_scale(self):
        self.assertEqual(rescale_int32([3, -5, 20], [1, 3, -2], [1, 1, 2], 4),
                         [6, -4, -6])

    def test_saturation_and_quantized_relu(self):
        self.assertEqual(rescale_int32([2**31-1, -(2**31)], [2**31-1], [0]),
                         [127, -128])
        self.assertEqual(rescale_int32([-20, 0, 40], [1], [0], 5, 5, 17),
                         [5, 5, 17])

    def test_scale_and_clamp_errors(self):
        for args in [([], [1], [0]), ([1, 2], [1, 2, 3], [0, 0, 0]),
                     ([1], [1], []), ([1], [2**31], [0])]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                rescale_int32(*args)
        for kwargs in [dict(zero_point=128), dict(clamp_min=3, clamp_max=2),
                       dict(clamp_max=128)]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                rescale_int32([0], [1], [0], **kwargs)


if __name__ == "__main__":
    unittest.main()
