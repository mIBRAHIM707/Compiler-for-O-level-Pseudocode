from parser import Program, Assignment, Conditional, Loop, PrintStatement, ReturnStatement, CallStatement, ProcedureDefinition, ProcedureCall, BinaryOperation, Variable, Literal

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.analyze(statement)
        elif isinstance(node, Assignment):
            self.analyze(node.expression)
            self.symbol_table[node.identifier] = self.get_type(node.expression)
        elif isinstance(node, Conditional):
            self.analyze(node.condition)
            for stmt in node.true_branch:
                self.analyze(stmt)
            if node.false_branch:
                for stmt in node.false_branch:
                    self.analyze(stmt)
        elif isinstance(node, Loop):
            self.analyze(node.start)
            self.analyze(node.end)
            for stmt in node.body.statements:
                self.analyze(stmt)
        elif isinstance(node, PrintStatement):
            self.analyze(node.expression)
        elif isinstance(node, ReturnStatement):
            self.analyze(node.expression)
        elif isinstance(node, CallStatement):
            for arg in node.args:
                self.analyze(arg)
        elif isinstance(node, ProcedureDefinition):
            for stmt in node.body:
                self.analyze(stmt)
        elif isinstance(node, ProcedureCall):
            for arg in node.args:
                self.analyze(arg)
        elif isinstance(node, BinaryOperation):
            self.analyze(node.left)
            self.analyze(node.right)
        elif isinstance(node, Variable):
            if node.name not in self.symbol_table:
                raise NameError(f"Variable {node.name} not declared")
        elif isinstance(node, Literal):
            pass

    def get_type(self, node):
        if isinstance(node, Literal):
            return type(node.value)
        elif isinstance(node, Variable):
            return self.symbol_table.get(node.name, None)
        elif isinstance(node, BinaryOperation):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            if left_type != right_type:
                raise TypeError("Type mismatch in binary operation")
            return left_type
        return None
