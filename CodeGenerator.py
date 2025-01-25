from parser import Program, Assignment, Conditional, Loop, PrintStatement, ReturnStatement, CallStatement, ProcedureDefinition, ProcedureCall, BinaryOperation, Variable, Literal, ReadStatement

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def indent(self):
        return '    ' * self.indent_level

    def generate(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.generate(statement)
        elif isinstance(node, Assignment):
            self.generate(node.expression)
            self.code.append(f"{self.indent()}{node.identifier} = {self.code.pop()}")
        elif isinstance(node, Conditional):
            self.generate(node.condition)
            condition_code = self.code.pop()
            if " = " in condition_code:
                condition_code = condition_code.replace(" = ", " == ")
            self.code.append(f"{self.indent()}if {condition_code}:")
            self.indent_level += 1
            for stmt in node.true_branch:
                self.generate(stmt)
            self.indent_level -= 1
            if node.false_branch:
                self.code.append(f"{self.indent()}else:")
                self.indent_level += 1
                for stmt in node.false_branch:
                    self.generate(stmt)
                self.indent_level -= 1
        elif isinstance(node, Loop):
            self.generate(node.start)
            start = self.code.pop()
            self.generate(node.end)
            end = self.code.pop()
            self.code.append(f"{self.indent()}for {node.identifier} in range({start}, {end} + 1):")
            self.indent_level += 1
            for stmt in node.body.statements:
                self.generate(stmt)
            self.indent_level -= 1
        elif isinstance(node, PrintStatement):
            self.generate(node.expression)
            self.code.append(f"{self.indent()}print({self.code.pop()})")
        elif isinstance(node, ReturnStatement):
            self.generate(node.expression)
            self.code.append(f"{self.indent()}return {self.code.pop()}")
        elif isinstance(node, CallStatement):
            args = [self.generate(arg) for arg in node.args]
            self.code.append(f"{self.indent()}{node.procedure_name}({', '.join(args)})")
        elif isinstance(node, ProcedureDefinition):
            self.code.append(f"{self.indent()}def {node.name}({', '.join(node.params)}):")
            self.indent_level += 1
            for stmt in node.body:
                self.generate(stmt)
            self.indent_level -= 1
        elif isinstance(node, ProcedureCall):
            args = []
            for arg in node.args:
                self.generate(arg)
                args.append(self.code.pop())
            self.code.append(f"{self.indent()}{node.name}({', '.join(args)})")
        elif isinstance(node, BinaryOperation):
            self.generate(node.left)
            left = self.code.pop()
            self.generate(node.right)
            right = self.code.pop()
            self.code.append(f"({left} {node.operator} {right})")
        elif isinstance(node, Variable):
            self.code.append(node.name)
        elif isinstance(node, Literal):
            self.code.append(str(node.value))
        elif isinstance(node, ReadStatement):
            self.code.append(f"{self.indent()}{node.identifier} = input()")
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def get_code(self):
        return "\n".join(self.code)
