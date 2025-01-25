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
    pass

class Literal(Expression):
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
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOperation(Expression):
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
            self.advance()
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, found {self.current_token()} at position {self.position}")

    def parse_program(self):
        statements = []
        while self.current_token():
            token = self.current_token()
            if token[0] == "KEYWORD" and token[1] == "ENDPROCEDURE":
                break
            if token[0] == "COMMENT":
                self.advance()
                continue
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()

        if token[0] == "IDENTIFIER":
            var_name = token[1]

            if self.lookahead(1):
                next_token = self.lookahead(1)

                if next_token[0] == "ASSIGN_OP":
                    self.match("IDENTIFIER")
                    self.match("ASSIGN_OP")
                    rhs = self.parse_expression()
                    return Assignment(var_name, rhs)

                elif next_token[0] == "DELIMITER" and next_token[1] == "(":
                    return self.parse_procedure_call()

            return IdentifierStatement(token[1])

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

        raise SyntaxError(f"Unexpected token: {token} at position {self.position}")

    def parse_assignment(self):
        left_token = self.current_token()
        if left_token[0] != "IDENTIFIER":
            raise SyntaxError(f"Expected identifier, found {left_token} at position {self.position}")

        identifier = left_token[1]
        self.match("IDENTIFIER")
        assign_op_token = self.current_token()
        if assign_op_token[0] != "ASSIGN_OP" or assign_op_token[1] != "<-":
            raise SyntaxError(f"Expected assignment operator, found {assign_op_token} at position {self.position}")
        self.match("ASSIGN_OP")
        next_token = self.current_token()
        if next_token[0] == "IDENTIFIER":
            lookahead_token = self.lookahead(1)
            if lookahead_token and lookahead_token[0] == "DELIMITER" and lookahead_token[1] == "(":
                procedure_call = self.parse_procedure_call()
                return Assignment(identifier, procedure_call)
        expression = self.parse_expression()
        return Assignment(identifier, expression)

    def parse_conditional(self):
        self.match("KEYWORD")
        condition = self.parse_expression()
        self.match("KEYWORD")
        true_branch = []
        while self.current_token() and self.current_token()[1] not in ("ELSE", "ENDIF"):
            true_branch.append(self.parse_statement())
        false_branch = None
        if self.current_token() and self.current_token()[1] == "ELSE":
            self.match("KEYWORD")
            false_branch = []
            while self.current_token() and self.current_token()[1] != "ENDIF":
                false_branch.append(self.parse_statement())
        self.match("KEYWORD")
        return Conditional(condition, true_branch, false_branch)

    def parse_loop(self):
        self.match("KEYWORD")
        identifier = self.current_token()[1]
        self.match("IDENTIFIER")
        self.match("ASSIGN_OP")
        start = self.parse_expression()
        self.match("KEYWORD")
        end = self.parse_expression()
        self.match("KEYWORD")
        body = []
        while self.current_token()[1] != "ENDFOR":
            body.append(self.parse_statement())
        self.match("KEYWORD")
        return Loop(identifier, start, end, Program(body))

    def parse_expression(self):
        left = self.parse_primary()
        while self.current_token() and self.current_token()[0] in ("OPERATOR", "REL_OP"):
            op_token = self.current_token()
            self.advance()
            right = self.parse_primary()
            left = BinaryOperation(left, op_token[1], right)
        return left

    def parse_primary(self):
        token = self.current_token()

        if token[0] == "NUMBER":
            self.match("NUMBER")
            return Literal(token[1])

        elif token[0] == "STRING":
            self.match("STRING")
            return Literal(token[1])

        elif token[0] == "IDENTIFIER":
            if self.lookahead(1) and self.lookahead(1)[0] == "DELIMITER" and self.lookahead(1)[1] == "(":
                return self.parse_procedure_call()
            self.match("IDENTIFIER")
            return Variable(token[1])

        elif token[0] == "DELIMITER" and token[1] == "(":
            self.match("DELIMITER")
            expr = self.parse_expression()
            if self.current_token() is None or self.current_token()[0] != "DELIMITER" or self.current_token()[1] != ")":
                raise SyntaxError(f"Expected ')', but got {self.current_token()} at position {self.position}")
            self.match("DELIMITER")
            return expr

        raise SyntaxError(f"Unexpected token in primary: {token} at position {self.position}")

    def lookahead(self, n):
        if self.position + n < len(self.tokens):
            return self.tokens[self.position + n]
        return None

    def parse_print(self):
        self.match("KEYWORD")
        expression = self.parse_expression()
        return PrintStatement(expression)
    
    def parse_term(self):
        token = self.current_token()
        if token[0] in ("IDENTIFIER", "NUMBER", "STRING"):
            self.match(token[0])
            return token[1]
        elif token[0] == "DELIMITER" and token[1] == "(":
            self.match("DELIMITER")
            expr = self.parse_expression()
            self.match("DELIMITER")
            return expr
        raise SyntaxError(f"Unexpected token in term: {token} at position {self.position}")
    
    def parse_return(self):
        self.match("KEYWORD")
        expression = self.parse_expression()
        return ReturnStatement(expression)
    
    def parse_call(self):
        self.match("KEYWORD")
        procedure_name = self.current_token()[1]
        self.match("IDENTIFIER")
        self.match("DELIMITER")
        args = []
        while self.current_token() and self.current_token()[0] != "DELIMITER":
            args.append(self.parse_expression())
            if self.current_token() and self.current_token()[0] == "DELIMITER" and self.current_token()[1] == ",":
                self.match("DELIMITER")
        self.match("DELIMITER")
        return CallStatement(procedure_name, args)
    
    def parse_procedure(self):
        self.match("KEYWORD")
        name_token = self.match("IDENTIFIER")
        name = name_token[1]
        self.match("DELIMITER")
        params = []
        while self.current_token()[0] == "IDENTIFIER":
            params.append(self.match("IDENTIFIER")[1])
            if self.current_token()[1] == ",":
                self.match("DELIMITER")
        self.match("DELIMITER")
        body = []
        while self.current_token() and self.current_token()[1] != "ENDPROCEDURE":
            body.append(self.parse_statement())
        self.match("KEYWORD")
        return ProcedureDefinition(name, params, body)
    
    def parse_procedure_call(self):
        token = self.current_token()
        if token[0] != "IDENTIFIER":
            raise SyntaxError(f"Expected an identifier, but got {token} at position {self.position}")
        procedure_name = token[1]
        self.match("IDENTIFIER")
        token = self.current_token()
        if token[0] != "DELIMITER" or token[1] != "(":
            raise SyntaxError(f"Expected '(', but got {token} at position {self.position}")
        self.match("DELIMITER")
        arguments = []
        while True:
            token = self.current_token()
            if token[0] == "DELIMITER" and token[1] == ")":
                break
            arguments.append(self.parse_expression())
            token = self.current_token()
            if token[0] == "DELIMITER" and token[1] == ",":
                self.match("DELIMITER")
            elif token[0] == "DELIMITER" and token[1] == ")":
                break
            else:
                raise SyntaxError(f"Unexpected token while parsing arguments: {token} at position {self.position}")
        token = self.current_token()
        if token[0] != "DELIMITER" or token[1] != ")":
            raise SyntaxError(f"Expected ')', but got {token} at position {self.position}")
        self.match("DELIMITER")
        return ProcedureCall(procedure_name, arguments)

    def parse_read(self):
        self.match("KEYWORD")
        identifier = self.match("IDENTIFIER")[1]
        return ReadStatement(identifier)
