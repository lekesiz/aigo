"""
Tests for AIGo Standard Library - Math Module

Tests all mathematical functions and constants.
"""

import pytest
import math as py_math
from src.aigo.stdlib.math import MathModule, PI, E, TAU


class TestMathConstants:
    """Test mathematical constants."""

    def test_pi_constant(self):
        """Test PI constant value."""
        assert PI == py_math.pi
        assert MathModule.pi == py_math.pi

    def test_e_constant(self):
        """Test E constant value."""
        assert E == py_math.e
        assert MathModule.e == py_math.e

    def test_tau_constant(self):
        """Test TAU constant value."""
        assert TAU == py_math.tau
        assert MathModule.tau == py_math.tau


class TestBasicMathFunctions:
    """Test basic mathematical functions."""

    def test_abs_positive(self):
        """Test absolute value of positive number."""
        assert MathModule.abs(42) == 42
        assert MathModule.abs(3.14) == 3.14

    def test_abs_negative(self):
        """Test absolute value of negative number."""
        assert MathModule.abs(-42) == 42
        assert MathModule.abs(-3.14) == 3.14

    def test_abs_zero(self):
        """Test absolute value of zero."""
        assert MathModule.abs(0) == 0
        assert MathModule.abs(0.0) == 0.0

    def test_sqrt_perfect_square(self):
        """Test square root of perfect squares."""
        assert MathModule.sqrt(4.0) == 2.0
        assert MathModule.sqrt(9.0) == 3.0
        assert MathModule.sqrt(16.0) == 4.0

    def test_sqrt_non_perfect_square(self):
        """Test square root of non-perfect squares."""
        assert abs(MathModule.sqrt(2.0) - 1.41421356) < 0.00001
        assert abs(MathModule.sqrt(5.0) - 2.23606798) < 0.00001

    def test_sqrt_negative_raises_error(self):
        """Test that square root of negative raises error."""
        with pytest.raises(ValueError):
            MathModule.sqrt(-1.0)

    def test_pow_positive_exponent(self):
        """Test power with positive exponent."""
        assert MathModule.pow(2.0, 3.0) == 8.0
        assert MathModule.pow(5.0, 2.0) == 25.0

    def test_pow_negative_exponent(self):
        """Test power with negative exponent."""
        assert abs(MathModule.pow(2.0, -1.0) - 0.5) < 0.00001
        assert abs(MathModule.pow(4.0, -2.0) - 0.0625) < 0.00001

    def test_pow_zero_exponent(self):
        """Test power with zero exponent."""
        assert MathModule.pow(5.0, 0.0) == 1.0
        assert MathModule.pow(100.0, 0.0) == 1.0


class TestLogarithmFunctions:
    """Test logarithm functions."""

    def test_log_natural(self):
        """Test natural logarithm."""
        assert abs(MathModule.log(E) - 1.0) < 0.00001
        assert abs(MathModule.log(1.0) - 0.0) < 0.00001

    def test_log_with_base(self):
        """Test logarithm with custom base."""
        assert abs(MathModule.log(8.0, 2.0) - 3.0) < 0.00001
        assert abs(MathModule.log(1000.0, 10.0) - 3.0) < 0.00001

    def test_log_negative_raises_error(self):
        """Test that log of negative raises error."""
        with pytest.raises(ValueError):
            MathModule.log(-1.0)

    def test_log10(self):
        """Test base-10 logarithm."""
        assert abs(MathModule.log10(10.0) - 1.0) < 0.00001
        assert abs(MathModule.log10(100.0) - 2.0) < 0.00001

    def test_log2(self):
        """Test base-2 logarithm."""
        assert abs(MathModule.log2(2.0) - 1.0) < 0.00001
        assert abs(MathModule.log2(8.0) - 3.0) < 0.00001


class TestTrigonometricFunctions:
    """Test trigonometric functions."""

    def test_sin(self):
        """Test sine function."""
        assert abs(MathModule.sin(0.0) - 0.0) < 0.00001
        assert abs(MathModule.sin(PI / 2) - 1.0) < 0.00001
        assert abs(MathModule.sin(PI) - 0.0) < 0.00001

    def test_cos(self):
        """Test cosine function."""
        assert abs(MathModule.cos(0.0) - 1.0) < 0.00001
        assert abs(MathModule.cos(PI / 2) - 0.0) < 0.00001
        assert abs(MathModule.cos(PI) - (-1.0)) < 0.00001

    def test_tan(self):
        """Test tangent function."""
        assert abs(MathModule.tan(0.0) - 0.0) < 0.00001
        assert abs(MathModule.tan(PI / 4) - 1.0) < 0.00001

    def test_asin(self):
        """Test arc sine function."""
        assert abs(MathModule.asin(0.0) - 0.0) < 0.00001
        assert abs(MathModule.asin(1.0) - PI / 2) < 0.00001

    def test_asin_out_of_range_raises_error(self):
        """Test that asin out of range raises error."""
        with pytest.raises(ValueError):
            MathModule.asin(2.0)
        with pytest.raises(ValueError):
            MathModule.asin(-2.0)

    def test_acos(self):
        """Test arc cosine function."""
        assert abs(MathModule.acos(1.0) - 0.0) < 0.00001
        assert abs(MathModule.acos(0.0) - PI / 2) < 0.00001

    def test_atan(self):
        """Test arc tangent function."""
        assert abs(MathModule.atan(0.0) - 0.0) < 0.00001
        assert abs(MathModule.atan(1.0) - PI / 4) < 0.00001

    def test_atan2(self):
        """Test two-argument arc tangent."""
        assert abs(MathModule.atan2(0.0, 1.0) - 0.0) < 0.00001
        assert abs(MathModule.atan2(1.0, 0.0) - PI / 2) < 0.00001


