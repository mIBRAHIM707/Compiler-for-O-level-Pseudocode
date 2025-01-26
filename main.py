import tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from Optimizer import Optimizer
import os

def read_pseudocode(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    pseudocode_file = input("Enter the path to the pseudocode (.psc) file: ")
    pseudocode = read_pseudocode(pseudocode_file)

    try:
        tokens = tokenizer.tokenize(pseudocode)
        parser = par.Parser(tokens)
        ast = parser.parse_program()

        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        optimizer = Optimizer()
        optimized_ast = optimizer.optimize(ast)

        generator = CodeGenerator()
        generator.generate(optimized_ast)
        target_code = generator.get_code()

        with open("generatedCode.py", "w") as code_file:
            code_file.write(target_code)

        os.system("python3 generatedCode.py")

    except SyntaxError:
        print("Syntax error in the pseudocode.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
