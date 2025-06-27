import interpreter
import argparse

p = argparse.ArgumentParser()
p.add_argument('--run')
p.add_argument('--benchmark', action='store_true')

args = p.parse_args()

with open(args.run, 'r', encoding='utf-8') as file:
    code = file.read()

if args.benchmark:
    interpreter.benchmark(code)
else:
    interpreter.run_program(code)
