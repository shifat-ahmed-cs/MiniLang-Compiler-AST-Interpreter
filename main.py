"""
Entry point for CSE420_Compiler_Design.
Executes the comprehensive demonstration suite.
"""
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from examples.demo import main

if __name__ == "__main__":
    main()
