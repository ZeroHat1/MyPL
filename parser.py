OPERATORS = (
    "+",
    "-",
    "*",
    "/",
    ">",
    "<",
    ">=",
    "<=",
    "==",
    "!="
)

def parse_expression(tokens):
    current = None
    pos = 0
    token = tokens[pos]

    if token[0] == "NUMBER":
        current = {"type": "number", "value": int(token[1])}
    elif token[0] == "IDENT":
        current = {"type": "identifier", "value": token[1]}
    else:
        raise Exception("Expected number or identifier")

    pos += 1
    while pos < len(tokens):
        token = tokens[pos]

        if token[1] in OPERATORS:
            operator = token[1]
            next_token = tokens[pos + 1]

            if next_token[0] == "NUMBER":
                right = {"type": "number", "value": int(next_token[1])}
            elif next_token[0] == "IDENT":
                right = {"type": "identifier", "value": next_token[1]}
            else:
                raise Exception("Expected number or identifier after operator")
        
            current = {
                "type": "binary",
                "operator": operator,
                "left": current,
                "right": right
            }

        pos += 2
    
    return current

def parse_let(tokens, pos):
    if tokens[pos][0] != "LET":
        raise Exception("Expected LET")
    pos += 1

    if tokens[pos][0] != "IDENT":
        raise Exception("Expected identifier after let")
    name = tokens[pos][1]
    pos += 1

    if tokens[pos][0] != "EQUAL":
        raise Exception("Expected '=' after identifier")
    pos += 1

    expr_tokens = []
    while tokens[pos][0] != "SEMICOLON":
        expr_tokens.append(tokens[pos])
        pos += 1

    pos += 1

    value = parse_expression(expr_tokens)

    return {
        "type": "let",
        "name": name,
        "value": value
    }, pos

def parse_del(tokens, pos):
    if tokens[pos][0] != "DEL":
        raise Exception("Expected DEL")
    pos += 1

    if tokens[pos][0] != "IDENT":
        raise Exception("Expected identifier after del")
    name = tokens[pos][1]
    pos += 1

    if tokens[pos][0] != "SEMICOLON":
        raise Exception("Expected semicolon after identifier")
    pos += 1

    return {
        "type": "del",
        "name": name,
    }, pos

def parse_print(tokens, pos, isNewLine=False):
    if tokens[pos][0] != "PRINT" and tokens[pos][0] != "PRINTLN":
        raise Exception("Expected PRINT")
    pos += 1

    if tokens[pos][0] != "LPAREN":
        raise Exception("Expected left paren after let")
    pos += 1

    if tokens[pos][0] == "STRING":
        value = {"type": "string", "value": tokens[pos][1]}
        pos += 1
    else:
        expr_tokens = []
        while tokens[pos][0] != "RPAREN":
            expr_tokens.append(tokens[pos])
            pos += 1
        value = parse_expression(expr_tokens)

    pos += 1

    if tokens[pos][0] != "SEMICOLON":
        raise Exception("Expected semicolon after let")
    pos += 1
    if not isNewLine:
        return {
            "type": "print",
            "value": value
        }, pos
    else:
        return {
            "type": "println",
            "value": value
        }, pos
    
def parse_while(tokens, pos):
    if tokens[pos][0] != "WHILE":
        raise Exception("Expected WHILE")
    pos += 1

    if tokens[pos][0] != "LPAREN":
        raise Exception("Expected LPAREN")
    pos += 1

    expr_tokens = []
    while tokens[pos][0] != "RPAREN":
        expr_tokens.append(tokens[pos])
        pos += 1
    condition = parse_expression(expr_tokens)
    pos += 1

    if tokens[pos][0] != "LBRACE":
        raise Exception("Expected LBRACE")
    pos += 1

    depth = 1
    expr_tokens.clear()
    while depth > 0:
        expr_tokens.append(tokens[pos])
        pos += 1

        if tokens[pos][0] == "LBRACE":
            depth += 1
        elif tokens[pos][0] == "RBRACE":
            depth -= 1

    body = parse_program(expr_tokens)
    pos += 1

    if tokens[pos][0] != "ELSE":
        pos += 1
        

    else:
        return {
                "type": "if",
                "condition": condition,
                "body": body
            }, pos
        

def parse_if(tokens, pos):
    if tokens[pos][0] != "IF":
        raise Exception("Expected WHILE")
    pos += 1

    if tokens[pos][0] != "LPAREN":
        raise Exception("Expected LPAREN")
    pos += 1

    expr_tokens = []
    while tokens[pos][0] != "RPAREN":
        expr_tokens.append(tokens[pos])
        pos += 1
    condition = parse_expression(expr_tokens)
    pos += 1

    if tokens[pos][0] != "LBRACE":
        raise Exception("Expected LBRACE")
    pos += 1

    depth = 1
    expr_tokens.clear()
    while depth > 0:
        expr_tokens.append(tokens[pos])
        pos += 1

        if tokens[pos][0] == "LBRACE":
            depth += 1
        elif tokens[pos][0] == "RBRACE":
            depth -= 1

    body = parse_program(expr_tokens)
    pos += 1
    
    return {
            "type": "while",
            "condition": condition,
            "body": body
        }, pos

def parse_program(tokens):
    pos = 0
    statements = []

    while pos < len(tokens):
        # print(tokens)
        token = tokens[pos]

        if token[0] == "LET":
            stmt, pos = parse_let(tokens, pos)
            statements.append(stmt)
        elif token[0] == "UPD":
            stmt, pos = parse_let(tokens, pos)
            statements.append(stmt)
        elif token[0] == "DEL":
            stmt, pos = parse_del(tokens, pos)
            statements.append(stmt)
        elif token[0] == "PRINT":
            stmt, pos = parse_print(tokens, pos, isNewLine=False)
            statements.append(stmt)
        elif token[0] == "PRINTLN":
            stmt, pos = parse_print(tokens, pos, isNewLine=True)
            statements.append(stmt)
        elif token[0] == "WHILE":
            stmt, pos = parse_while(tokens, pos)
            statements.append(stmt)
        else:
            raise Exception(f"Unknown statement type: {token[0]}")

    return statements
    
# print(parse_program([('WHILE', 'while'), ('LPAREN', '('), ('IDENT', 'x'), ('LT', '<'), ('NUMBER', '10'), ('RPAREN', ')'), ('LBRACE', '{'), ('PRINT', 'print'), ('LPAREN', '('), ('IDENT', 'x'), ('RPAREN', ')'), ('SEMICOLON', ';'), ('LET', 'let'), ('IDENT', 'x'), ('EQUAL', '='), ('IDENT', 'x'), ('PLUS', '+'), ('NUMBER', '1'), ('SEMICOLON', ';'), ('RBRACE', '}')]))
