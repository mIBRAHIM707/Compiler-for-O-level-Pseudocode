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

class ProcedureCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"ProcedureCall(name={self.name}, args={self.args})"

class IdentifierStatement:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"IdentifierStatement(identifier={self.identifier})"

class ReadStatement:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"Read({self.identifier})"

class Expression:
    """Base class for all expressions."""
    pass

class Literal(Expression):
    """Represents a literal value (e.g., numbers or strings)."""
    def __init__(self, value):
        try:
            self.value = int(value)
        except ValueError:
            try:
                self.value = float(value)
            except ValueError:
                self.value = value

    def __repr__(self):
        return f"Literal({repr(self.value)})"

class Variable(Expression):
    """Represents a variable (identifier)."""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOperation(Expression):
    """Represents a binary operation (e.g., addition, subtraction)."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOperation({self.left} {self.operator} {self.right})"


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
            if token[0] == "COMMENT":
                self.advance()  # Skip comments
                continue
            statements.append(self.parse_statement())
        return Program(statements)  # Wrap in Program object

    def parse_statement(self):
        token = self.current_token()
        print(f"Parsing statement: {token}")  # Debugging print

        if token[0] == "IDENTIFIER":
            print(f"Found IDENTIFIER: {token[1]}")  # Debugging print for IDENTIFIER
            var_name = token[1]

            if self.lookahead(1):  # Look at the next token
                next_token = self.lookahead(1)
                print(f"Lookahead 1: {next_token}")  # Debugging print for the next token

                # Check if the next token is an ASSIGN_OP, indicating an assignment
                if next_token[0] == "ASSIGN_OP":
                    print("Detected assignment operation, parsing assignment.")  # Debugging print
                    self.match("IDENTIFIER")  # Consume the variable name
                    self.match("ASSIGN_OP")  # Consume the '<-'

                    # Parse the right-hand side (could be an expression or procedure call)
                    rhs = self.parse_expression()  # Assume parse_expression handles procedure calls
                    return Assignment(var_name, rhs)

                # Check if the next token is a DELIMITER '(' indicating a procedure call
                elif next_token[0] == "DELIMITER" and next_token[1] == "(":
                    print("Detected standalone procedure call, parsing procedure call.")  # Debugging print
                    return self.parse_procedure_call()

            print("No assignment or procedure call detected, treating as standalone identifier.")  # Debugging print
            return IdentifierStatement(token[1])

        # Handle other cases like IF, FOR, etc.
        elif token[0] == "KEYWORD":
            print(f"Found KEYWORD: {token[1]}")  # Debugging print for KEYWORD

            if token[1] == "IF":
                print("Parsing IF statement.")  # Debugging print
                return self.parse_conditional()
            elif token[1] == "FOR":
                print("Parsing FOR loop.")  # Debugging print
                return self.parse_loop()
            elif token[1] == "WHILE":
                print("Parsing WHILE loop.")  # Debugging print
                return self.parse_while()
            elif token[1] == "PRINT":
                print("Parsing PRINT statement.")  # Debugging print
                return self.parse_print()
            elif token[1] == "READ":
                print("Parsing READ statement.")  # Debugging print
                return self.parse_read()
            elif token[1] == "PROCEDURE":
                print("Parsing PROCEDURE declaration.")  # Debugging print
                return self.parse_procedure()
            elif token[1] == "CALL":
                print("Parsing CALL statement.")  # Debugging print
                return self.parse_call()
            elif token[1] == "RETURN":
                print("Parsing RETURN statement.")  # Debugging print
                return self.parse_return()
        
        # elif token[0] == "DELIMITER" and token[1] == "(":
        #             print("Detected standalone procefffffffdure call, parsing procedure call.")  # Debugging print
        #             return self.parse_procedure_call()

        raise SyntaxError(f"Unexpected token: {token}")

    def parse_assignment(self):
        # Parse the left-hand side identifier
        left_token = self.current_token()
        if left_token[0] != "IDENTIFIER":
            raise SyntaxError(f"Expected identifier, found {left_token}")

        identifier = left_token[1]  # Store the identifier

        # Consume the IDENTIFIER token
        self.match("IDENTIFIER")

        # Check if the next token is an ASSIGN_OP
        assign_op_token = self.current_token()
        if assign_op_token[0] != "ASSIGN_OP" or assign_op_token[1] != "<-":
            raise SyntaxError(f"Expected assignment operator, found {assign_op_token}")

        # Consume the ASSIGN_OP token
        self.match("ASSIGN_OP")

        # Now, check if the right-hand side is a procedure call or a regular expression
        next_token = self.current_token()
        if next_token[0] == "IDENTIFIER":  # Potential procedure call
            lookahead_token = self.lookahead(1)
            if lookahead_token and lookahead_token[0] == "DELIMITER" and lookahead_token[1] == "(":
                print(f"Detected procedure call for {identifier}, parsing procedure call.")  # Debugging print
                procedure_call = self.parse_procedure_call()
                return Assignment(identifier, procedure_call)

        # Otherwise, parse the right-hand side as a regular expression
        print(f"Parsing right-hand side expression for assignment to {identifier}.")  # Debugging print
        expression = self.parse_expression()

        # Return the assignment statement
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
        left = self.parse_primary()
        while self.current_token() and self.current_token()[0] in ("OPERATOR", "REL_OP"):
            op_token = self.current_token()
            self.advance()  # match() not strictly necessary here, but we skip the operator token
            right = self.parse_primary()
            left = BinaryOperation(left, op_token[1], right)
        return left

    def parse_primary(self):
        token = self.current_token()
        print(f"Parsing primary: {token}")  # Debugging print

        if token[0] == "NUMBER":
            # Handle literal numbers
            self.match("NUMBER")
            return Literal(token[1])

        elif token[0] == "STRING":
            # Handle literal strings
            self.match("STRING")
            return Literal(token[1])

        elif token[0] == "IDENTIFIER":
            # Look ahead to check for a procedure call
            if self.lookahead(1) and self.lookahead(1)[0] == "DELIMITER" and self.lookahead(1)[1] == "(":
                print(f"Detected procedure call in expression: {token[1]}")
                return self.parse_procedure_call()

            # Otherwise, it's a variable
            self.match("IDENTIFIER")
            return Variable(token[1])

        elif token[0] == "DELIMITER" and token[1] == "(":
            # Handle parenthesized expressions
            self.match("DELIMITER")
            expr = self.parse_expression()
            if self.current_token() is None or self.current_token()[0] != "DELIMITER" or self.current_token()[1] != ")":
                raise SyntaxError(f"Expected ')', but got {self.current_token()}")
            self.match("DELIMITER")
            return expr

        raise SyntaxError(f"Unexpected token in primary: {token}")

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
        print(f"Parsing procedure, current token: {self.current_token()}")

        self.match("KEYWORD")  # Match PROCEDURE
        name_token = self.match("IDENTIFIER")  # Match procedure name
        name = name_token[1]  # Extract the procedure name

        self.match("DELIMITER")  # Match '('
        params = []
        while self.current_token()[0] == "IDENTIFIER":  # Collect parameters
            params.append(self.match("IDENTIFIER")[1])
            if self.current_token()[1] == ",":
                self.match("DELIMITER")  # Match ',' if more params

        self.match("DELIMITER")  # Match ')'

        body = []
        while self.current_token() and self.current_token()[1] != "ENDPROCEDURE":
            body.append(self.parse_statement())

        self.match("KEYWORD")  # Match ENDPROCEDURE

        return ProcedureDefinition(name, params, body)
    
    def parse_procedure_call(self):
        print("-----------------------------------------------------")
        print(f"Starting procedure call parsing. Current token: {self.current_token()}")  # Entry debug

        # Ensure the current token is an identifier (procedure name)
        token = self.current_token()
        if token[0] != "IDENTIFIER":
            raise SyntaxError(f"Expected an identifier, but got {token}")
        procedure_name = token[1]
        print(f"Procedure name: {procedure_name}")
        self.match("IDENTIFIER")  # Consume the identifier

        # Now expect an opening parenthesis '('
        token = self.current_token()
        if token[0] != "DELIMITER" or token[1] != "(":
            raise SyntaxError(f"Expected '(', but got {token}")
        self.match("DELIMITER")  # Consume the '('
        print(f"Opening parenthesis detected. Current token: {self.current_token()}")

        # Parse arguments inside the parentheses (if any)
        arguments = []
        while True:
            token = self.current_token()
            if token[0] == "DELIMITER" and token[1] == ")":
                break  # End of arguments
            print(f"Parsing argument. Current token: {token}")
            arguments.append(self.parse_expression())  # Parse argument
            
            token = self.current_token()
            if token[0] == "DELIMITER" and token[1] == ",":
                self.match("DELIMITER")  # Consume the comma
                print(f"Comma detected. Continuing to next argument.")
            elif token[0] == "DELIMITER" and token[1] == ")":
                break
            else:
                raise SyntaxError(f"Unexpected token while parsing arguments: {token}")

        # Closing parenthesis
        token = self.current_token()
        if token[0] != "DELIMITER" or token[1] != ")":
            raise SyntaxError(f"Expected ')', but got {token}")
        self.match("DELIMITER")  # Consume the ')'
        print(f"Closing parenthesis detected. Procedure call parsing complete.")

        return ProcedureCall(procedure_name, arguments)

    def parse_read(self):
        self.match("KEYWORD")  # Match READ
        identifier = self.match("IDENTIFIER")[1]  # Match the identifier to read into
        return ReadStatement(identifier)
