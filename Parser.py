import AST_Tree as a

class Program:
    def __init__(self, statements):
        self.statements = statements

class Assignment:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Conditional:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class Loop:
    def __init__(self, identifier, start, end, body):
        self.identifier = identifier
        self.start = start
        self.end = end
        self.body = body


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def match(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.position += 1
            return True
        return False

    def parse_program(self):
        statements = []
        while self.current_token():
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if token[0] == "IDENTIFIER" and self.lookahead(1)[0] == "ASSIGN_OP":
            return self.parse_assignment()
        elif token[0] == "KEYWORD":
            if token[1] == "IF":
                return self.parse_conditional()
            elif token[1] == "FOR":
                return self.parse_loop()
        raise SyntaxError(f"Unexpected token: {token}")

    def parse_assignment(self):
        identifier = self.current_token()[1]
        self.match("IDENTIFIER")
        self.match("ASSIGN_OP")
        expression = self.parse_expression()
        return Assignment(identifier, expression)

    def parse_conditional(self):
        self.match("KEYWORD")  # IF
        condition = self.parse_expression()  # Expression may contain a REL_OP
        self.match("KEYWORD")  # THEN
        true_branch = self.parse_program()
        false_branch = None
        if self.current_token() and self.current_token()[1] == "ELSE":
            self.match("KEYWORD")  # ELSE
            false_branch = self.parse_program()
        self.match("KEYWORD")  # ENDIF
        return Conditional(condition, true_branch, false_branch)

    def parse_loop(self):
        self.match("KEYWORD")  # FOR
        identifier = self.current_token()[1]
        self.match("IDENTIFIER")
        self.match("ASSIGN_OP")
        start = self.parse_expression()
        self.match("KEYWORD")  # TO
        end = self.parse_expression()
        self.match("KEYWORD")  # DO
        body = self.parse_program()
        self.match("KEYWORD")  # ENDFOR
        return Loop(identifier, start, end, body)

    def parse_expression(self):
        token = self.current_token()

        # Check for a relational operator (e.g., >, <, ==)
        if token[0] == "IDENTIFIER" or token[0] == "NUMBER":
            left = token[1]
            self.match(token[0])
            token = self.current_token()

            # Check for a relational operator
            if token and token[0] == "REL_OP":
                op = token[1]
                self.match("REL_OP")
                right = self.parse_expression()
                return (left, op, right)

            return left  # Return the identifier/number as an expression

        raise SyntaxError(f"Unexpected token in expression: {token}")

    def lookahead(self, n):
        if self.position + n < len(self.tokens):
            return self.tokens[self.position + n]
        return None


# Example usage
tokens = [
    ("IDENTIFIER", "x"),
    ("ASSIGN_OP", "<-"),
    ("NUMBER", "5"),
    ("KEYWORD", "IF"),
    ("IDENTIFIER", "x"),
    ("REL_OP", ">"),
    ("NUMBER", "0"),
    ("KEYWORD", "THEN"),
    ("KEYWORD", "PRINT"),
    ("STRING", "\"Positive\""),
    ("KEYWORD", "ENDIF")
]

parser = Parser(tokens)
program = parser.parse_program()
print(program)
