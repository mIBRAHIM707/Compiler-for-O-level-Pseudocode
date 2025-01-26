import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'srcFiles'))

import argparse
import Tokenizer as tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from Optimizer import Optimizer

def read_pseudocode(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="O-Level Pseudocode Compiler")
    parser.add_argument("pseudocode_file", help="Path to the pseudocode (.psc) file")
    args = parser.parse_args()

    pseudocode = read_pseudocode(args.pseudocode_file)

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
