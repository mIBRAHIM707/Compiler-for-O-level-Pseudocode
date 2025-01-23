import tokenizer
import parser as par

pseudocode = """
x <- 3 + 4

"""

tokens = tokenizer.tokenize(pseudocode)
# try:
#     for token in tokens:
#         print(token)
# except SyntaxError as e:
#     print(f"Error: {e}")

parser = par.Parser(tokens)
ast = parser.parse_program()

# Print the AST (you can improve this for better readability)

print("\nParsed Program:")
for statement in ast.statements:
    print(statement)
