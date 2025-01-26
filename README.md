# O-Level Pseudocode Compiler

This project is an O-level pseudocode compiler that translates pseudocode into executable Python code. The compiler consists of several components: tokenizer, parser, semantic analyzer, optimizer, and code generator.

## Components

### Tokenizer

The tokenizer converts pseudocode into a list of tokens. It uses regular expressions to identify different types of tokens such as keywords, operators, delimiters, numbers, strings, identifiers, whitespace, and comments.

### Parser

The parser converts the list of tokens into an abstract syntax tree (AST). It supports various pseudocode constructs such as assignments, conditionals, loops, print statements, procedure definitions, and procedure calls.

### Semantic Analyzer

The semantic analyzer checks the AST for semantic errors. It ensures that variables are declared before use, types are consistent, and other semantic rules are followed.

### Optimizer

The optimizer performs various optimizations on the AST. It includes constant folding, dead code elimination, and other optimizations to improve the efficiency of the generated code.

### Code Generator

The code generator converts the optimized AST into executable Python code. It handles the translation of pseudocode constructs into their Python equivalents.

## Usage

To use the compiler, follow these steps:

1. **Write Pseudocode**: Write your pseudocode in a `.psc` file.

2. **Run the Compiler**: Execute the `main.py` file with the path to the `.psc` file as a command-line argument to tokenize, parse, analyze, optimize, and generate Python code from the pseudocode.

3. **View and Execute Generated Code**: The generated Python code will be written to a file named `generatedCode.py` and executed automatically.

## Example

Here is an example pseudocode:

```plaintext
x <- (3 + 2) * (7 - 4)
READ x
PROCEDURE square(n)
  RETURN n * n
ENDPROCEDURE
x <- square(5)
```

The generated Python code will be:

```python
x = 15
x = input()
def square(n):
    return (n * n)
x = square(5)
```

## Running the Compiler

To run the compiler, use the following command:

```sh
python3 srcFiles/main.py example.psc
```

Replace `example.psc` with the path to your `.psc` file.

## Files

- `Tokenizer.py`: Defines the token patterns for the tokenizer and Implements the tokenizer to convert pseudocode into tokens.
- `Parser.py`: Implements the parser to convert tokens into an AST.
- `SemanticAnalyzer.py`: Implements the semantic analyzer to check for semantic errors.
- `Optimizer.py`: Implements the optimizer to perform various optimizations on the AST.
- `CodeGenerator.py`: Implements the code generator to convert the AST into Python code.
- `main.py`: Main file to run the compiler.

## Future Work

- **Testing**: Write comprehensive test cases to ensure the compiler works correctly.
- **Error Handling**: Improve error handling to provide more informative error messages.
- **Documentation**: Expand the documentation with more examples and detailed explanations.
- **Optimization**: Enhance the optimizer to handle more complex optimizations.
- **User Interface**: Create a user-friendly interface for the compiler.
- **Deployment**: Package the compiler for distribution.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.