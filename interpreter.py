precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}
import pprint

def traverse_dict(d, path=None, filter=()):
    if path is None:
        path = []

    results = []

    for key, value in d.items():
        current_path = path + [key]
        if isinstance(value, dict):
            results.extend(traverse_dict(value, current_path, filter))
        else:
            if any(k in filter for k in current_path):
                results.append(value)

    return results

def recursive_eval_expr(tokens, env):
    # print("tokens:", tokens)
    lower = None

    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i] in precedence and precedence[tokens[i]] <= 1:
            lower = i
            break
    if lower == None:
        for i in range(len(tokens) - 1, -1, -1):
            if tokens[i] in precedence and precedence[tokens[i]] <= 2:
                lower = i
                break

    if lower is not None and len(tokens) >= 1:
        current = {
            "type": "binary",
            "operator": tokens[lower],
            "left": recursive_eval_expr(tokens[:lower], env),
            "right": recursive_eval_expr(tokens[lower + 1:], env)
        }
        return current
    elif len(tokens) == 1:
        if type(tokens[0]) == int:
            current = {
                "type": "number",
                "value": tokens[0]
            }
        else:
            current = {
                "type": "identifier",
                "value": env[tokens[0]]
            }
        return current
    else:
        raise ValueError("Invalid expression: empty or invalid token list.", tokens)

def eval_expr(node, env):
    if node["type"] == "number":
        return node["value"]
    elif node["type"] == "identifier":
        return env[node["value"]]
    elif node["type"] == "string":
        return node["value"]
    elif node["type"] == "binary":
        operators = traverse_dict(node, filter=("operator"))
        operators = operators[::-1]
        values = traverse_dict(node, filter=("value"))
        tokens = []

        for i in range(0, len(values)-1):
            tokens.append(values[i])
            tokens.append(operators[i])
        tokens.append(values[-1])
    
        node = recursive_eval_expr(tokens, env)

        valBuff = 0

        left = eval_expr(node["left"], env)
        right = eval_expr(node["right"], env)
        op = node["operator"]

        if op == "+": valBuff = left + right
        elif op == "-": valBuff = left - right
        elif op == "*": valBuff = left * right
        elif op == "/": valBuff = left / right

        return valBuff

import parser
import lexer

def run_program(program):
    env = {}

    tokens = lexer.lexer(program)
    # print(tokens)
    statements = parser.parse_program(tokens)
    # pprint.pprint(statements)

    for stmt in statements:
        if stmt["type"] == "let":
            value = eval_expr(stmt["value"], env)
            env[stmt["name"]] = value
            
        elif stmt["type"] == "print":
            value = eval_expr(stmt["value"], env)
            print(value)
    # print(env)

# eval_expr({'type': 'binary', 'operator': '-', 'left': {'type': 'binary', 'operator': '+', 'left': {'type': 'binary', 'operator': '+', 'left': {'type': 'number', 'value': 10}, 'right': {'type': 'number', 'value': 5}}, 'right': {'type': 'number', 'value': 'x'}}, 'right': {'type': 'number', 'value': 1}}, {'x': 3})


import time

def benchmark(code, iterations=1000):
    # Сначала "прогреем" (опционально, если в будущем будет JIT или кэш)
    for _ in range(10):
        run_program(code)

    start = time.perf_counter()
    for _ in range(iterations):
        run_program(code)
    end = time.perf_counter()

    total = end - start
    avg = total / iterations
    print(f"Total: {total:.6f} sec")
    print(f"Average per run: {avg * 1_000_000:.2f} µs")



# code = """
# let x = 2 + 2 * 2;
# print(x);
# """



# run_program(code)
# benchmark(code)


