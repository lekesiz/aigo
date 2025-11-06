#!/usr/bin/env python3
"""
AIGo Command Line Interface

Provides CLI commands for running AIGo programs.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from .interpreter import run_aigo_code
from . import __version__


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="aigo",
        description="AIGo Programming Language Interpreter",
        epilog="For more information, visit https://github.com/lekesiz/aigo"
    )

    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        help="AIGo source file to execute"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"AIGo {__version__}"
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Show execution statistics"
    )

    args = parser.parse_args()

    # If no file provided, show help
    if not args.file:
        parser.print_help()
        return 0

    # Check if file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1

    # Read and execute the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        run_aigo_code(code)
        return 0

    except FileNotFoundError:
        print(f"Error: Could not read file '{args.file}'", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def run_from_cli():
    """Alternative entry point for aigo-run command"""
    sys.exit(main())


def repl():
    """Entry point for REPL command"""
    from .repl import main as repl_main
    sys.exit(repl_main())


if __name__ == "__main__":
    sys.exit(main())
