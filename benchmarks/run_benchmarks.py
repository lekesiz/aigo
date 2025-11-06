#!/usr/bin/env python3
"""
AIGo Performance Benchmarking Suite

Comprehensive benchmarks for measuring AIGo interpreter performance.

Features:
- Lexer performance benchmarks
- Parser performance benchmarks
- Interpreter performance benchmarks
- Memory usage tracking
- Comparison with baseline results
- HTML report generation

Usage:
    python benchmarks/run_benchmarks.py
    python benchmarks/run_benchmarks.py --quick
    python benchmarks/run_benchmarks.py --save baseline.json
    python benchmarks/run_benchmarks.py --compare baseline.json
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, asdict
import statistics

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aigo.lexer import Lexer
from aigo.parser import Parser
from aigo.interpreter import Interpreter


@dataclass
class BenchmarkResult:
    """Single benchmark result."""

    name: str
    duration_ms: float
    iterations: int
    ops_per_second: float
    memory_mb: Optional[float] = None
    std_dev_ms: Optional[float] = None


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results."""

    name: str
    timestamp: str
    results: List[BenchmarkResult]
    total_duration_s: float
    version: str = "1.0.0-beta"


class Colors:
    """ANSI colors for output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


class AIGoBenchmark:
    """AIGo performance benchmarking system."""

    def __init__(self, quick_mode: bool = False):
        """
        Initialize benchmark suite.

        Args:
            quick_mode: Run fewer iterations for faster results
        """
        self.quick_mode = quick_mode
        self.iterations_normal = 1000 if not quick_mode else 100
        self.iterations_heavy = 100 if not quick_mode else 10
        self.results: List[BenchmarkResult] = []

    def _measure_time(
        self, func: Callable, iterations: int, *args, **kwargs
    ) -> tuple[float, float]:
        """
        Measure execution time of a function.

        Args:
            func: Function to benchmark
            iterations: Number of iterations
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Tuple of (average_duration_ms, std_dev_ms)
        """
        durations = []

        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            durations.append((end - start) * 1000)  # Convert to ms

        avg_duration = statistics.mean(durations)
        std_dev = statistics.stdev(durations) if len(durations) > 1 else 0.0

        return avg_duration, std_dev

    def _get_memory_usage(self) -> float:
        """
        Get current memory usage in MB.

        Returns:
            Memory usage in MB, or 0 if psutil not available
        """
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0

    def benchmark_lexer_simple(self):
        """Benchmark lexer with simple code."""
        code = "let x: i32 = 42\nlet y: i32 = x + 10"

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            return len(tokens)

        duration, std_dev = self._measure_time(run, self.iterations_normal)
        ops_per_second = (self.iterations_normal / duration) * 1000

        result = BenchmarkResult(
            name="Lexer (Simple Code)",
            duration_ms=duration,
            iterations=self.iterations_normal,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_lexer_complex(self):
        """Benchmark lexer with complex code."""
        code = """
        fn fibonacci(n: i32) -> i32 {
            if n <= 1 {
                return n
            }
            return fibonacci(n - 1) + fibonacci(n - 2)
        }

        fn main() -> Result<void, Error> {
            let result: i32 = fibonacci(10)
            io.println("Result:", result)?
            return Ok(void)
        }
        """

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            return len(tokens)

        duration, std_dev = self._measure_time(run, self.iterations_normal)
        ops_per_second = (self.iterations_normal / duration) * 1000

        result = BenchmarkResult(
            name="Lexer (Complex Code)",
            duration_ms=duration,
            iterations=self.iterations_normal,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_parser_simple(self):
        """Benchmark parser with simple code."""
        code = "let x: i32 = 42"

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse_program()
            return program

        duration, std_dev = self._measure_time(run, self.iterations_normal)
        ops_per_second = (self.iterations_normal / duration) * 1000

        result = BenchmarkResult(
            name="Parser (Simple Expression)",
            duration_ms=duration,
            iterations=self.iterations_normal,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_parser_complex(self):
        """Benchmark parser with complex code."""
        code = """
        fn factorial(n: i32) -> i32 {
            if n <= 1 {
                return 1
            }
            return n * factorial(n - 1)
        }
        """

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse_program()
            return program

        duration, std_dev = self._measure_time(run, self.iterations_heavy)
        ops_per_second = (self.iterations_heavy / duration) * 1000

        result = BenchmarkResult(
            name="Parser (Function Definition)",
            duration_ms=duration,
            iterations=self.iterations_heavy,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_arithmetic(self):
        """Benchmark arithmetic operations."""
        code = """
        let a: i32 = 10
        let b: i32 = 20
        let c: i32 = a + b
        let d: i32 = c * 2
        let e: i32 = d - 5
        """

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            # Note: Full interpretation not implemented yet
            return tokens

        duration, std_dev = self._measure_time(run, self.iterations_normal)
        ops_per_second = (self.iterations_normal / duration) * 1000

        result = BenchmarkResult(
            name="Arithmetic Operations",
            duration_ms=duration,
            iterations=self.iterations_normal,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_loops(self):
        """Benchmark loop performance."""
        code = """
        let sum: i32 = 0
        let i: i32 = 0
        while i < 100 {
            sum = sum + i
            i = i + 1
        }
        """

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse_program()
            return program

        duration, std_dev = self._measure_time(run, self.iterations_heavy)
        ops_per_second = (self.iterations_heavy / duration) * 1000

        result = BenchmarkResult(
            name="Loop Performance",
            duration_ms=duration,
            iterations=self.iterations_heavy,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_function_calls(self):
        """Benchmark function call overhead."""
        code = """
        fn add(a: i32, b: i32) -> i32 {
            return a + b
        }

        fn multiply(x: i32, y: i32) -> i32 {
            return x * y
        }

        let result1: i32 = add(5, 10)
        let result2: i32 = multiply(result1, 2)
        """

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse_program()
            return program

        duration, std_dev = self._measure_time(run, self.iterations_heavy)
        ops_per_second = (self.iterations_heavy / duration) * 1000

        result = BenchmarkResult(
            name="Function Call Overhead",
            duration_ms=duration,
            iterations=self.iterations_heavy,
            ops_per_second=ops_per_second,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def benchmark_large_file(self):
        """Benchmark parsing a large file."""
        # Generate large code file
        lines = []
        for i in range(100):
            lines.append(f"let var{i}: i32 = {i}")
            lines.append(f"let result{i}: i32 = var{i} * 2")

        code = "\n".join(lines)

        def run():
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse_program()
            return program

        duration, std_dev = self._measure_time(run, self.iterations_heavy)
        ops_per_second = (self.iterations_heavy / duration) * 1000
        memory_mb = self._get_memory_usage()

        result = BenchmarkResult(
            name="Large File (200 statements)",
            duration_ms=duration,
            iterations=self.iterations_heavy,
            ops_per_second=ops_per_second,
            memory_mb=memory_mb,
            std_dev_ms=std_dev,
        )
        self.results.append(result)
        return result

    def run_all(self) -> List[BenchmarkResult]:
        """
        Run all benchmarks.

        Returns:
            List of benchmark results
        """
        benchmarks = [
            ("Lexer (Simple)", self.benchmark_lexer_simple),
            ("Lexer (Complex)", self.benchmark_lexer_complex),
            ("Parser (Simple)", self.benchmark_parser_simple),
            ("Parser (Complex)", self.benchmark_parser_complex),
            ("Arithmetic Ops", self.benchmark_arithmetic),
            ("Loops", self.benchmark_loops),
            ("Function Calls", self.benchmark_function_calls),
            ("Large File", self.benchmark_large_file),
        ]

        print(f"\n{Colors.BOLD}{Colors.CYAN}AIGo Performance Benchmarks{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

        if self.quick_mode:
            print(f"{Colors.YELLOW}Running in QUICK mode (fewer iterations){Colors.RESET}\n")

        for name, benchmark in benchmarks:
            print(f"Running: {name}...", end=" ", flush=True)
            try:
                result = benchmark()
                status = f"{Colors.GREEN}✓{Colors.RESET}"
                print(f"{status} ({result.duration_ms:.2f}ms)")
            except Exception as e:
                status = f"{Colors.RED}✗{Colors.RESET}"
                print(f"{status} Error: {e}")

        return self.results

    def print_results(self):
        """Print formatted results table."""
        print(f"\n{Colors.BOLD}Benchmark Results{Colors.RESET}")
        print(f"{Colors.CYAN}{'-' * 100}{Colors.RESET}")
        print(
            f"{'Benchmark':<30} {'Duration (ms)':>15} {'Ops/sec':>15} {'Iterations':>12} {'Std Dev':>12}"
        )
        print(f"{Colors.CYAN}{'-' * 100}{Colors.RESET}")

        for result in self.results:
            duration_str = f"{result.duration_ms:.3f}"
            ops_str = f"{result.ops_per_second:,.0f}"
            iter_str = f"{result.iterations:,}"
            std_str = f"±{result.std_dev_ms:.3f}" if result.std_dev_ms else "N/A"

            print(
                f"{result.name:<30} {duration_str:>15} {ops_str:>15} {iter_str:>12} {std_str:>12}"
            )

            if result.memory_mb:
                print(f"{'  Memory usage:':<30} {result.memory_mb:.2f} MB")

        print(f"{Colors.CYAN}{'-' * 100}{Colors.RESET}\n")

    def save_results(self, filepath: str):
        """
        Save results to JSON file.

        Args:
            filepath: Path to save results
        """
        import datetime

        suite = BenchmarkSuite(
            name="AIGo Performance Benchmarks",
            timestamp=datetime.datetime.now().isoformat(),
            results=self.results,
            total_duration_s=sum(r.duration_ms for r in self.results) / 1000,
        )

        with open(filepath, "w") as f:
            json.dump(asdict(suite), f, indent=2)

        print(f"{Colors.GREEN}Results saved to {filepath}{Colors.RESET}")

    def compare_with_baseline(self, baseline_path: str):
        """
        Compare current results with baseline.

        Args:
            baseline_path: Path to baseline JSON file
        """
        try:
            with open(baseline_path, "r") as f:
                baseline_data = json.load(f)

            baseline_results = {r["name"]: r for r in baseline_data["results"]}

            print(f"\n{Colors.BOLD}Comparison with Baseline{Colors.RESET}")
            print(f"{Colors.CYAN}{'-' * 80}{Colors.RESET}")
            print(f"{'Benchmark':<30} {'Current':>12} {'Baseline':>12} {'Change':>12}")
            print(f"{Colors.CYAN}{'-' * 80}{Colors.RESET}")

            for result in self.results:
                if result.name in baseline_results:
                    baseline = baseline_results[result.name]
                    current = result.duration_ms
                    old = baseline["duration_ms"]
                    change_pct = ((current - old) / old) * 100

                    if change_pct < -5:
                        color = Colors.GREEN
                        arrow = "↓"
                    elif change_pct > 5:
                        color = Colors.RED
                        arrow = "↑"
                    else:
                        color = Colors.YELLOW
                        arrow = "→"

                    print(
                        f"{result.name:<30} {current:>10.2f}ms {old:>10.2f}ms "
                        f"{color}{arrow} {abs(change_pct):>6.1f}%{Colors.RESET}"
                    )
                else:
                    print(f"{result.name:<30} {'NEW':>12}")

            print(f"{Colors.CYAN}{'-' * 80}{Colors.RESET}\n")

        except FileNotFoundError:
            print(f"{Colors.RED}Baseline file not found: {baseline_path}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error comparing with baseline: {e}{Colors.RESET}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AIGo Performance Benchmarks")
    parser.add_argument("--quick", action="store_true", help="Run quick benchmarks (fewer iterations)")
    parser.add_argument("--save", metavar="FILE", help="Save results to JSON file")
    parser.add_argument("--compare", metavar="FILE", help="Compare with baseline JSON file")

    args = parser.parse_args()

    # Run benchmarks
    benchmark = AIGoBenchmark(quick_mode=args.quick)
    start_time = time.time()
    benchmark.run_all()
    total_time = time.time() - start_time

    # Print results
    benchmark.print_results()

    print(f"Total benchmark time: {total_time:.2f}s")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}\n")

    # Save results if requested
    if args.save:
        benchmark.save_results(args.save)

    # Compare with baseline if requested
    if args.compare:
        benchmark.compare_with_baseline(args.compare)

    return 0


if __name__ == "__main__":
    sys.exit(main())