class TestRoundingFunctions:
    """Test rounding functions."""

    def test_ceil(self):
        """Test ceiling function."""
        assert MathModule.ceil(4.1) == 5
        assert MathModule.ceil(4.9) == 5
        assert MathModule.ceil(5.0) == 5
        assert MathModule.ceil(-4.1) == -4

    def test_floor(self):
        """Test floor function."""
        assert MathModule.floor(4.1) == 4
        assert MathModule.floor(4.9) == 4
        assert MathModule.floor(5.0) == 5
        assert MathModule.floor(-4.1) == -5

    def test_round(self):
        """Test round function."""
        assert MathModule.round(4.4) == 4.0
        assert MathModule.round(4.5) == 4.0  # Python's banker's rounding
        assert MathModule.round(4.6) == 5.0
        assert MathModule.round(4.567, 2) == 4.57

    def test_trunc(self):
        """Test truncate function."""
        assert MathModule.trunc(4.7) == 4
        assert MathModule.trunc(-4.7) == -4
        assert MathModule.trunc(5.0) == 5


class TestNumberTheoryFunctions:
    """Test number theory functions."""

    def test_gcd(self):
        """Test greatest common divisor."""
        assert MathModule.gcd(12, 8) == 4
        assert MathModule.gcd(17, 5) == 1
        assert MathModule.gcd(100, 50) == 50

    def test_lcm(self):
        """Test least common multiple."""
        assert MathModule.lcm(12, 8) == 24
        assert MathModule.lcm(5, 7) == 35
        assert MathModule.lcm(4, 6) == 12

    def test_factorial(self):
        """Test factorial function."""
        assert MathModule.factorial(0) == 1
        assert MathModule.factorial(1) == 1
        assert MathModule.factorial(5) == 120
        assert MathModule.factorial(10) == 3628800

    def test_factorial_negative_raises_error(self):
        """Test that factorial of negative raises error."""
        with pytest.raises(ValueError):
            MathModule.factorial(-1)

    def test_is_prime(self):
        """Test prime checking function."""
        assert MathModule.is_prime(2) is True
        assert MathModule.is_prime(3) is True
        assert MathModule.is_prime(17) is True
        assert MathModule.is_prime(4) is False
        assert MathModule.is_prime(1) is False
        assert MathModule.is_prime(0) is False


class TestUtilityFunctions:
    """Test utility functions."""

    def test_max(self):
        """Test max function."""
        assert MathModule.max(1, 5, 3) == 5
        assert MathModule.max(-1, -5, -3) == -1

    def test_min(self):
        """Test min function."""
        assert MathModule.min(1, 5, 3) == 1
        assert MathModule.min(-1, -5, -3) == -5

    def test_clamp(self):
        """Test clamp function."""
        assert MathModule.clamp(5, 0, 10) == 5
        assert MathModule.clamp(-5, 0, 10) == 0
        assert MathModule.clamp(15, 0, 10) == 10

    def test_lerp(self):
        """Test linear interpolation."""
        assert MathModule.lerp(0, 10, 0.0) == 0
        assert MathModule.lerp(0, 10, 0.5) == 5
        assert MathModule.lerp(0, 10, 1.0) == 10

    def test_degrees(self):
        """Test radians to degrees conversion."""
        assert abs(MathModule.degrees(PI) - 180.0) < 0.00001
        assert abs(MathModule.degrees(PI / 2) - 90.0) < 0.00001

    def test_radians(self):
        """Test degrees to radians conversion."""
        assert abs(MathModule.radians(180.0) - PI) < 0.00001
        assert abs(MathModule.radians(90.0) - PI / 2) < 0.00001


class TestStatisticsFunctions:
    """Test statistics functions."""

    def test_sum(self):
        """Test sum function."""
        assert MathModule.sum([1, 2, 3, 4, 5]) == 15
        assert MathModule.sum([10, 20, 30]) == 60

    def test_mean(self):
        """Test mean function."""
        assert MathModule.mean([1, 2, 3, 4, 5]) == 3.0
        assert MathModule.mean([10, 20, 30]) == 20.0

    def test_mean_empty_raises_error(self):
        """Test that mean of empty list raises error."""
        with pytest.raises(ValueError):
            MathModule.mean([])

    def test_median_odd_count(self):
        """Test median with odd number of elements."""
        assert MathModule.median([1, 2, 3, 4, 5]) == 3.0
        assert MathModule.median([1, 3, 5]) == 3.0

    def test_median_even_count(self):
        """Test median with even number of elements."""
        assert MathModule.median([1, 2, 3, 4]) == 2.5
        assert MathModule.median([10, 20, 30, 40]) == 25.0

    def test_median_empty_raises_error(self):
        """Test that median of empty list raises error."""
        with pytest.raises(ValueError):
            MathModule.median([])
