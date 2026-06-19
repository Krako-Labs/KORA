import os
import subprocess
import sys
from setuptools import setup

rust_extensions = []

# Check if cargo is available in the system path
try:
    subprocess.run(["cargo", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    try:
        from setuptools_rust import RustExtension, Binding
        rust_extensions = [
            RustExtension("kora_rust", "kora-rust/Cargo.toml", binding=Binding.PyO3)
        ]
    except ImportError:
        print("Warning: setuptools-rust is not installed. Building without Rust extension.", file=sys.stderr)
except (subprocess.SubprocessError, FileNotFoundError):
    print("Warning: cargo not found. Building without Rust extension kora_rust.", file=sys.stderr)

setup(
    rust_extensions=rust_extensions,
)
