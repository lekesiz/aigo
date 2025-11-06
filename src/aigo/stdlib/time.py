"""
AIGo Standard Library - Time Module

Time and date utilities for AIGo programs.

This module provides time operations including:
- Current time and date
- Time formatting and parsing
- Time arithmetic
- Timezones
- Sleep and delays

Usage in AIGo:
    import std.time

    let now: i64 = time.now()
    let formatted: string = time.format(now, "%Y-%m-%d")
    time.sleep(1.0)
"""

import time as py_time
import datetime
from typing import Optional, Tuple


class TimeModule:
    """AIGo Time standard library module."""

    # Time format constants
    FORMAT_ISO = "%Y-%m-%dT%H:%M:%S"
    FORMAT_DATE = "%Y-%m-%d"
    FORMAT_TIME = "%H:%M:%S"
    FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"
    FORMAT_US = "%m/%d/%Y"
    FORMAT_EU = "%d/%m/%Y"

    @staticmethod
    def now() -> float:
        """
        Get current Unix timestamp (seconds since epoch).

        Returns:
            Current timestamp as float
        """
        return py_time.time()

    @staticmethod
    def now_millis() -> int:
        """
        Get current timestamp in milliseconds.

        Returns:
            Current timestamp in milliseconds
        """
        return int(py_time.time() * 1000)

    @staticmethod
    def now_nanos() -> int:
        """
        Get current timestamp in nanoseconds (if available).

        Returns:
            Current timestamp in nanoseconds
        """
        return py_time.time_ns()

    @staticmethod
    def sleep(seconds: float) -> None:
        """
        Sleep for specified seconds.

        Args:
            seconds: Sleep duration in seconds
        """
        py_time.sleep(seconds)

    @staticmethod
    def sleep_millis(milliseconds: int) -> None:
        """
        Sleep for specified milliseconds.

        Args:
            milliseconds: Sleep duration in milliseconds
        """
        py_time.sleep(milliseconds / 1000.0)

    @staticmethod
    def format(timestamp: float, format_str: str = FORMAT_ISO) -> str:
        """
        Format timestamp to string.

        Args:
            timestamp: Unix timestamp
            format_str: Format string (default: ISO format)

        Returns:
            Formatted time string

        Format codes:
            %Y - Year (4 digits)
            %m - Month (01-12)
            %d - Day (01-31)
            %H - Hour (00-23)
            %M - Minute (00-59)
            %S - Second (00-59)
            %a - Weekday short (Mon, Tue, ...)
            %A - Weekday full (Monday, Tuesday, ...)
            %b - Month short (Jan, Feb, ...)
            %B - Month full (January, February, ...)
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime(format_str)

    @staticmethod
    def parse(time_str: str, format_str: str = FORMAT_ISO) -> float:
        """
        Parse time string to timestamp.

        Args:
            time_str: Time string to parse
            format_str: Format string (default: ISO format)

        Returns:
            Unix timestamp

        Raises:
            ValueError: If time string doesn't match format
        """
        try:
            dt = datetime.datetime.strptime(time_str, format_str)
            return dt.timestamp()
        except ValueError as e:
            raise ValueError(f"time.parse: invalid time string - {e}")

    @staticmethod
    def year(timestamp: float) -> int:
        """Get year from timestamp."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.year

    @staticmethod
    def month(timestamp: float) -> int:
        """Get month from timestamp (1-12)."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.month

    @staticmethod
    def day(timestamp: float) -> int:
        """Get day from timestamp (1-31)."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.day

    @staticmethod
    def hour(timestamp: float) -> int:
        """Get hour from timestamp (0-23)."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.hour

    @staticmethod
    def minute(timestamp: float) -> int:
        """Get minute from timestamp (0-59)."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.minute

    @staticmethod
    def second(timestamp: float) -> int:
        """Get second from timestamp (0-59)."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.second

    @staticmethod
    def weekday(timestamp: float) -> int:
        """
        Get weekday from timestamp.

        Returns:
            Weekday (0=Monday, 6=Sunday)
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.weekday()

    @staticmethod
    def is_weekend(timestamp: float) -> bool:
        """
        Check if timestamp is on weekend.

        Returns:
            True if Saturday or Sunday
        """
        return TimeModule.weekday(timestamp) >= 5

    @staticmethod
    def add_seconds(timestamp: float, seconds: float) -> float:
        """
        Add seconds to timestamp.

        Args:
            timestamp: Base timestamp
            seconds: Seconds to add

        Returns:
            New timestamp
        """
        return timestamp + seconds

    @staticmethod
    def add_minutes(timestamp: float, minutes: int) -> float:
        """Add minutes to timestamp."""
        return timestamp + (minutes * 60)

    @staticmethod
    def add_hours(timestamp: float, hours: int) -> float:
        """Add hours to timestamp."""
        return timestamp + (hours * 3600)

    @staticmethod
    def add_days(timestamp: float, days: int) -> float:
        """Add days to timestamp."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt = dt + datetime.timedelta(days=days)
        return dt.timestamp()

    @staticmethod
    def add_months(timestamp: float, months: int) -> float:
        """
        Add months to timestamp.

        Args:
            timestamp: Base timestamp
            months: Months to add

        Returns:
            New timestamp
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        year = dt.year
        month = dt.month + months

        # Handle year overflow
        while month > 12:
            month -= 12
            year += 1

        while month < 1:
            month += 12
            year -= 1

        # Handle day overflow
        max_day = 31
        if month in [4, 6, 9, 11]:
            max_day = 30
        elif month == 2:
            max_day = 29 if TimeModule._is_leap_year(year) else 28

        day = min(dt.day, max_day)

        new_dt = dt.replace(year=year, month=month, day=day)
        return new_dt.timestamp()

    @staticmethod
    def add_years(timestamp: float, years: int) -> float:
        """Add years to timestamp."""
        return TimeModule.add_months(timestamp, years * 12)

    @staticmethod
    def diff(timestamp1: float, timestamp2: float) -> float:
        """
        Calculate difference between two timestamps.

        Args:
            timestamp1: First timestamp
            timestamp2: Second timestamp

        Returns:
            Difference in seconds (timestamp1 - timestamp2)
        """
        return timestamp1 - timestamp2

    @staticmethod
    def diff_days(timestamp1: float, timestamp2: float) -> int:
        """
        Calculate difference in days.

        Returns:
            Difference in days (rounded)
        """
        return int((timestamp1 - timestamp2) / 86400)

    @staticmethod
    def diff_hours(timestamp1: float, timestamp2: float) -> int:
        """
        Calculate difference in hours.

        Returns:
            Difference in hours (rounded)
        """
        return int((timestamp1 - timestamp2) / 3600)

    @staticmethod
    def start_of_day(timestamp: float) -> float:
        """
        Get timestamp for start of day (00:00:00).

        Args:
            timestamp: Input timestamp

        Returns:
            Timestamp for start of day
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return dt.timestamp()

    @staticmethod
    def end_of_day(timestamp: float) -> float:
        """
        Get timestamp for end of day (23:59:59).

        Args:
            timestamp: Input timestamp

        Returns:
            Timestamp for end of day
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return dt.timestamp()

    @staticmethod
    def start_of_month(timestamp: float) -> float:
        """Get timestamp for start of month."""
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return dt.timestamp()

    @staticmethod
    def end_of_month(timestamp: float) -> float:
        """Get timestamp for end of month."""
        dt = datetime.datetime.fromtimestamp(timestamp)

        # Find last day of month
        next_month = dt.replace(day=28) + datetime.timedelta(days=4)
        last_day = next_month - datetime.timedelta(days=next_month.day)

        dt = dt.replace(day=last_day.day, hour=23, minute=59, second=59, microsecond=999999)
        return dt.timestamp()

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Check if year is a leap year.

        Args:
            year: Year to check

        Returns:
            True if leap year
        """
        return TimeModule._is_leap_year(year)

    @staticmethod
    def _is_leap_year(year: int) -> bool:
        """Internal leap year check."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Get number of days in a month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Number of days in month
        """
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:  # February
            return 29 if TimeModule._is_leap_year(year) else 28

    @staticmethod
    def elapsed(start_time: float) -> float:
        """
        Calculate elapsed time since start_time.

        Args:
            start_time: Start timestamp

        Returns:
            Elapsed seconds
        """
        return py_time.time() - start_time

    @staticmethod
    def measure(func: callable) -> Tuple[Any, float]:
        """
        Measure execution time of function.

        Args:
            func: Function to measure

        Returns:
            Tuple of (result, duration_seconds)
        """
        start = py_time.time()
        result = func()
        duration = py_time.time() - start
        return result, duration

    @staticmethod
    def timer_start() -> float:
        """
        Start a timer.

        Returns:
            Start timestamp
        """
        return py_time.time()

    @staticmethod
    def timer_stop(start_time: float) -> float:
        """
        Stop timer and get elapsed time.

        Args:
            start_time: Timer start time from timer_start()

        Returns:
            Elapsed seconds
        """
        return py_time.time() - start_time


# Create module instance
time_module = TimeModule()

__all__ = ["TimeModule", "time_module"]
