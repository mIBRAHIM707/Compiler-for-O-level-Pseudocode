import tokenizer
import parser as par

pseudocode = """
x <- 5
IF x > 0 THEN
    PRINT "Positive"
ENDIF
"""

try:
    tokens = tokenizer.tokenize(pseudocode)
    for token in tokens:
        print(token)
except SyntaxError as e:
    print(f"Error: {e}")

parser = par.Parser(tokens)
ast = parser.parse_program()

# Print the AST (you can improve this for better readability)
print(ast)
