from re import sub

KEY_WORDS = {
    "let": "LET",
    "upd": "UPD",
    "del": "DEL",
    "for": "FOR",
    "while": "WHILE",
    "if": "IF",
    "else": "ELSE",
    "func": "FUNC",
    "print": "PRINT",
    "println": "PRINTLN"
}

SPECIAL_CHARS = {
    "=": "EQUAL",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
    ",": "COMMA",
    "==": "EQEQ",
    "!=": "NOTEQ",
    ">": "GT",
    "<": "LT"
}

def lexer(code):
    result = []
    pos = 0
    wordBuff = ""
    isStr = False
    codelen = len(code)

    while pos < codelen:
        ch = code[pos]
        nextch = code[pos+1] if pos+1 < codelen else " "
    
        if ch.isspace() and isStr == False:
            pos += 1
            continue

        elif ch.isalpha() and isStr == False:
            # print("Letter")
            # print(wordBuff)
            # print(nextch)
            wordBuff += ch
            if nextch.isspace() or nextch in SPECIAL_CHARS:
                # print("Space")
                if wordBuff in KEY_WORDS:
                    result.append((KEY_WORDS[wordBuff], wordBuff))
                else:
                    result.append(("IDENT", wordBuff))
                wordBuff = ""

        elif ch.isdigit() and isStr == False:
            wordBuff += ch
            if nextch.isspace() or nextch in SPECIAL_CHARS:
                # print("Space")
                if wordBuff.isdigit():
                    result.append(("NUMBER", wordBuff))
                else:
                    result.append(("IDENT", wordBuff))
                wordBuff = ""
        
        elif ch == '"':
            if isStr == False: 
                isStr = True
            else: 
                isStr = False
                result.append(("STRING", wordBuff))
                wordBuff = ""

        elif isStr == True: 
            wordBuff += ch
        
        elif ch in SPECIAL_CHARS and isStr == False:
            if ch == "=" and nextch == "=":
                result.append((SPECIAL_CHARS["=="], "=="))
                pos += 2
                continue
            elif ch == "!" and nextch == "=": 
                result.append((SPECIAL_CHARS["!="], "!="))
                pos += 2
                continue
            elif ch == "/" and nextch == "/":
                while code[pos] != "\n": pos += 1
            else:
                result.append((SPECIAL_CHARS[ch], ch))
                wordBuff = ""

        else:
            raise Exception(f"Unknown character: {ch}")
    
        pos += 1
    return result

# print(lexer("""
# while(x < 10){
#     print(x);
#     let x = x + 1;
# }
# """))
