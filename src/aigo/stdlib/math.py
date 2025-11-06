"""
AIGo Standard Library - Math Module

Mathematical functions and constants for AIGo programs.

This module provides mathematical operations including:
- Basic arithmetic utilities
- Trigonometric functions
- Exponential and logarithmic functions
- Number theory functions
- Constants (PI, E, etc.)

Usage in AIGo:
    import std.math

    let result: f64 = math.sqrt(16.0)
    let area: f64 = math.pi * radius * radius
"""

import math as py_math
from typing import Union, List

# Mathematical constants
PI = py_math.pi
E = py_math.e
TAU = py_math.tau
INF = float('inf')
NAN = float('nan')


class MathModule:
    """AIGo Math standard library module."""

    # Constants
    pi = PI
    e = E
    tau = TAU
    inf = INF
    nan = NAN

    @staticmethod
    def abs(x: Union[int, float]) -> Union[int, float]:
        """
        Return the absolute value of a number.

        Args:
            x: Number

        Returns:
            Absolute value
        """
        return abs(x)

    @staticmethod
    def sqrt(x: float) -> float:
        """
        Return the square root of x.

        Args:
            x: Non-negative number

        Returns:
            Square root of x

        Raises:
            ValueError: If x is negative
        """
        if x < 0:
            raise ValueError(f"math.sqrt: negative argument {x}")
        return py_math.sqrt(x)

    @staticmethod
    def pow(x: float, y: float) -> float:
        """
        Return x raised to the power y.

        Args:
            x: Base
            y: Exponent

        Returns:
            x ** y
        """
        return py_math.pow(x, y)

    @staticmethod
    def exp(x: float) -> float:
        """
        Return e raised to the power x.

        Args:
            x: Exponent

        Returns:
            e ** x
        """
        return py_math.exp(x)

    @staticmethod
    def log(x: float, base: float = E) -> float:
        """
        Return the logarithm of x to the given base.

        Args:
            x: Number (must be positive)
            base: Logarithm base (default: e)

        Returns:
            log_base(x)

        Raises:
            ValueError: If x <= 0
        """
        if x <= 0:
            raise ValueError(f"math.log: non-positive argument {x}")
        if base == E:
            return py_math.log(x)
        return py_math.log(x, base)

    @staticmethod
    def log10(x: float) -> float:
        """
        Return the base-10 logarithm of x.

        Args:
            x: Positive number

        Returns:
            log10(x)
        """
        if x <= 0:
            raise ValueError(f"math.log10: non-positive argument {x}")
        return py_math.log10(x)

    @staticmethod
    def log2(x: float) -> float:
        """
        Return the base-2 logarithm of x.

        Args:
            x: Positive number

        Returns:
            log2(x)
        """
        if x <= 0:
            raise ValueError(f"math.log2: non-positive argument {x}")
        return py_math.log2(x)

    # Trigonometric functions
    @staticmethod
    def sin(x: float) -> float:
        """Return the sine of x radians."""
        return py_math.sin(x)

    @staticmethod
    def cos(x: float) -> float:
        """Return the cosine of x radians."""
        return py_math.cos(x)

    @staticmethod
    def tan(x: float) -> float:
        """Return the tangent of x radians."""
        return py_math.tan(x)

    @staticmethod
    def asin(x: float) -> float:
        """
        Return the arc sine of x, in radians.

        Args:
            x: Number in range [-1, 1]

        Returns:
            Arc sine in radians

        Raises:
            ValueError: If x is outside [-1, 1]
        """
        if x < -1 or x > 1:
            raise ValueError(f"math.asin: argument {x} outside domain [-1, 1]")
        return py_math.asin(x)

    @staticmethod
    def acos(x: float) -> float:
        """
        Return the arc cosine of x, in radians.

        Args:
            x: Number in range [-1, 1]

        Returns:
            Arc cosine in radians
        """
        if x < -1 or x > 1:
            raise ValueError(f"math.acos: argument {x} outside domain [-1, 1]")
        return py_math.acos(x)

    @staticmethod
    def atan(x: float) -> float:
        """Return the arc tangent of x, in radians."""
        return py_math.atan(x)

    @staticmethod
    def atan2(y: float, x: float) -> float:
        """
        Return atan(y / x), in radians.

        The result is between -pi and pi.
        """
        return py_math.atan2(y, x)

    # Hyperbolic functions
    @staticmethod
    def sinh(x: float) -> float:
        """Return the hyperbolic sine of x."""
        return py_math.sinh(x)

    @staticmethod
    def cosh(x: float) -> float:
        """Return the hyperbolic cosine of x."""
        return py_math.cosh(x)

    @staticmethod
    def tanh(x: float) -> float:
        """Return the hyperbolic tangent of x."""
        return py_math.tanh(x)

    # Rounding and comparison
    @staticmethod
    def ceil(x: float) -> int:
        """Return the ceiling of x as an integer."""
        return py_math.ceil(x)

    @staticmethod
    def floor(x: float) -> int:
        """Return the floor of x as an integer."""
        return py_math.floor(x)

    @staticmethod
    def round(x: float, ndigits: int = 0) -> float:
        """
        Round x to ndigits decimal places.

        Args:
            x: Number to round
            ndigits: Number of decimal places (default: 0)

        Returns:
            Rounded number
        """
        return round(x, ndigits)

    @staticmethod
    def trunc(x: float) -> int:
        """Return x truncated to an integer."""
        return py_math.trunc(x)

    # Number theory and special functions
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Return the greatest common divisor of a and b.

        Args:
            a: First integer
            b: Second integer

        Returns:
            GCD of a and b
        """
        return py_math.gcd(a, b)

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Return the least common multiple of a and b.

        Args:
            a: First integer
            b: Second integer

        Returns:
            LCM of a and b
        """
        return (a * b) // py_math.gcd(a, b) if a and b else 0

    @staticmethod
    def factorial(n: int) -> int:
        """
        Return n factorial.

        Args:
            n: Non-negative integer

        Returns:
            n!

        Raises:
            ValueError: If n is negative
        """
        if n < 0:
            raise ValueError(f"math.factorial: negative argument {n}")
        return py_math.factorial(n)

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Check if n is a prime number.

        Args:
            n: Integer to check

        Returns:
            True if n is prime, False otherwise
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    # Utility functions
    @staticmethod
    def max(*args: Union[int, float]) -> Union[int, float]:
        """
        Return the largest argument.

        Args:
            *args: Numbers to compare

        Returns:
            Maximum value
        """
        return max(args)

    @staticmethod
    def min(*args: Union[int, float]) -> Union[int, float]:
        """
        Return the smallest argument.

        Args:
            *args: Numbers to compare

        Returns:
            Minimum value
        """
        return min(args)

    @staticmethod
    def clamp(x: float, min_val: float, max_val: float) -> float:
        """
        Clamp x to the range [min_val, max_val].

        Args:
            x: Value to clamp
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Clamped value
        """
        return max(min_val, min(x, max_val))

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """
        Linear interpolation between a and b.

        Args:
            a: Start value
            b: End value
            t: Interpolation factor (0.0 to 1.0)

        Returns:
            Interpolated value
        """
        return a + (b - a) * t

    @staticmethod
    def degrees(x: float) -> float:
        """Convert angle x from radians to degrees."""
        return py_math.degrees(x)

    @staticmethod
    def radians(x: float) -> float:
        """Convert angle x from degrees to radians."""
        return py_math.radians(x)

    # Statistics
    @staticmethod
    def sum(values: List[Union[int, float]]) -> Union[int, float]:
        """
        Return the sum of all values.

        Args:
            values: List of numbers

        Returns:
            Sum of values
        """
        return sum(values)

    @staticmethod
    def mean(values: List[Union[int, float]]) -> float:
        """
        Return the arithmetic mean of values.

        Args:
            values: List of numbers

        Returns:
            Mean value

        Raises:
            ValueError: If values is empty
        """
        if not values:
            raise ValueError("math.mean: empty list")
        return sum(values) / len(values)

    @staticmethod
    def median(values: List[Union[int, float]]) -> float:
        """
        Return the median of values.

        Args:
            values: List of numbers

        Returns:
            Median value

        Raises:
            ValueError: If values is empty
        """
        if not values:
            raise ValueError("math.median: empty list")

        sorted_values = sorted(values)
        n = len(sorted_values)

        if n % 2 == 0:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        else:
            return float(sorted_values[n // 2])


# Create module instance
math_module = MathModule()

__all__ = [
    "MathModule",
    "math_module",
    "PI",
    "E",
    "TAU",
    "INF",
    "NAN",
]
