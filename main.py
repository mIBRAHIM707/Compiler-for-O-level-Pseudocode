import tokenizer
import parser as par

pseudocode = """
PROCEDURE CalculateSum()
    x <- 0
    FOR i <- 1 TO 10 DO
        IF i > 2 THEN
            x <- x + i
            PRINT "Adding even number: "
            PRINT i
        ELSE
            PRINT "Skipping odd number: "
            PRINT i
        ENDIF
    ENDFOR
    RETURN x
ENDPROCEDURE

y <- CalculateSum()
PRINT "Total sum is: "
PRINT y

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
print("Parsed Program:")
for statement in ast.statements:
    print(statement)
