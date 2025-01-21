import AST_Tree as a

class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class Assignment:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Assignment({self.identifier} <- {self.expression})"

class Conditional:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"Conditional(IF {self.condition} THEN {self.true_branch} ELSE {self.false_branch})"

class Loop:
    def __init__(self, identifier, start, end, body):
        self.identifier = identifier
        self.start = start
        self.end = end
        self.body = body

    def __repr__(self):
        return f"Loop(FOR {self.identifier} <- {self.start} TO {self.end} DO {self.body})"

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Return({self.expression})"

class CallStatement:
    def __init__(self, procedure_name, args):
        self.procedure_name = procedure_name
        self.args = args

    def __repr__(self):
        return f"Call(procedure_name={self.procedure_name}, args={self.args})"

class ProcedureDefinition:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Procedure(name={self.name}, params={self.params}, body={self.body})"

class IdentifierStatement:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"IdentifierStatement(identifier={self.identifier})"


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
        print(f"Parsing statement: {token}")  # Debugging print

        if token[0] == "IDENTIFIER":
            # Handle assignment or standalone identifiers
            if self.lookahead(1) and self.lookahead(1)[0] == "ASSIGN_OP":
                return self.parse_assignment()
            else:
                # Treat standalone identifiers as valid statements
                identifier = token[1]
                self.match("IDENTIFIER")  # Consume the identifier
                print(f"Standalone identifier encountered: {identifier}")  # Debugging print
                return IdentifierStatement(identifier)
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

        # Parse the true branch until ELSE or ENDIF
        true_branch = []
        while self.current_token() and self.current_token()[1] not in ("ELSE", "ENDIF"):
            true_branch.append(self.parse_statement())

        false_branch = None
        if self.current_token() and self.current_token()[1] == "ELSE":
            self.match("KEYWORD")  # ELSE
            # Parse the false branch until ENDIF
            false_branch = []
            while self.current_token() and self.current_token()[1] != "ENDIF":
                false_branch.append(self.parse_statement())

        self.match("KEYWORD")  # ENDIF
        return Conditional(condition, true_branch, false_branch)


    def parse_loop(self):
        self.match("KEYWORD")  # FOR
        identifier = self.current_token()[1]
        print(f"Parsing loop with identifier: {identifier}")  # Debugging print
        self.match("IDENTIFIER")
        self.match("ASSIGN_OP")
        start = self.parse_expression()
        self.match("KEYWORD")  # TO
        end = self.parse_expression()
        self.match("KEYWORD")  # DO
        body = self.parse_program()  # Parse loop body
        print(f"Loop body parsed: {body}")  # Debugging print

        # Ensure that ENDFOR is expected after the loop body
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
    
    def parse_return(self):
        self.match("KEYWORD")  # Match RETURN
        expression = self.parse_expression()  # Parse the return value
        return ReturnStatement(expression)
    
    def parse_call(self):
        self.match("KEYWORD")  # Match CALL
        procedure_name = self.current_token()[1]
        self.match("IDENTIFIER")  # Match the procedure name
        self.match("DELIMITER")  # Match (
        args = []
        while self.current_token() and self.current_token()[0] != "DELIMITER":
            args.append(self.parse_expression())
            if self.current_token() and self.current_token()[0] == "DELIMITER" and self.current_token()[1] == ",":
                self.match("DELIMITER")
        self.match("DELIMITER")  # Match )
        return CallStatement(procedure_name, args)
    
    def parse_procedure(self):
        self.match("KEYWORD")  # Match PROCEDURE
        name = self.current_token()[1]
        self.match("IDENTIFIER")  # Match the procedure name
        self.match("DELIMITER")  # Match (
        params = []
        while self.current_token() and self.current_token()[0] == "IDENTIFIER":
            params.append(self.current_token()[1])
            self.match("IDENTIFIER")
            if self.current_token() and self.current_token()[0] == "DELIMITER" and self.current_token()[1] == ",":
                self.match("DELIMITER")
        self.match("DELIMITER")  # Match )
        body = self.parse_program()
        self.match("KEYWORD")  # Match ENDPROCEDURE
        return ProcedureDefinition(name, params, body)


# Example token list
tokens = [
    # ("IDENTIFIER", "x"),       # Assignment statement
    # ("ASSIGN_OP", "<-"),       
    # ("NUMBER", "5"),           
    # ("KEYWORD", "IF"),         # Conditional statement
    # ("IDENTIFIER", "x"),       
    # ("REL_OP", ">"),           
    # ("NUMBER", "0"),           
    # ("KEYWORD", "THEN"),
    # ("KEYWORD", "PRINT"),
    # ("STRING", "\"Positive\""),
    # ("KEYWORD", "ENDIF"),
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
