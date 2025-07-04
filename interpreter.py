PRECEDENCE = {
    "==": 0,
    "!=": 0,
    "<": 0,
    ">": 0,
    "<=": 0,
    ">=": 0,
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2
}

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

def eval_expr(node, env):
    if node["type"] == "number":
        return node["value"]
    elif node["type"] == "identifier":
        return env[node["value"]]
    elif node["type"] == "string":
        return node["value"]
    elif node["type"] == "bool":
        return node["value"]
    elif node["type"] == "binary":
        values = traverse_dict(node, filter=("value"))
        operators = traverse_dict(node, filter=("operator"))[::-1]
        infix = []
        
        for i in range(0, len(values)-1):
            infix.append(values[i])
            infix.append(operators[i])
        infix.append(values[-1])

        stack = []
        output = []

        for i in infix:
            if i in PRECEDENCE:
                if len(stack) == 0:
                    stack.append(i)
                else:
                    if PRECEDENCE[stack[-1]] >= PRECEDENCE[i]:
                        for j in range(len(stack)-1, -1, -1):
                            if PRECEDENCE[stack[j]] >= PRECEDENCE[i]:
                                output.append(stack[j])
                                stack.pop(j)
                        stack.append(i)
                    else:
                        stack.append(i)
            else:
                if i in env:
                    output.append(env[i])
                else:
                    output.append(i)

        output += stack[::-1]
        stack.clear()

        for val in output:
            if val in PRECEDENCE:
                if val == "+": 
                    stack[-1] = stack[-2] + stack[-1]
                    stack.pop(-2)
                elif val == "-":
                    stack[-1] = stack[-2] - stack[-1]
                    stack.pop(-2)
                elif val == "*":
                    stack[-1] = stack[-2] * stack[-1]
                    stack.pop(-2)
                elif val == "/":
                    stack[-1] = stack[-2] / stack[-1]
                    stack.pop(-2)
                elif val == ">":
                    stack[-1] = stack[-2] > stack[-1]
                    stack.pop(-2)
                elif val == "<":
                    stack[-1] = stack[-2] < stack[-1]
                    stack.pop(-2)
                elif val == ">=":
                    stack[-1] = stack[-2] >= stack[-1]
                    stack.pop(-2)
                elif val == "<=":
                    stack[-1] = stack[-2] <= stack[-1]
                    stack.pop(-2)
                elif val == "==":
                    stack[-1] = stack[-2] == stack[-1]
                    stack.pop(-2)
                elif val == "!=":
                    stack[-1] = stack[-2] != stack[-1]
                    stack.pop(-2)
            else:
                stack.append(val)
        
        return stack[-1]

import mypl_parser
import lexer

def resolve_variable(env, outer_env, node):
    # print("\n\n")
    # print("Node:", node)
    # print(type(node))
    values = []
    if isinstance(node, list):
        for n in node:
            # print(n)
            values += traverse_dict(n, filter=("value"))
    else:
        values = traverse_dict(node, filter=("value"))
    resolve_env = {}

    # print(values)
    for val in values:
        if val in env.keys():
            resolve_env[val] = env[val]
        elif val in outer_env.keys():
            resolve_env[val] = outer_env[val]
    
    # print(env)
    # print(outer_env)
    # print(resolve_env)
    # print("\n\n")
    return resolve_env

def run_function(statements, outer_env={}, env={}):
    for stmt in statements:
        if stmt["type"] == "let":
            value = eval_expr(stmt["value"], resolve_variable(env, outer_env, stmt["value"]))
            env[stmt["name"]] = value
        elif stmt["type"] == "del":
            del env[stmt["name"]]
        elif stmt["type"] == "print":
            value = eval_expr(stmt["value"], resolve_variable(env, outer_env, stmt["value"]))
            print(value, end="")
        elif stmt["type"] == "println":
            value = eval_expr(stmt["value"], resolve_variable(env, outer_env, stmt["value"]))
            print(value, end="\n")
        elif stmt["type"] == "while":
            while eval_expr(stmt["condition"], resolve_variable(env, outer_env, stmt["condition"])):
                run_program(stmt["body"], resolve_variable(env, outer_env, stmt["body"]))
        elif stmt["type"] == "if":
            if eval_expr(stmt["condition"], resolve_variable(env, outer_env, stmt["condition"])):
                run_program(stmt["body"], resolve_variable(env, outer_env, stmt["body"]))
            else:
                run_program(stmt["else_body"], resolve_variable(env, outer_env, stmt["else_body"]))
        # elif stmt["type"] == "function-def":
        #     env[stmt["name"]] = {"type": "function", "params": stmt["params"], "body": stmt["body"]}
        elif stmt["type"] == "call":
            params = env[stmt["name"]]["params"]
            func_env = {}
            for i, val in enumerate(params):
                func_env[val] = eval_expr(stmt["args"][i], resolve_variable(env, outer_env, stmt["args"][i]))

            run_function(env[stmt["name"]]["body"], outer_env=env, env=func_env)

def run_program(statements, env={}):
    for stmt in statements:
        if stmt["type"] == "let":
            value = eval_expr(stmt["value"], env)
            env[stmt["name"]] = value
        elif stmt["type"] == "del":
            del env[stmt["name"]]
        elif stmt["type"] == "print":
            value = eval_expr(stmt["value"], env)
            print(value, end="")
        elif stmt["type"] == "println":
            value = eval_expr(stmt["value"], env)
            print(value, end="\n")
        elif stmt["type"] == "while":
            while eval_expr(stmt["condition"], env):
                run_program(stmt["body"], env)
        elif stmt["type"] == "if":
            if eval_expr(stmt["condition"], env):
                run_program(stmt["body"], env)
            else:
                run_program(stmt["else_body"], env)
        elif stmt["type"] == "function-def":
            env[stmt["name"]] = {"type": "function", "params": stmt["params"], "body": stmt["body"]}
        elif stmt["type"] == "call":
            params = env[stmt["name"]]["params"]
            func_env = {}
            for i, val in enumerate(params):
                func_env[val] = eval_expr(stmt["args"][i], env)

            run_function(env[stmt["name"]]["body"], outer_env=env, env=func_env)

    # print(env)



def init_program(program):
    tokens = lexer.lexer(program)
    statements = mypl_parser.parse_program(tokens)

    run_program(statements)


# eval_expr({'type': 'binary', 'operator': '-', 'left': {'type': 'binary', 'operator': '+', 'left': {'type': 'binary', 'operator': '+', 'left': {'type': 'number', 'value': 10}, 'right': {'type': 'number', 'value': 5}}, 'right': {'type': 'number', 'value': 'x'}}, 'right': {'type': 'number', 'value': 1}}, {'x': 3})

# code = """
# let x = 2 + 2 * 2;
# print(x);
# """

# run_program(code)
