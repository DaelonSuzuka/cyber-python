import re


class Writer:
    def __init__(self, out=None):
        self.items = []
        self.out = self.items.append
        if out:
            self.out = out
        self.indent = 4
        self.level = 0

    def __iadd__(self, other):
        self.line(other)
        return self

    def raw(self, string):
        self.out(string)

    def join(self, base: str):
        return base.join(self.items)

    def line(self, string=''):
        if string:
            self.out(' ' * self.indent * self.level + string + '\n')
        else:
            self.out('\n')

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, *_):
        self.level -= 1


with open('src/cyber/src/cyber.h') as f:
    raw = f.read()

output = ''

thing = r'^.*[,;{]$'

matches = re.findall(thing, raw, flags=re.M)

definitions = []
chunk = []
in_chunk = False

for m in matches:
    if m.endswith('{'):
        in_chunk = True
    if in_chunk:
        chunk.append(m)

        if m.startswith('}'):
            in_chunk = False
            definitions.append('\n'.join(chunk))
            chunk = []

        continue
    definitions.append(m)

w = Writer()

w += '# GENERATED FILE DO NOT EDIT #'
w += ''
w += 'from ctypes import *'
w += 'from pathlib import Path'
w += 'import sys'
w += 'from enum import Enum'
w += 'import platform'
w += ''

# TODO: add linux-arm64 support
w += """
base_path = Path(__file__).parent / 'lib'

if sys.platform == 'win32':
    path = base_path / 'cyber.dll'
    lib = WinDLL(path.as_posix())
elif sys.platform == 'linux':
    path = base_path / 'libcyber.so'
    lib = CDLL(path.as_posix())
elif sys.platform == 'darwin':
    if platform.machine() == 'arm64':
        path = base_path / 'libcyber-arm64.dylib'
        lib = CDLL(path.as_posix())
    else:
        path = base_path / 'libcyber.dylib'
        lib = CDLL(path.as_posix())
"""
w += ''
w += '# GENERATED FILE DO NOT EDIT #'
w += ''

types = {
    'bool': 'c_bool',
    'double': 'c_double',
    'void*': 'c_void_p',
    'char*': 'c_char_p',
    'const char*': 'c_char_p',
    'size_t': 'c_size_t',
    'uint8_t': 'c_uint8',
    'uint64_t': 'c_uint64',
    'uint32_t': 'c_uint32',
    'int': 'c_int',
    'CyResultCode': 'c_int',
}


def typedef_int(w, d):
    m = re.match(r'typedef (\w+) (\w*)', d)
    t = m[1]
    types[f'{m[2]}*'] = f'POINTER({m[2]})'
    w += f'class {m[2]}({types.get(t, t)}):'
    with w:
        w += '...'


def typedef_struct(w, d):
    m = re.match(r'typedef struct (\w+) ({.*})?', d.replace('\n', ''))
    struct_name = m[1]
    types[f'{struct_name}*'] = f'POINTER({struct_name})'
    fields = []
    if m[2]:
        for f in m[2][1:-1].split(';'):
            if f:
                parts = f.strip().split(' ')
                name = parts[-1]
                c_type = ' '.join(parts[:-1])
                py_type = types.get(c_type, c_type)
                fields.append(f"('{name}', {py_type})")

    w += f'class {struct_name}(Structure):'
    with w:
        if fields:
            w += f"_fields_ = [{', '.join(fields)}]"
        else:
            w += '...'


def typedef_enum(w, d):
    m = re.match(r'typedef enum ({.*})? (\w+);', d.replace('\n', ''))
    values = m[1]
    enum_name = m[2]
    items = [v.strip().replace(' = 0', '') for v in values[1:-1].split(',') if v]

    w += f'class {enum_name}(Enum):'
    with w:
        for i, item in enumerate(items):
            w += f'{item} = {i}'


def typedef_funcptr_def(w, d):
    m = re.match(r'typedef (\w+) \(\*(\w+)\)(.*);', d)
    type_name = m[2]
    args = m[3][1:-1].split(', ')
    arg_types = [a.split(' ')[0] for a in args]
    argtypes = [types.get(m[1], m[1])]
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))

    w += f'# {d}'
    w += f'{type_name} = CFUNCTYPE({", ".join(argtypes)})'


def func_def(w, d):
    m = re.match(r'(\w+\*?) (\w+)(.*);', d)
    func_name = m[2]
    ret = m[1]
    args = m[3][1:-1].split(', ')
    arg_types = [a.split(' ')[0] for a in args]
    argtypes = []
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))

    w += f'# {d}'
    w += f'{func_name} = lib.{func_name}'
    if ret != 'void':
        w += f'{func_name}.restype = {types.get(ret, ret)}'
    w += f'{func_name}.argtypes = [{", ".join(argtypes)}]'


for d in definitions:
    if d.startswith('//'):
        continue
    if 'typedef' in d:
        if '(*' in d:
            typedef_funcptr_def(w, d)
        elif 'int' in d:
            typedef_int(w, d)
        elif 'struct' in d:
            typedef_struct(w, d)
        elif 'enum' in d:
            typedef_enum(w, d)
    else:
        if '=' in d:
            continue
        func_def(w, d)
    w += ''

with open('cyber/lib.py', 'w') as f:
    f.write(w.join(''))
