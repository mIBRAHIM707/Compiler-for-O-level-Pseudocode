import re

TOKEN_PATTERNS = [
    ("KEYWORD", r"\b(IF|THEN|ELSE|ENDIF|FOR|TO|DO|ENDFOR|WHILE|ENDWHILE|PRINT|READ|PROCEDURE|CALL|RETURN)\b"),
    ("ASSIGN_OP", r"<-"),
    ("REL_OP", r"(=|<>|<|>|<=|>=)"),
    ("OPERATOR", r"(\+|\-|\*|/)"),
    ("DELIMITER", r"(\(|\)|,)"),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),  # Matches integers and decimals
    ("STRING", r"\".*?\""),  # Matches anything in double quotes
    ("IDENTIFIER", r"\b[A-Za-z_][A-Za-z0-9_]*\b"),  # Variable/function names
    ("WHITESPACE", r"\s+"),  # Matches spaces and tabs
    #("UNKNOWN", r".")  # Matches any unknown character
]
