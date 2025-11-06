"""
AIGo Standard Library - File System Module

File system operations for AIGo programs.

This module provides file system operations including:
- File reading and writing
- Directory operations
- Path manipulation
- File metadata
- File system queries

Usage in AIGo:
    import std.fs

    let content: string = fs.read_file("example.txt")
    fs.write_file("output.txt", "Hello, AIGo!")
    let exists: bool = fs.exists("file.txt")
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
import stat


class FSModule:
    """AIGo File System standard library module."""

    # File operations

    @staticmethod
    def read_file(filepath: str, encoding: str = "utf-8") -> str:
        """
        Read entire file as string.

        Args:
            filepath: Path to file
            encoding: Text encoding (default: utf-8)

        Returns:
            File contents as string

        Raises:
            ValueError: If file not found or read error
        """
        try:
            with open(filepath, "r", encoding=encoding) as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"fs.read_file: file not found - {filepath}")
        except Exception as e:
            raise ValueError(f"fs.read_file: error reading file - {e}")

    @staticmethod
    def write_file(filepath: str, content: str, encoding: str = "utf-8") -> None:
        """
        Write string to file (overwrites if exists).

        Args:
            filepath: Path to file
            content: Content to write
            encoding: Text encoding (default: utf-8)

        Raises:
            ValueError: If write error
        """
        try:
            with open(filepath, "w", encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            raise ValueError(f"fs.write_file: error writing file - {e}")

    @staticmethod
    def append_file(filepath: str, content: str, encoding: str = "utf-8") -> None:
        """
        Append string to file.

        Args:
            filepath: Path to file
            content: Content to append
            encoding: Text encoding (default: utf-8)

        Raises:
            ValueError: If write error
        """
        try:
            with open(filepath, "a", encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            raise ValueError(f"fs.append_file: error appending to file - {e}")

    @staticmethod
    def read_lines(filepath: str, encoding: str = "utf-8") -> List[str]:
        """
        Read file as list of lines.

        Args:
            filepath: Path to file
            encoding: Text encoding (default: utf-8)

        Returns:
            List of lines (without newlines)

        Raises:
            ValueError: If file not found or read error
        """
        try:
            with open(filepath, "r", encoding=encoding) as f:
                return [line.rstrip("\n") for line in f]
        except FileNotFoundError:
            raise ValueError(f"fs.read_lines: file not found - {filepath}")
        except Exception as e:
            raise ValueError(f"fs.read_lines: error reading file - {e}")

    @staticmethod
    def write_lines(filepath: str, lines: List[str], encoding: str = "utf-8") -> None:
        """
        Write list of lines to file.

        Args:
            filepath: Path to file
            lines: Lines to write
            encoding: Text encoding (default: utf-8)

        Raises:
            ValueError: If write error
        """
        try:
            with open(filepath, "w", encoding=encoding) as f:
                for line in lines:
                    f.write(line + "\n")
        except Exception as e:
            raise ValueError(f"fs.write_lines: error writing file - {e}")

    @staticmethod
    def read_bytes(filepath: str) -> bytes:
        """
        Read file as bytes.

        Args:
            filepath: Path to file

        Returns:
            File contents as bytes

        Raises:
            ValueError: If file not found or read error
        """
        try:
            with open(filepath, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"fs.read_bytes: file not found - {filepath}")
        except Exception as e:
            raise ValueError(f"fs.read_bytes: error reading file - {e}")

    @staticmethod
    def write_bytes(filepath: str, content: bytes) -> None:
        """
        Write bytes to file.

        Args:
            filepath: Path to file
            content: Bytes to write

        Raises:
            ValueError: If write error
        """
        try:
            with open(filepath, "wb") as f:
                f.write(content)
        except Exception as e:
            raise ValueError(f"fs.write_bytes: error writing file - {e}")

    # File metadata

    @staticmethod
    def exists(path: str) -> bool:
        """
        Check if path exists.

        Args:
            path: Path to check

        Returns:
            True if path exists
        """
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        """
        Check if path is a file.

        Args:
            path: Path to check

        Returns:
            True if path is a file
        """
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        """
        Check if path is a directory.

        Args:
            path: Path to check

        Returns:
            True if path is a directory
        """
        return os.path.isdir(path)

    @staticmethod
    def is_link(path: str) -> bool:
        """
        Check if path is a symbolic link.

        Args:
            path: Path to check

        Returns:
            True if path is a symbolic link
        """
        return os.path.islink(path)

    @staticmethod
    def file_size(filepath: str) -> int:
        """
        Get file size in bytes.

        Args:
            filepath: Path to file

        Returns:
            File size in bytes

        Raises:
            ValueError: If file not found
        """
        try:
            return os.path.getsize(filepath)
        except FileNotFoundError:
            raise ValueError(f"fs.file_size: file not found - {filepath}")

    @staticmethod
    def modified_time(path: str) -> float:
        """
        Get last modified time as Unix timestamp.

        Args:
            path: Path to file or directory

        Returns:
            Last modified timestamp

        Raises:
            ValueError: If path not found
        """
        try:
            return os.path.getmtime(path)
        except FileNotFoundError:
            raise ValueError(f"fs.modified_time: path not found - {path}")

    @staticmethod
    def created_time(path: str) -> float:
        """
        Get creation time as Unix timestamp.

        Args:
            path: Path to file or directory

        Returns:
            Creation timestamp

        Raises:
            ValueError: If path not found
        """
        try:
            return os.path.getctime(path)
        except FileNotFoundError:
            raise ValueError(f"fs.created_time: path not found - {path}")

    # Directory operations

    @staticmethod
    def list_dir(dirpath: str) -> List[str]:
        """
        List directory contents.

        Args:
            dirpath: Path to directory

        Returns:
            List of filenames

        Raises:
            ValueError: If directory not found
        """
        try:
            return os.listdir(dirpath)
        except FileNotFoundError:
            raise ValueError(f"fs.list_dir: directory not found - {dirpath}")
        except Exception as e:
            raise ValueError(f"fs.list_dir: error listing directory - {e}")

    @staticmethod
    def list_files(dirpath: str) -> List[str]:
        """
        List files in directory (not subdirectories).

        Args:
            dirpath: Path to directory

        Returns:
            List of file paths
        """
        try:
            entries = os.listdir(dirpath)
            return [e for e in entries if os.path.isfile(os.path.join(dirpath, e))]
        except Exception as e:
            raise ValueError(f"fs.list_files: error - {e}")

    @staticmethod
    def list_dirs(dirpath: str) -> List[str]:
        """
        List subdirectories in directory.

        Args:
            dirpath: Path to directory

        Returns:
            List of directory names
        """
        try:
            entries = os.listdir(dirpath)
            return [e for e in entries if os.path.isdir(os.path.join(dirpath, e))]
        except Exception as e:
            raise ValueError(f"fs.list_dirs: error - {e}")

    @staticmethod
    def walk(dirpath: str) -> List[Tuple[str, List[str], List[str]]]:
        """
        Recursively walk directory tree.

        Args:
            dirpath: Path to directory

        Returns:
            List of (dirpath, dirnames, filenames) tuples
        """
        return list(os.walk(dirpath))

    @staticmethod
    def make_dir(dirpath: str, parents: bool = False) -> None:
        """
        Create directory.

        Args:
            dirpath: Path to directory
            parents: Create parent directories if needed (default: False)

        Raises:
            ValueError: If error creating directory
        """
        try:
            if parents:
                os.makedirs(dirpath, exist_ok=True)
            else:
                os.mkdir(dirpath)
        except Exception as e:
            raise ValueError(f"fs.make_dir: error creating directory - {e}")

    @staticmethod
    def remove_dir(dirpath: str, recursive: bool = False) -> None:
        """
        Remove directory.

        Args:
            dirpath: Path to directory
            recursive: Remove recursively (default: False)

        Raises:
            ValueError: If error removing directory
        """
        try:
            if recursive:
                shutil.rmtree(dirpath)
            else:
                os.rmdir(dirpath)
        except Exception as e:
            raise ValueError(f"fs.remove_dir: error removing directory - {e}")

    # File operations

    @staticmethod
    def copy_file(src: str, dst: str) -> None:
        """
        Copy file.

        Args:
            src: Source file path
            dst: Destination file path

        Raises:
            ValueError: If error copying file
        """
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            raise ValueError(f"fs.copy_file: error copying file - {e}")

    @staticmethod
    def move_file(src: str, dst: str) -> None:
        """
        Move/rename file.

        Args:
            src: Source file path
            dst: Destination file path

        Raises:
            ValueError: If error moving file
        """
        try:
            shutil.move(src, dst)
        except Exception as e:
            raise ValueError(f"fs.move_file: error moving file - {e}")

    @staticmethod
    def remove_file(filepath: str) -> None:
        """
        Delete file.

        Args:
            filepath: Path to file

        Raises:
            ValueError: If error deleting file
        """
        try:
            os.remove(filepath)
        except Exception as e:
            raise ValueError(f"fs.remove_file: error deleting file - {e}")

    @staticmethod
    def rename(old_path: str, new_path: str) -> None:
        """
        Rename file or directory.

        Args:
            old_path: Current path
            new_path: New path

        Raises:
            ValueError: If error renaming
        """
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            raise ValueError(f"fs.rename: error renaming - {e}")

    # Path operations

    @staticmethod
    def join_path(*parts: str) -> str:
        """
        Join path parts.

        Args:
            *parts: Path parts to join

        Returns:
            Joined path
        """
        return os.path.join(*parts)

    @staticmethod
    def absolute_path(path: str) -> str:
        """
        Get absolute path.

        Args:
            path: Relative or absolute path

        Returns:
            Absolute path
        """
        return os.path.abspath(path)

    @staticmethod
    def basename(path: str) -> str:
        """
        Get basename (filename) from path.

        Args:
            path: File path

        Returns:
            Basename

        Example:
            basename("/path/to/file.txt") -> "file.txt"
        """
        return os.path.basename(path)

    @staticmethod
    def dirname(path: str) -> str:
        """
        Get directory name from path.

        Args:
            path: File path

        Returns:
            Directory name

        Example:
            dirname("/path/to/file.txt") -> "/path/to"
        """
        return os.path.dirname(path)

    @staticmethod
    def extension(path: str) -> str:
        """
        Get file extension.

        Args:
            path: File path

        Returns:
            Extension including dot (e.g., ".txt")

        Example:
            extension("file.txt") -> ".txt"
        """
        return os.path.splitext(path)[1]

    @staticmethod
    def stem(path: str) -> str:
        """
        Get filename without extension.

        Args:
            path: File path

        Returns:
            Filename without extension

        Example:
            stem("file.txt") -> "file"
        """
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def split_path(path: str) -> Tuple[str, str]:
        """
        Split path into directory and basename.

        Args:
            path: File path

        Returns:
            Tuple of (directory, basename)

        Example:
            split_path("/path/to/file.txt") -> ("/path/to", "file.txt")
        """
        return os.path.split(path)

    @staticmethod
    def expand_user(path: str) -> str:
        """
        Expand ~ in path to user home directory.

        Args:
            path: Path with ~

        Returns:
            Expanded path
        """
        return os.path.expanduser(path)

    @staticmethod
    def cwd() -> str:
        """
        Get current working directory.

        Returns:
            Current working directory path
        """
        return os.getcwd()

    @staticmethod
    def home_dir() -> str:
        """
        Get user home directory.

        Returns:
            Home directory path
        """
        return str(Path.home())

    @staticmethod
    def temp_dir() -> str:
        """
        Get temporary directory.

        Returns:
            Temporary directory path
        """
        import tempfile
        return tempfile.gettempdir()


# Create module instance
fs_module = FSModule()

__all__ = ["FSModule", "fs_module"]
