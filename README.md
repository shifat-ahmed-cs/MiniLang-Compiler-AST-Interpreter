# MiniLang: End-to-End Compiler & Virtual Machine Architecture

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI: Passing](https://img.shields.io/badge/build-passing-brightgreen.svg)](.github/workflows/ci.yml)
[![Domain: Compilers](https://img.shields.io/badge/domain-Compiler%20Design-darkgreen.svg)]()
[![Academic: BRACU CSE420](https://img.shields.io/badge/course-CSE%20420-orange.svg)]()

## 📌 Course Context: CSE 420 (Compiler Design)
*Department of Computer Science and Engineering, BRAC University*  
**Core Principles:** Lexical Analysis (DFA Tokenizer), Context-Free Grammar Parsing (Recursive-Descent), Abstract Syntax Tree (AST) Construction, Scope Resolution, and Intermediate Execution.

---

## 🎯 Compiler Pipeline

```
Source Code -> [Lexer] -> Tokens -> [Parser] -> AST -> [Interpreter] -> Execution Output
```

1. **Handwritten Lexical Scanner:**
   - Converts source text into strongly-typed token streams (`Token(TokenType, value, line)`).
   - Handles variable identifiers, keywords, numeric literals, and comments.
2. **Recursive-Descent AST Parser:**
   - Implements operator precedence climbing (Expressions $\to$ Terms $\to$ Factors $\to$ Primaries).
   - Generates typed AST hierarchy (`ProgramNode`, `IfNode`, `WhileNode`, `AssignNode`).
3. **Tree-Walking Evaluator:**
   - Scoped symbol table environment managing runtime variables, conditional branching, and loops.

---

## 🚀 Quickstart & Testing
```bash
# Run demonstration
python main.py

# Run unit tests
python -m unittest discover -s tests
```
