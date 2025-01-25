import tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator

pseudocode = """
x <- (3 + 2
"""

tokens = tokenizer.tokenize(pseudocode)
parser = par.Parser(tokens)
ast = parser.parse_program()

# Perform semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# Generate target code
generator = CodeGenerator()
generator.generate(ast)
target_code = generator.get_code()

print("\nGenerated Code:")
print(target_code)
