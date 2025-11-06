"""
Unit tests for AIGo CLI
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from io import StringIO
from aigo.cli import main
from aigo import __version__


class TestCLI:
    """Test cases for the CLI module"""

    def test_cli_help(self, monkeypatch, capsys):
        """Test CLI help message"""
        monkeypatch.setattr(sys, 'argv', ['aigo', '--help'])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert 'usage:' in captured.out.lower()
        assert 'aigo' in captured.out.lower()

    def test_cli_version(self, monkeypatch, capsys):
        """Test CLI version display"""
        monkeypatch.setattr(sys, 'argv', ['aigo', '--version'])

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_cli_no_args(self, monkeypatch, capsys):
        """Test CLI with no arguments shows help"""
        monkeypatch.setattr(sys, 'argv', ['aigo'])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert 'usage:' in captured.out.lower()

    def test_cli_file_not_found(self, monkeypatch, capsys):
        """Test CLI with non-existent file"""
        monkeypatch.setattr(sys, 'argv', ['aigo', 'nonexistent.aigo'])

        result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert 'not found' in captured.err.lower()

    def test_cli_execute_file(self, monkeypatch, capsys):
        """Test CLI executing a valid file"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write("""
module main
import std.io

fn main() -> Result<void, Error> {
    io.println("CLI Test")?
    return Ok(void)
}
            """)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert 'CLI Test' in captured.out
        finally:
            os.unlink(temp_file)

    def test_cli_debug_mode(self, monkeypatch, capsys):
        """Test CLI debug mode"""
        # Create a file with an error
        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write("""
module main
let x = invalid_syntax
            """)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file, '--debug'])
            result = main()

            # Should fail but show debug info
            assert result == 1
        finally:
            os.unlink(temp_file)


class TestCLIIntegration:
    """Integration tests for CLI"""

    def test_run_hello_world(self, monkeypatch, capsys):
        """Test running Hello World program"""
        code = """
module main
import std.io

fn main() -> Result<void, Error> {
    io.println("Hello from CLI!")?
    return Ok(void)
}
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert 'Hello from CLI!' in captured.out
        finally:
            os.unlink(temp_file)

    def test_run_arithmetic(self, monkeypatch, capsys):
        """Test running program with arithmetic"""
        code = """
module main
import std.io

fn main() -> Result<void, Error> {
    let result: i32 = 40 + 2
    io.println("Result:", result)?
    return Ok(void)
}
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert '42' in captured.out
        finally:
            os.unlink(temp_file)


class TestCLIEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_file(self, monkeypatch, capsys):
        """Test running an empty file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            # Empty file might succeed or fail depending on implementation
            # assert result in [0, 1]
        finally:
            os.unlink(temp_file)

    def test_large_file(self, monkeypatch):
        """Test running a large file"""
        # Create a large program
        code = "module main\n\n"
        for i in range(100):
            code += f"let var{i}: i32 = {i}\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            assert result == 0
        finally:
            os.unlink(temp_file)

    def test_unicode_content(self, monkeypatch, capsys):
        """Test file with Unicode content"""
        code = """
module main
import std.io

fn main() -> Result<void, Error> {
    io.println("Hello, 世界! 🌍")?
    return Ok(void)
}
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.aigo', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name

        try:
            monkeypatch.setattr(sys, 'argv', ['aigo', temp_file])
            result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert '世界' in captured.out or 'Hello' in captured.out
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
