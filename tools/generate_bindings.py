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


with open('cyber/src/cyber.h') as f:
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
w += ''

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


types = {
    'bool': 'c_bool',
    'double': 'c_double',
    'void*': 'c_void_p',
    'char*': 'c_char_p',
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
    t = m[1]
    fields = m[2]
    types[f'{t}*'] = f'POINTER({t})'
    w += f'class {m[1]}(Structure):'

    with w:
        if fields:
            _fields = []
            for f in fields[1:-1].split(';'):
                if f:
                    parts = f.strip().split(' ')
                    t = types.get(parts[0], parts[0])
                    _fields.append(f"('{parts[1]}', {t})")
            w += f"_fields_ = [{', '.join(_fields)}]"
        else:
            w += '...'


def typedef_enum(w, d):
    w += f'# enum'


def typedef_funcptr_def(w, d):
    m = re.match(r'typedef (\w+) \(\*(\w+)\)(.*);', d)
    t = m[2]
    args = m[3][1:-1].split(', ')
    arg_types = [a.split(' ')[0] for a in args]
    w += f'# {d}'
    argtypes = [types.get(m[1], m[1])]
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))
    w += f'{t} = CFUNCTYPE({", ".join(argtypes)})'


def func_def(w, d):
    w += f'# {d}'
    m = re.match(r'(\w+\*?) (\w+)(.*);', d)
    ret = m[1]
    args = m[3][1:-1].split(', ')
    arg_types = [a.split(' ')[0] for a in args]
    w += f'{m[2]} = lib.{m[2]}'

    if ret != 'void':
        w += f'{m[2]}.restype = {types.get(ret, ret)}'

    argtypes = []
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))
    w += f'{m[2]}.argtypes = [{", ".join(argtypes)}]'

    w += ''


for d in definitions:
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

with open('src/cyber/lib.py', 'w') as f:
    f.write(w.join(''))
