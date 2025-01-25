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
