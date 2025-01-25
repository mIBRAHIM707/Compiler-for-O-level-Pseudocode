import tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from optimizer import Optimizer  # Updated import statement

pseudocode = """
x <- (3 + 2) * (7 - 4)
"""

tokens = tokenizer.tokenize(pseudocode)
parser = par.Parser(tokens)
ast = parser.parse_program()

# Perform semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# Optimize the AST
optimizer = Optimizer()
optimized_ast = optimizer.optimize(ast)

# Generate target code
generator = CodeGenerator()
generator.generate(optimized_ast)
target_code = generator.get_code()

print("\nGenerated Code:")
print(target_code)
