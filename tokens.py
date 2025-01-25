import re

TOKEN_PATTERNS = [
    ("KEYWORD", r"\b(IF|THEN|ELSE|ENDIF|FOR|TO|DO|ENDFOR|WHILE|ENDWHILE|PRINT|READ|PROCEDURE|ENDPROCEDURE|CALL|RETURN)\b"),
    ("ASSIGN_OP", r"<-"),
    ("REL_OP", r"(=|<>|<|>|<=|>=)"),
    ("OPERATOR", r"(\+|\-|\*|/|MOD)"),  # Added 'MOD' for modulus operation
    ("DELIMITER", r"(\(|\)|,|:)"),  # Added ':' for optional cases like label or type definition
    ("NUMBER", r"\b\d+(\.\d+)?\b"),  # Matches integers and decimals
    ("STRING", r"\".*?\""),  # Matches anything in double quotes
    ("IDENTIFIER", r"\b[A-Za-z_][A-Za-z0-9_]*\b"),  # Matches variable/procedure names
    ("WHITESPACE", r"\s+"),  # Matches spaces and tabs
    ("COMMENT", r"#.*"),  # Matches comments starting with #
]
