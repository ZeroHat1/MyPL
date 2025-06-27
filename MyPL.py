import interpreter
import argparse
import time

def benchmark(code, iterations=1000):
    for _ in range(10):
        interpreter.run_program(code)

    start = time.perf_counter()
    for _ in range(iterations):
        interpreter.run_program(code)
    end = time.perf_counter()

    total = end - start
    avg = total / iterations
    print(f"Total: {total:.6f} sec")
    print(f"Average per run: {avg * 1_000_000:.2f} µs")

p = argparse.ArgumentParser()
p.add_argument('--run')
p.add_argument('--benchmark', action='store_true')

args = p.parse_args()

with open(args.run, 'r', encoding='utf-8') as file:
    code = file.read()

if args.benchmark:
    benchmark(code)
else:
    interpreter.run_program(code)
