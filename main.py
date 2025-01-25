import tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator

pseudocode = """
x <- 5
IF x > 0 THEN
  PRINT "Positive"
ENDIF
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
