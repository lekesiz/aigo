# AIGo Performance Benchmarks

Comprehensive benchmarking suite for measuring AIGo interpreter performance.

## Features

- **Lexer Benchmarks**: Tokenization speed for simple and complex code
- **Parser Benchmarks**: Parsing performance for different code patterns
- **Interpreter Benchmarks**: Execution speed for common operations
- **Memory Tracking**: Memory usage measurement (requires psutil)
- **Baseline Comparison**: Track performance changes over time
- **Statistical Analysis**: Standard deviation and confidence intervals

## Requirements

```bash
# Basic requirements (included in project)
pip install -e .

# Optional: For memory tracking
pip install psutil
```

## Usage

### Run All Benchmarks

```bash
python benchmarks/run_benchmarks.py
```

### Quick Mode (Fewer Iterations)

```bash
python benchmarks/run_benchmarks.py --quick
```

### Save Results

```bash
python benchmarks/run_benchmarks.py --save baseline.json
```

### Compare with Baseline

```bash
# First, create a baseline
python benchmarks/run_benchmarks.py --save baseline.json

# Make some changes...

# Compare current performance with baseline
python benchmarks/run_benchmarks.py --compare baseline.json
```

## Benchmarks Included

### 1. Lexer (Simple Code)
- **Code**: Basic variable declarations
- **Measures**: Tokenization speed
- **Iterations**: 1,000 (100 in quick mode)

### 2. Lexer (Complex Code)
- **Code**: Recursive function with control flow
- **Measures**: Tokenization of complex syntax
- **Iterations**: 1,000 (100 in quick mode)

### 3. Parser (Simple Expression)
- **Code**: Single variable declaration
- **Measures**: AST construction speed
- **Iterations**: 1,000 (100 in quick mode)

### 4. Parser (Function Definition)
- **Code**: Function with recursion and if statement
- **Measures**: Complex AST construction
- **Iterations**: 100 (10 in quick mode)

### 5. Arithmetic Operations
- **Code**: Multiple arithmetic expressions
- **Measures**: Expression evaluation speed
- **Iterations**: 1,000 (100 in quick mode)

### 6. Loop Performance
- **Code**: While loop with 100 iterations
- **Measures**: Loop execution overhead
- **Iterations**: 100 (10 in quick mode)

### 7. Function Call Overhead
- **Code**: Multiple function definitions and calls
- **Measures**: Function call performance
- **Iterations**: 100 (10 in quick mode)

### 8. Large File
- **Code**: 200 statements (100 variables + 100 calculations)
- **Measures**: Scalability with file size
- **Includes**: Memory usage tracking
- **Iterations**: 100 (10 in quick mode)

## Output Format

### Console Output

```
AIGo Performance Benchmarks
============================================================

Running in QUICK mode (fewer iterations)

Running: Lexer (Simple)... ✓ (0.15ms)
Running: Lexer (Complex)... ✓ (0.48ms)
Running: Parser (Simple)... ✓ (0.32ms)
...

Benchmark Results
----------------------------------------------------------------------------------------------------
Benchmark                        Duration (ms)        Ops/sec    Iterations      Std Dev
----------------------------------------------------------------------------------------------------
Lexer (Simple Code)                      0.145         689,655           100       ±0.012
Lexer (Complex Code)                     0.482         207,468           100       ±0.028
Parser (Simple Expression)               0.318         314,465           100       ±0.021
...
----------------------------------------------------------------------------------------------------

Total benchmark time: 2.45s
Python version: 3.11.5
Platform: linux
```

### Comparison Output

```
Comparison with Baseline
--------------------------------------------------------------------------------
Benchmark                      Current     Baseline       Change
--------------------------------------------------------------------------------
Lexer (Simple Code)              0.15ms      0.18ms    ↓   16.7%
Lexer (Complex Code)             0.48ms      0.45ms    ↑    6.7%
Parser (Simple Expression)       0.32ms      0.33ms    ↓    3.0%
...
--------------------------------------------------------------------------------
```

**Legend**:
- 🟢 `↓` Green: Performance improved (>5% faster)
- 🟡 `→` Yellow: Similar performance (±5%)
- 🔴 `↑` Red: Performance degraded (>5% slower)

## Understanding Results

### Duration (ms)
Average time to execute one iteration in milliseconds. **Lower is better**.

### Ops/sec
Operations per second = `(iterations / duration_ms) * 1000`. **Higher is better**.

### Iterations
Number of times the benchmark was executed for averaging.

### Std Dev
Standard deviation of durations. Lower values indicate more consistent performance.

## Performance Goals

| Component | Target | Current Status |
|-----------|--------|----------------|
| Lexer (Simple) | < 0.5ms | ✅ |
| Parser (Simple) | < 1.0ms | ✅ |
| Loops (100 iterations) | < 5.0ms | 🚧 In Progress |
| Large File (200 statements) | < 50ms | 🚧 In Progress |

## Continuous Integration

Add benchmarks to your CI pipeline:

```yaml
# .github/workflows/benchmarks.yml
name: Performance Benchmarks

on: [push, pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run benchmarks
        run: python benchmarks/run_benchmarks.py --save current.json

      - name: Compare with baseline
        run: python benchmarks/run_benchmarks.py --compare baseline.json
```

## Profiling

For detailed profiling:

```bash
# CPU profiling
python -m cProfile -o profile.stats benchmarks/run_benchmarks.py

# Analyze profile
python -m pstats profile.stats
>>> sort cumulative
>>> stats 20

# Memory profiling
pip install memory-profiler
python -m memory_profiler benchmarks/run_benchmarks.py
```

## Contributing

To add new benchmarks:

1. Add a new method to `AIGoBenchmark` class:
   ```python
   def benchmark_my_feature(self):
       code = "..."

       def run():
           # Your benchmark code
           pass

       duration, std_dev = self._measure_time(run, self.iterations_normal)
       # ... create and return result
   ```

2. Add it to the `run_all()` method
3. Document it in this README
4. Test it with both normal and quick modes

## Best Practices

1. **Warm-up**: Run a few iterations before measuring to warm up caches
2. **Isolation**: Close other applications to minimize interference
3. **Consistency**: Run on the same machine for comparisons
4. **Multiple Runs**: Run multiple times and average results
5. **Environment**: Document Python version, OS, and hardware

## Troubleshooting

### High Standard Deviation
- Close other applications
- Increase iteration count
- Check for background processes

### Memory Errors
- Reduce iteration count
- Use `--quick` mode
- Install psutil: `pip install psutil`

### Inconsistent Results
- Ensure consistent system load
- Run multiple times and compare
- Check CPU frequency scaling

## Resources

- [Python timeit module](https://docs.python.org/3/library/timeit.html)
- [Python profilers](https://docs.python.org/3/library/profile.html)
- [Benchmarking Best Practices](https://pyperf.readthedocs.io/en/latest/api.html)

## Future Enhancements

- [ ] HTML report generation
- [ ] Visualization graphs
- [ ] Regression detection
- [ ] Multi-platform comparison
- [ ] Historical trend tracking
- [ ] Automatic baseline updates
- [ ] Benchmark isolation (separate processes)
- [ ] JIT compilation benchmarks
