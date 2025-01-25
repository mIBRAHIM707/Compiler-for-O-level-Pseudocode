from parser import Program, Assignment, Conditional, Loop, PrintStatement, ReturnStatement, CallStatement, ProcedureDefinition, ProcedureCall, BinaryOperation, Variable, Literal

class Optimizer:
    def optimize(self, node):
        if isinstance(node, Program):
            optimized_statements = [self.optimize(stmt) for stmt in node.statements]
            return Program(optimized_statements)
        elif isinstance(node, Assignment):
            optimized_expression = self.optimize(node.expression)
            return Assignment(node.identifier, optimized_expression)
        elif isinstance(node, Conditional):
            optimized_condition = self.optimize(node.condition)
            optimized_true_branch = [self.optimize(stmt) for stmt in node.true_branch]
            optimized_false_branch = [self.optimize(stmt) for stmt in node.false_branch] if node.false_branch else None
            return Conditional(optimized_condition, optimized_true_branch, optimized_false_branch)
        elif isinstance(node, Loop):
            optimized_start = self.optimize(node.start)
            optimized_end = self.optimize(node.end)
            optimized_body = Program([self.optimize(stmt) for stmt in node.body.statements])
            return Loop(node.identifier, optimized_start, optimized_end, optimized_body)
        elif isinstance(node, PrintStatement):
            optimized_expression = self.optimize(node.expression)
            return PrintStatement(optimized_expression)
        elif isinstance(node, ReturnStatement):
            optimized_expression = self.optimize(node.expression)
            return ReturnStatement(optimized_expression)
        elif isinstance(node, CallStatement):
            optimized_args = [self.optimize(arg) for arg in node.args]
            return CallStatement(node.procedure_name, optimized_args)
        elif isinstance(node, ProcedureDefinition):
            optimized_body = [self.optimize(stmt) for stmt in node.body]
            return ProcedureDefinition(node.name, node.params, optimized_body)
        elif isinstance(node, ProcedureCall):
            optimized_args = [self.optimize(arg) for arg in node.args]
            return ProcedureCall(node.name, optimized_args)
        elif isinstance(node, BinaryOperation):
            optimized_left = self.optimize(node.left)
            optimized_right = self.optimize(node.right)
            if isinstance(optimized_left, Literal) and isinstance(optimized_right, Literal):
                # Perform constant folding
                if node.operator == '+':
                    return Literal(optimized_left.value + optimized_right.value)
                elif node.operator == '-':
                    return Literal(optimized_left.value - optimized_right.value)
                elif node.operator == '*':
                    return Literal(optimized_left.value * optimized_right.value)
                elif node.operator == '/':
                    return Literal(optimized_left.value / optimized_right.value)
            return BinaryOperation(optimized_left, node.operator, optimized_right)
        elif isinstance(node, Variable):
            return node
        elif isinstance(node, Literal):
            return node
        return node
