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
