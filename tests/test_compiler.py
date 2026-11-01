"""
Unit tests for MiniLang compiler stages.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.lexer import Lexer
from src.interpreter import Parser, Interpreter

class TestMiniLang(unittest.TestCase):
    def test_arithmetic_and_variables(self):
        src = "let x = 10; let y = 20; let z = x + y * 2; print z;"
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        interp = Interpreter()
        interp.eval(ast)
        self.assertEqual(interp.env["z"], 50.0)
        self.assertEqual(interp.output_log, [50.0])

    def test_while_loop(self):
        src = "let c = 0; while (c < 3) { c = c + 1; } print c;"
        ast = Parser(Lexer(src).tokenize()).parse()
        interp = Interpreter()
        interp.eval(ast)
        self.assertEqual(interp.env["c"], 3.0)

if __name__ == "__main__":
    unittest.main()
