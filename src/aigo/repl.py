"""
AIGo REPL (Read-Eval-Print-Loop)

Interactive shell for the AIGo programming language.

Features:
- Line-by-line code execution
- Multi-line input support
- Command history
- Tab completion (if readline available)
- Persistent environment across commands
- Special REPL commands

Usage:
    aigo-repl
    python -m aigo.repl

Special Commands:
    :help    - Show help message
    :quit    - Exit REPL
    :clear   - Clear screen
    :reset   - Reset environment
    :vars    - Show all variables
    :type X  - Show type of variable X
    :load F  - Load and execute file F
    :save F  - Save session history to file F
"""

import sys
import os
from typing import Optional, List
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, Environment

# Try to import readline for history and completion
try:
    import readline

    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class AIGoREPL:
    """AIGo Read-Eval-Print-Loop interactive shell."""

    def __init__(self):
        """Initialize REPL."""
        self.interpreter = Interpreter()
        self.environment = Environment()
        self.history: List[str] = []
        self.multiline_buffer: List[str] = []
        self.in_multiline = False
        self.prompt_main = f"{Colors.CYAN}aigo>{Colors.RESET} "
        self.prompt_cont = f"{Colors.CYAN}....>{Colors.RESET} "

        # Setup readline if available
        if HAS_READLINE:
            self._setup_readline()

    def _setup_readline(self) -> None:
        """Setup readline for history and completion."""
        history_file = os.path.expanduser("~/.aigo_history")

        # Load history
        try:
            readline.read_history_file(history_file)
        except FileNotFoundError:
            pass

        # Save history on exit
        import atexit

        atexit.register(readline.write_history_file, history_file)

        # Set history length
        readline.set_history_length(1000)

    def print_banner(self) -> None:
        """Print welcome banner."""
        version = "1.0.0-beta"
        print(f"{Colors.BOLD}{Colors.MAGENTA}")
        print("╔═══════════════════════════════════════════╗")
        print("║                                           ║")
        print("║        AIGo Programming Language          ║")
        print(f"║              Version {version}             ║")
        print("║                                           ║")
        print("╚═══════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        print(f"Type {Colors.YELLOW}:help{Colors.RESET} for help, ", end="")
        print(f"{Colors.YELLOW}:quit{Colors.RESET} to exit\n")

    def print_help(self) -> None:
        """Print help message."""
        print(f"\n{Colors.BOLD}AIGo REPL Commands:{Colors.RESET}")
        print(f"  {Colors.YELLOW}:help{Colors.RESET}     - Show this help message")
        print(f"  {Colors.YELLOW}:quit{Colors.RESET}     - Exit REPL")
        print(f"  {Colors.YELLOW}:exit{Colors.RESET}     - Exit REPL")
        print(f"  {Colors.YELLOW}:clear{Colors.RESET}    - Clear screen")
        print(f"  {Colors.YELLOW}:reset{Colors.RESET}    - Reset environment")
        print(f"  {Colors.YELLOW}:vars{Colors.RESET}     - Show all variables")
        print(f"  {Colors.YELLOW}:type X{Colors.RESET}   - Show type of variable X")
        print(f"  {Colors.YELLOW}:load F{Colors.RESET}   - Load and execute file F")
        print(f"  {Colors.YELLOW}:save F{Colors.RESET}   - Save session history to file F")
        print(f"  {Colors.YELLOW}:history{Colors.RESET}  - Show command history")
        print()
        print(f"{Colors.BOLD}Multi-line Input:{Colors.RESET}")
        print("  Use empty line to execute multi-line code block")
        print("  Incomplete statements automatically continue on next line")
        print()
        print(f"{Colors.BOLD}Examples:{Colors.RESET}")
        print(f'  {Colors.GREEN}let x: i32 = 42{Colors.RESET}')
        print(f'  {Colors.GREEN}fn double(n: i32) -> i32 {{ return n * 2 }}{Colors.RESET}')
        print(f'  {Colors.GREEN}io.println("Hello, AIGo!"){Colors.RESET}')
        print()

    def handle_command(self, command: str) -> bool:
        """
        Handle REPL commands.

        Args:
            command: Command string starting with ':'

        Returns:
            True to continue REPL, False to exit
        """
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd in [":quit", ":exit", ":q"]:
            print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
            return False

        elif cmd == ":help":
            self.print_help()

        elif cmd == ":clear":
            os.system("clear" if os.name != "nt" else "cls")

        elif cmd == ":reset":
            self.environment = Environment()
            self.interpreter = Interpreter()
            print(f"{Colors.GREEN}Environment reset{Colors.RESET}")

        elif cmd == ":vars":
            self.show_variables()

        elif cmd == ":type":
            if args:
                self.show_type(args)
            else:
                print(f"{Colors.RED}Usage: :type <variable>{Colors.RESET}")

        elif cmd == ":load":
            if args:
                self.load_file(args)
            else:
                print(f"{Colors.RED}Usage: :load <filename>{Colors.RESET}")

        elif cmd == ":save":
            if args:
                self.save_history(args)
            else:
                print(f"{Colors.RED}Usage: :save <filename>{Colors.RESET}")

        elif cmd == ":history":
            self.show_history()

        else:
            print(f"{Colors.RED}Unknown command: {cmd}{Colors.RESET}")
            print(f"Type {Colors.YELLOW}:help{Colors.RESET} for help")

        return True

    def show_variables(self) -> None:
        """Show all variables in current environment."""
        if not self.environment.variables:
            print(f"{Colors.YELLOW}No variables defined{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}Variables:{Colors.RESET}")
        for name, value in self.environment.variables.items():
            type_name = type(value).__name__
            print(f"  {Colors.CYAN}{name}{Colors.RESET}: {type_name} = {value}")
        print()

    def show_type(self, var_name: str) -> None:
        """Show type of variable."""
        var_name = var_name.strip()
        if var_name in self.environment.variables:
            value = self.environment.variables[var_name]
            type_name = type(value).__name__
            print(f"{Colors.CYAN}{var_name}{Colors.RESET}: {type_name}")
        else:
            print(f"{Colors.RED}Variable '{var_name}' not defined{Colors.RESET}")

    def load_file(self, filename: str) -> None:
        """Load and execute file."""
        filename = filename.strip()
        try:
            with open(filename, "r") as f:
                code = f.read()

            print(f"{Colors.YELLOW}Loading {filename}...{Colors.RESET}")
            self.eval_code(code)
            print(f"{Colors.GREEN}File loaded successfully{Colors.RESET}")

        except FileNotFoundError:
            print(f"{Colors.RED}File not found: {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error loading file: {e}{Colors.RESET}")

    def save_history(self, filename: str) -> None:
        """Save history to file."""
        filename = filename.strip()
        try:
            with open(filename, "w") as f:
                for line in self.history:
                    f.write(line + "\n")
            print(f"{Colors.GREEN}History saved to {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error saving history: {e}{Colors.RESET}")

    def show_history(self) -> None:
        """Show command history."""
        if not self.history:
            print(f"{Colors.YELLOW}No history{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}History:{Colors.RESET}")
        for i, line in enumerate(self.history, 1):
            print(f"  {i:3d}  {line}")
        print()

    def is_complete_statement(self, code: str) -> bool:
        """
        Check if code is a complete statement.

        Args:
            code: Code string

        Returns:
            True if complete, False if needs more input
        """
        # Count braces
        open_braces = code.count("{")
        close_braces = code.count("}")

        # Count parentheses
        open_parens = code.count("(")
        close_parens = code.count(")")

        # Count brackets
        open_brackets = code.count("[")
        close_brackets = code.count("]")

        # If unbalanced, need more input
        if (
            open_braces != close_braces
            or open_parens != close_parens
            or open_brackets != close_brackets
        ):
            return False

        # Check for incomplete statements
        stripped = code.strip()
        incomplete_keywords = ["fn", "if", "while", "for", "match", "struct", "enum"]

        for keyword in incomplete_keywords:
            if stripped.startswith(keyword) and "{" not in code:
                return False

        return True

    def eval_code(self, code: str) -> None:
        """
        Evaluate code and print result.

        Args:
            code: AIGo code to evaluate
        """
        try:
            # Wrap in minimal module if needed
            if not code.strip().startswith("module"):
                code = "module repl\n\n" + code

            # Tokenize
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # Parse
            parser = Parser(tokens)
            program = parser.parse_program()

            # Interpret with current environment
            self.interpreter.environment = self.environment
            result = self.interpreter.interpret_program(program)

            # Update environment
            self.environment = self.interpreter.environment

            # Print result if not None
            if result is not None:
                print(f"{Colors.GREEN}{result}{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")

    def read_input(self) -> Optional[str]:
        """
        Read input from user.

        Returns:
            Input string or None if EOF
        """
        try:
            if self.in_multiline:
                line = input(self.prompt_cont)
            else:
                line = input(self.prompt_main)
            return line
        except (EOFError, KeyboardInterrupt):
            return None

    def run(self) -> None:
        """Run REPL main loop."""
        self.print_banner()

        while True:
            try:
                # Read input
                line = self.read_input()

                # Handle EOF or interrupt
                if line is None:
                    print()  # New line
                    break

                # Skip empty lines when not in multiline
                if not line.strip() and not self.in_multiline:
                    continue

                # Handle commands
                if line.strip().startswith(":"):
                    if not self.handle_command(line.strip()):
                        break
                    continue

                # Handle multiline input
                if self.in_multiline:
                    if line.strip() == "":
                        # Execute buffered code
                        code = "\n".join(self.multiline_buffer)
                        self.eval_code(code)
                        self.history.append(code)

                        # Reset buffer
                        self.multiline_buffer = []
                        self.in_multiline = False
                    else:
                        self.multiline_buffer.append(line)
                else:
                    # Check if complete statement
                    if self.is_complete_statement(line):
                        # Execute immediately
                        self.eval_code(line)
                        self.history.append(line)
                    else:
                        # Start multiline mode
                        self.multiline_buffer = [line]
                        self.in_multiline = True

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interrupted{Colors.RESET}")
                self.multiline_buffer = []
                self.in_multiline = False
                continue

            except Exception as e:
                print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
                continue


def main() -> int:
    """Main entry point for REPL."""
    repl = AIGoREPL()
    try:
        repl.run()
        return 0
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
