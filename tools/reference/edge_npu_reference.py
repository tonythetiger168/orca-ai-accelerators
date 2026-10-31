# SPDX-License-Identifier: Apache-2.0
"""Edge INT8 arithmetic oracle; no device, driver, cycles or ABI emulation."""


def signed(value, bits, name="value"):
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    if not -(1 << (bits - 1)) <= value < (1 << (bits - 1)):
        raise ValueError(f"{name} exceeds signed {bits}-bit range")
    return value


def round_shift_even(value, shift):
    """Exact signed division by 2**shift, nearest with ties to even."""
    signed(value, 64)
    if type(shift) is not int or not 0 <= shift <= 31:
        raise ValueError("right_shift must be 0..31")
    quotient, remainder = divmod(abs(value), 1 << shift)
    denominator = 1 << shift
    if 2 * remainder > denominator or (
        2 * remainder == denominator and quotient % 2
    ):
        quotient += 1
    return -quotient if value < 0 else quotient


def gemm_int8(a, b, bias=None):
    """Row-major A[M,K] @ B[K,N], zero points zero, optional bias once.

    Python exact integers are the oracle; out-of-range INT32 outputs are rejected,
    never wrapped. Hardware intermediate overflow policy remains a separate gate.
    """
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("empty matrix")
    k, n = len(a[0]), len(b[0])
    if len(b) != k or any(len(row) != k for row in a):
        raise ValueError("invalid A or K dimension")
    if any(len(row) != n for row in b):
        raise ValueError("ragged B")
    for row in a + b:
        for value in row:
            signed(value, 8, "operand")
    bias = [0] * n if bias is None else bias
    if len(bias) != n:
        raise ValueError("bias length must match output channels")
    for value in bias:
        signed(value, 32, "bias")
    result = []
    for row in a:
        output = []
        for channel in range(n):
            acc = bias[channel]
            for index in range(k):
                acc += row[index] * b[index][channel]
            output.append(signed(acc, 32, "accumulator output"))
        result.append(output)
    return result


def rescale_int32(values, multipliers, shifts, zero_point=0,
                  clamp_min=-128, clamp_max=127):
    """One output row, with one scale per tensor or per output channel.

    Bias is already included by GEMM; it is not added again here. Clamp bounds
    are quantized integers (e.g. ReLU lower bound = output zero point).
    """
    if not values:
        raise ValueError("empty values")
    signed(zero_point, 8, "output zero point")
    signed(clamp_min, 8, "clamp_min")
    signed(clamp_max, 8, "clamp_max")
    if clamp_min > clamp_max:
        raise ValueError("reversed clamp")
    if len(multipliers) != len(shifts) or len(shifts) not in (1, len(values)):
        raise ValueError("scale count must be 1 or channel count")
    result = []
    for channel, value in enumerate(values):
        signed(value, 32, "accumulator")
        index = 0 if len(shifts) == 1 else channel
        multiplier = signed(multipliers[index], 32, "multiplier")
        product = signed(value * multiplier, 64, "product")
        scaled = round_shift_even(product, shifts[index]) + zero_point
        result.append(min(clamp_max, max(clamp_min, scaled)))
    return result
