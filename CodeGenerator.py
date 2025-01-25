class CodeGenerator:
    def __init__(self):
        self.code = []

    def generate(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.generate(statement)
        elif isinstance(node, Assignment):
            self.generate(node.expression)
            self.code.append(f"{node.identifier} = {self.code.pop()}")
        elif isinstance(node, Conditional):
            self.generate(node.condition)
            self.code.append(f"if {self.code.pop()}:")
            for stmt in node.true_branch:
                self.generate(stmt)
            if node.false_branch:
                self.code.append("else:")
                for stmt in node.false_branch:
                    self.generate(stmt)
        elif isinstance(node, Loop):
            self.generate(node.start)
            start = self.code.pop()
            self.generate(node.end)
            end = self.code.pop()
            self.code.append(f"for {node.identifier} in range({start}, {end} + 1):")
            for stmt in node.body.statements:
                self.generate(stmt)
        elif isinstance(node, PrintStatement):
            self.generate(node.expression)
            self.code.append(f"print({self.code.pop()})")
        elif isinstance(node, ReturnStatement):
            self.generate(node.expression)
            self.code.append(f"return {self.code.pop()}")
        elif isinstance(node, CallStatement):
            args = [self.generate(arg) for arg in node.args]
            self.code.append(f"{node.procedure_name}({', '.join(args)})")
        elif isinstance(node, ProcedureDefinition):
            self.code.append(f"def {node.name}({', '.join(node.params)}):")
            for stmt in node.body:
                self.generate(stmt)
        elif isinstance(node, ProcedureCall):
            args = [self.generate(arg) for arg in node.args]
            self.code.append(f"{node.name}({', '.join(args)})")
        elif isinstance(node, BinaryOperation):
            self.generate(node.left)
            left = self.code.pop()
            self.generate(node.right)
            right = self.code.pop()
            self.code.append(f"({left} {node.operator} {right})")
        elif isinstance(node, Variable):
            self.code.append(node.name)
        elif isinstance(node, Literal):
            self.code.append(repr(node.value))

    def get_code(self):
        return "\n".join(self.code)
