# AIGo Examples

This directory contains comprehensive examples demonstrating AIGo language features and capabilities.

## Directory Structure

```
examples/
├── hello.aigo              # Hello World program
├── basics/                 # Basic language features
├── algorithms/             # Classic algorithms
├── data_structures/        # Data structure implementations
└── real_world/            # Practical applications
```

## Running Examples

To run any example:

```bash
aigo examples/hello.aigo
aigo examples/basics/variables.aigo
aigo examples/algorithms/fibonacci.aigo
```

## Examples by Category

### Basics (`basics/`)

Learn fundamental AIGo syntax and features:

- **variables.aigo** - Variable declarations, types, and assignments
  - Integer, string, boolean, and float types
  - Variable reassignment
  - Basic printing

- **functions.aigo** - Function definitions and calls
  - Single and multiple parameters
  - Return values
  - Conditional logic in functions
  - Loops in functions

- **control_flow.aigo** - Control flow statements
  - If/else statements
  - While loops
  - Nested loops
  - Boolean conditions

- **operators.aigo** - Operators and expressions
  - Arithmetic operators (+, -, *, /, %)
  - Comparison operators (==, !=, <, >, <=, >=)
  - Logical operators (&&, ||, !)
  - Complex expressions

### Algorithms (`algorithms/`)

Classic algorithm implementations:

- **fibonacci.aigo** - Fibonacci sequence
  - Iterative implementation
  - Recursive implementation
  - Performance comparison

- **bubble_sort.aigo** - Bubble sort algorithm
  - Array sorting
  - Swap operations
  - Multiple test cases

- **binary_search.aigo** - Binary search algorithm
  - Efficient searching in sorted arrays
  - Comparison with linear search
  - Edge cases

- **prime_numbers.aigo** - Prime number algorithms
  - Prime checking
  - Sieve of Eratosthenes
  - Finding nth prime
  - Twin primes

### Data Structures (`data_structures/`)

Common data structure implementations:

- **stack.aigo** - Stack (LIFO)
  - Push/pop operations
  - Empty/full checks
  - Balanced parentheses example

- **queue.aigo** - Queue (FIFO)
  - Enqueue/dequeue operations
  - Circular array implementation
  - FIFO property demonstration

### Real World (`real_world/`)

Practical applications:

- **calculator.aigo** - Scientific calculator
  - Basic arithmetic (add, subtract, multiply, divide)
  - Power and square root
  - Factorial and percentage
  - Compound calculations (circle area, Pythagorean theorem)

- **string_utilities.aigo** - String manipulation
  - String length and reverse
  - Palindrome checking
  - Vowel counting
  - Case conversion
  - Word counting

## Learning Path

For beginners, we recommend following this order:

1. **Start with Basics**
   - `hello.aigo` - Your first AIGo program
   - `basics/variables.aigo` - Learn about types
   - `basics/operators.aigo` - Understand expressions
   - `basics/control_flow.aigo` - Master if/while
   - `basics/functions.aigo` - Write reusable code

2. **Move to Algorithms**
   - `algorithms/fibonacci.aigo` - Simple recursion
   - `algorithms/prime_numbers.aigo` - Number theory
   - `algorithms/binary_search.aigo` - Search algorithms
   - `algorithms/bubble_sort.aigo` - Sorting algorithms

3. **Explore Data Structures**
   - `data_structures/stack.aigo` - LIFO operations
   - `data_structures/queue.aigo` - FIFO operations

4. **Build Real Applications**
   - `real_world/calculator.aigo` - Mathematical operations
   - `real_world/string_utilities.aigo` - Text processing

## Key Concepts Demonstrated

### Type System
- Strong static typing
- Type annotations (`: i32`, `: string`, `: bool`, `: f64`)
- Type inference in expressions

### Memory Safety
- No null pointers
- Array bounds checking
- Result types for error handling

### Functional Features
- First-class functions
- Pure functions
- No global mutable state

### Error Handling
- `Result<T, Error>` type
- `?` operator for error propagation
- Explicit error handling

## Contributing Examples

Want to add more examples? Please:

1. Place examples in the appropriate category
2. Include comprehensive comments
3. Add description to this README
4. Test the example works correctly
5. Submit a pull request

## Example Template

```aigo
module main

import std.io

// Brief description of what this example demonstrates

fn main() -> Result<void, Error> {
    // Your code here
    io.println("Example output")?

    return Ok(void)
}
```

## Getting Help

- Read the [Main README](../README.md)
- Check the [Documentation](../docs/)
- Join our [Community Forum](https://community.aigo-lang.org)
- Report issues on [GitHub](https://github.com/aigo-lang/aigo/issues)

## License

All examples are released under the MIT License. Feel free to use them in your projects!
