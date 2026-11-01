"""
AST Nodes, Recursive-Descent Parser, and Tree-Walking Evaluator for MiniLang.
"""
from typing import List, Any, Dict, Optional
from .lexer import Lexer, Token, TokenType

# --- AST Node Definitions ---
class ASTNode: pass

class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, name: str, expr: ASTNode):
        self.name = name
        self.expr = expr

class AssignNode(ASTNode):
    def __init__(self, name: str, expr: ASTNode):
        self.name = name
        self.expr = expr

class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

# --- Recursive-Descent Parser ---
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected: TokenType) -> Token:
        t = self.peek()
        if t.type != expected:
            raise SyntaxError(f"Line {t.line}: Expected {expected}, got {t.type} ('{t.value}')")
        self.pos += 1
        return t

    def parse(self) -> ProgramNode:
        stmts = []
        while self.peek().type != TokenType.EOF:
            stmts.append(self.parse_statement())
        return ProgramNode(stmts)

    def parse_statement(self) -> ASTNode:
        t = self.peek()
        if t.type == TokenType.LET:
            self.consume(TokenType.LET)
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.EQUAL)
            expr = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return VarDeclNode(name, expr)
        elif t.type == TokenType.PRINT:
            self.consume(TokenType.PRINT)
            expr = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return PrintNode(expr)
        elif t.type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            cond = self.parse_expression()
            self.consume(TokenType.LBRACE)
            body = []
            while self.peek().type != TokenType.RBRACE:
                body.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            return WhileNode(cond, body)
        elif t.type == TokenType.IF:
            self.consume(TokenType.IF)
            cond = self.parse_expression()
            self.consume(TokenType.LBRACE)
            then_b = []
            while self.peek().type != TokenType.RBRACE:
                then_b.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            else_b = None
            if self.peek().type == TokenType.ELSE:
                self.consume(TokenType.ELSE)
                self.consume(TokenType.LBRACE)
                else_b = []
                while self.peek().type != TokenType.RBRACE:
                    else_b.append(self.parse_statement())
                self.consume(TokenType.RBRACE)
            return IfNode(cond, then_b, else_b)
        elif t.type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.EQUAL)
            expr = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return AssignNode(name, expr)
        else:
            raise SyntaxError(f"Unexpected statement token: {t}")

    def parse_expression(self) -> ASTNode:
        node = self.parse_equality()
        return node

    def parse_equality(self) -> ASTNode:
        node = self.parse_relational()
        while self.peek().type in (TokenType.EQUAL_EQUAL,):
            op = self.consume(self.peek().type).value
            node = BinaryOpNode(node, op, self.parse_relational())
        return node

    def parse_relational(self) -> ASTNode:
        node = self.parse_term()
        while self.peek().type in (TokenType.LESS, TokenType.GREATER):
            op = self.consume(self.peek().type).value
            node = BinaryOpNode(node, op, self.parse_term())
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.peek().type).value
            node = BinaryOpNode(node, op, self.parse_factor())
        return node

    def parse_factor(self) -> ASTNode:
        node = self.parse_primary()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.consume(self.peek().type).value
            node = BinaryOpNode(node, op, self.parse_primary())
        return node

    def parse_primary(self) -> ASTNode:
        t = self.peek()
        if t.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumberNode(float(t.value))
        elif t.type == TokenType.IDENTIFIER:
            self.consume(TokenType.IDENTIFIER)
            return VariableNode(t.value)
        elif t.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token in expression: {t}")

# --- Interpreter Environment ---
class Interpreter:
    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.output_log: List[Any] = []

    def eval(self, node: ASTNode) -> Any:
        if isinstance(node, ProgramNode):
            for s in node.statements:
                self.eval(s)
        elif isinstance(node, VarDeclNode):
            val = self.eval(node.expr)
            self.env[node.name] = val
        elif isinstance(node, AssignNode):
            val = self.eval(node.expr)
            self.env[node.name] = val
        elif isinstance(node, PrintNode):
            val = self.eval(node.expr)
            self.output_log.append(val)
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, VariableNode):
            if node.name not in self.env:
                raise NameError(f"Undefined variable: '{node.name}'")
            return self.env[node.name]
        elif isinstance(node, BinaryOpNode):
            l = self.eval(node.left)
            r = self.eval(node.right)
            if node.op == '+': return l + r
            elif node.op == '-': return l - r
            elif node.op == '*': return l * r
            elif node.op == '/': return l / r
            elif node.op == '<': return 1.0 if l < r else 0.0
            elif node.op == '>': return 1.0 if l > r else 0.0
            elif node.op == '==': return 1.0 if l == r else 0.0
        elif isinstance(node, WhileNode):
            while self.eval(node.condition) != 0.0:
                for s in node.body:
                    self.eval(s)
        elif isinstance(node, IfNode):
            cond = self.eval(node.condition)
            if cond != 0.0:
                for s in node.then_branch:
                    self.eval(s)
            elif node.else_branch:
                for s in node.else_branch:
                    self.eval(s)
