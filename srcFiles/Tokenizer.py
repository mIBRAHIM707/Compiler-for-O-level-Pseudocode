import re

TOKEN_PATTERNS = [
    ("KEYWORD", r"\b(IF|THEN|ELSE|ENDIF|FOR|TO|DO|ENDFOR|WHILE|ENDWHILE|PRINT|READ|PROCEDURE|ENDPROCEDURE|CALL|RETURN)\b"),
    ("ASSIGN_OP", r"<-"),
    ("REL_OP", r"(=|<>|<|>|<=|>=)"),
    ("OPERATOR", r"(\+|\-|\*|/|MOD)"),
    ("DELIMITER", r"(\(|\)|,|:)"),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),
    ("STRING", r"\".*?\""),
    ("IDENTIFIER", r"\b[A-Za-z_][A-Za-z0-9_]*\b"),
    ("WHITESPACE", r"\s+"),
    ("COMMENT", r"#.*"),
]

def tokenize(pseudocode):
    tokens = []
    lineNumber = 1
    for line in pseudocode.splitlines():
        position = 0
        while position < len(line):
            match = None
            for token_type, pattern in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(line, position)
                if match:
                    if token_type != "WHITESPACE":
                        tokens.append((token_type, match.group(0)))
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unknown token at line {lineNumber}, position {position}: {line[position]}")
    return tokens