import tokens as t
import re

def tokenize(pseudocode):
    tokens = []
    lineNumber = 1
    for line in pseudocode.splitlines():
        position = 0
        while position < len(line):
            match = None
            for token_type, pattern in t.TOKEN_PATTERNS:
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