from sys import argv
import subprocess

iota_counter = 0
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota()
COUNT_VAR = 4

def push(x):
    return (OP_PUSH, x)

def plus():
    return (OP_PLUS, )

def minus():
    return (OP_MINUS, )

def dump():
    return (OP_DUMP, )

def simulate_program(program):
    assert COUNT_OPS == COUNT_VAR, 'Exhausted handling of operations in simulation'
    stack = []
    for op in program:
        if op[0] == OP_PUSH:
            stack.append(op[1])
        elif op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)  # LIFO
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif op[0] == OP_DUMP:
            a = stack.pop()
            print(a)
        else:
            assert False, 'Unreachable operation'

def compile_program(program, out_file_path):
    assert COUNT_OPS == COUNT_VAR, 'Exhaustive handling of operations in compilation'
    assert False, 'Not Implemented'

def parse_word_as_op(word):
    assert COUNT_OPS == COUNT_VAR, 'Exhaustive op handling in parse_word_as_op'
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    else:
        return push(int(word))

def load_program_from_file(in_file_path):
    with open(in_file_path, 'r') as f:
        return [parse_word_as_op(word) for word in f.read().split()]

def usage(porth_file):
    print(f'Usage: {porth_file} <SUBCOMMAND> [ARGS]')
    print('SUBCOMMANDS:')
    print('    sim <file>        Simulate the program')
    print('    com <file>        Compile the program')

def uncons(xs):
    return (xs[0], xs[1:])

def call_cmd(cmd):
    print(cmd)
    subprocess.call(cmd)

if __name__ == '__main__':
    assert len(argv) >= 1
    (program_name, argv) = uncons(argv)
    if len(argv) < 1:
        usage(program_name)
        print('ERROR: no subcommand is provided')
        exit(1)
    (subcommand, argv) = uncons(argv)
    if subcommand == 'sim':
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: no input file is provided for simulation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        simulate_program(program)
    elif subcommand == 'com':
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: no input file is provided for compilation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-felf64", "output.asm"])
        call_cmd(["ld", "-o", "output", "output.o"])
