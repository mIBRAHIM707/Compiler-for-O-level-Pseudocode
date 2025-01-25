import tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from optimizer import Optimizer  # Updated import statement

pseudocode = """
# Simple assignment
x <- 10

# Assignment with binary operations
y <- 10 + 20 - 5

# Conditional without ELSE
IF x > 0 THEN
  z <- 1
ENDIF

# Conditional with ELSE
IF x = 0 THEN
  z <- 1
ELSE
  z <- 0
ENDIF

# Loop from 1 to 5
FOR i <- 1 TO 5 DO
  x <- x + i
ENDFOR

# Print statement
PRINT x

# Procedure definition and call
PROCEDURE add(a, b)
  RETURN a + b
ENDPROCEDURE

x <- add(3, 4)

# Nested conditional
IF x > 0 THEN
  IF y > 0 THEN
    z <- 1
  ELSE
    z <- 2
  ENDIF
ELSE
  z <- 3
ENDIF

# Complex expression
x <- (3 + 2) * (7 - 4)

# Read statement
READ x

# Return statement
PROCEDURE square(n)
  RETURN n * n
ENDPROCEDURE

x <- square(5)

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
