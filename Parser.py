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

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"

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
            elif token[1] == "WHILE":
                return self.parse_while()
            elif token[1] == "PRINT":
                return self.parse_print()
            elif token[1] == "READ":
                return self.parse_read()
            elif token[1] == "PROCEDURE":
                return self.parse_procedure()
            elif token[1] == "CALL":
                return self.parse_call()
            elif token[1] == "RETURN":
                return self.parse_return()
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
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] in ("REL_OP", "OPERATOR"):
            operator = self.current_token()[1]
            self.match(self.current_token()[0])  # Match operator
            right = self.parse_term()
            left = (operator, left, right)  # Build a binary operation tree
        return left

        raise SyntaxError(f"Unexpected token in expression: {token}")

    def lookahead(self, n):
        if self.position + n < len(self.tokens):
            return self.tokens[self.position + n]
        return None
    
    def parse_print(self):
        self.match("KEYWORD")  # Match PRINT
        expression = self.parse_expression()  # Parse the expression to print
        return PrintStatement(expression)
    
    def parse_term(self):
        token = self.current_token()
        if token[0] in ("IDENTIFIER", "NUMBER", "STRING"):
            self.match(token[0])
            return token[1]
        elif token[0] == "DELIMITER" and token[1] == "(":
            self.match("DELIMITER")  # Match (
            expr = self.parse_expression()
            self.match("DELIMITER")  # Match )
            return expr
        raise SyntaxError(f"Unexpected token in term: {token}")


# Example token list
tokens = [
    ("IDENTIFIER", "x"),       # Assignment statement
    ("ASSIGN_OP", "<-"),       
    ("NUMBER", "5"),           
    ("KEYWORD", "IF"),         # Conditional statement
    ("IDENTIFIER", "x"),       
    ("REL_OP", ">"),           
    ("NUMBER", "0"),           
    ("KEYWORD", "THEN"),
    ("KEYWORD", "PRINT"),
    ("STRING", "\"Positive\""),
    ("KEYWORD", "ENDIF"),
    ("KEYWORD", "FOR"),        # Loop statement
    ("IDENTIFIER", "i"),       
    ("ASSIGN_OP", "<-"),       
    ("NUMBER", "1"),
    ("KEYWORD", "TO"),
    ("NUMBER", "10"),
    ("KEYWORD", "DO"),
    ("KEYWORD", "PRINT"),
    ("STRING", "\"i is \""),
    ("IDENTIFIER", "i"),
    ("KEYWORD", "ENDFOR"),
]

# Initialize parser with the tokens
parser = Parser(tokens)

# Parse the program
program = parser.parse_program()

# Print the program's abstract syntax tree (AST) or statements
print("Parsed Program:")
for statement in program.statements:
    print(statement)
