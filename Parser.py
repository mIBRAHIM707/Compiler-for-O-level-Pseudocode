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
    
    def advance(self):
        if self.position < len(self.tokens):
            self.position += 1

    def match(self, expected_type):
        if self.current_token() and self.current_token()[0] == expected_type:
            token = self.current_token()
            self.advance()  # Consume the token
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, found {self.current_token()}")


    def parse_program(self):
        statements = []
        while self.current_token():
            token = self.current_token()
            if token[0] == "KEYWORD" and token[1] == "ENDPROCEDURE":
                break  # End the procedure parsing
            statements.append(self.parse_statement())
        return statements


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
            elif token[1] == "ENDFOR":
                # Simply consume the ENDFOR token and stop parsing
                print("ENDFOR encountered. Ending loop block.")  # Debugging print
                self.match("KEYWORD")  # Consume ENDFOR
                return None  # No statement to return for ENDFOR
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
        body = []  # Collect statements in the loop body
        while self.current_token()[1] != "ENDFOR":  # Stop parsing at ENDFOR
            body.append(self.parse_statement())
        self.match("KEYWORD")  # Consume ENDFOR
        return Loop(identifier, start, end, Program(body))  # Return loop with body

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
        name = self.match("IDENTIFIER")[1]  # Match the procedure name (e.g., CalculateSum)
        self.match("DELIMITER")  # Match '('
        self.match("DELIMITER")  # Match ')'
        
        # Parse procedure parameters or just continue if none
        self.match("KEYWORD")  # Match FOR (if applicable)
        
        body = self.parse_program()  # Parse the procedure body
        
        self.match("KEYWORD")  # Match ENDPROCEDURE
        
        return Procedure(name, body)
