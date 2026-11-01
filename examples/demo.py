"""
Demonstration of MiniLang: Lexing, Parsing, and Interpreting a Fibonacci Program.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import Lexer
from src.interpreter import Parser, Interpreter

def main():
    print("=" * 65)
    print("      MINILANG: FULL COMPILER & INTERPRETER PIPELINE          ")
    print("=" * 65)

    source_code = """
    # MiniLang Program: Calculate Factorial of 5
    let n = 5;
    let fact = 1;
    let i = 1;

    while (i < n + 1) {
        fact = fact * i;
        i = i + 1;
    }

    print fact;
    """

    print("[+] Source Code:")
    print(source_code.strip())

    # 1. Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print(f"\n[+] Lexical Analysis: Generated {len(tokens)} tokens.")

    # 2. Syntax Analysis (AST Construction)
    parser = Parser(tokens)
    ast = parser.parse()
    print("[+] Abstract Syntax Tree (AST) generated successfully.")

    # 3. Execution (Tree-Walking Interpretation)
    interpreter = Interpreter()
    interpreter.eval(ast)

    print(f"\n[+] Program Execution Output: {interpreter.output_log}")
    print(f"[+] Final Environment Variables: {interpreter.env}")
    print("=" * 65)

if __name__ == "__main__":
    main()
