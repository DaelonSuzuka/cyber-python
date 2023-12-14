import re
from pathlib import Path


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


with open('cyber/lib/cyber.h') as f:
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

w += open(Path(__file__).parent / 'bindings_preamble.py').read()

types = {
    'void': 'None',
    'bool': 'c_bool',
    'double': 'c_double',
    'void*': 'c_void_p',
    'char*': 'c_char_p',
    'const char*': 'c_char_p',
    'size_t': 'c_size_t',
    'uint8_t': 'c_uint8',
    'uint8_t*': 'POINTER(c_uint8)',
    'uint32_t': 'c_uint32',
    'uint64_t': 'c_uint64',
    'int8_t': 'c_int8',
    'int32_t': 'c_int32',
    'int64_t': 'c_int64',
    'int': 'c_int',
    'CsResultCode': 'c_int',
}


def typedef_int(w, d):
    m = re.match(r'typedef (\w+) (\w*)', d)
    if m is None:
        return
    t = m[1]
    types[f'{m[2]}*'] = f'POINTER({m[2]})'
    w += f'class {m[2]}({types.get(t, t)}):'
    with w:
        w += '...'


def typedef_struct(w, d):
    m = re.match(r'typedef (struct|union) (\w+) ({.*})?', d.replace('\n', ''))
    if m is None:
        return
    def_type = m[1]
    struct_name = m[2]
    body = m[3]
    types[f'{struct_name}*'] = f'POINTER({struct_name})'
    if struct_name == 'CsTypeResult':
        w += f'class {struct_name}(Structure):'
        with w:
            w += "..."
        return
    fields = []
    if body:
        for f in body[1:-1].split(';'):
            if f:
                parts = f.strip().replace('const ', '').split(' ')
                name = parts[-1]
                c_type = ' '.join(parts[:-1])
                py_type = types.get(c_type, c_type)
                fields.append(f"('{name}', {py_type})")

    if def_type == 'union':
        # TODO: actually support unions
        # TODO: probably requires supporting arbitrarily nested struct/union defs
        w += f'class {struct_name}(Union):'
        with w:
            w += '# unions not supported yet'
            w += '...'

    if def_type == 'struct':
        w += f'class {struct_name}(Structure):'
        with w:
            if fields:
                w += f"_fields_ = [{', '.join(fields)}]"
            else:
                w += '...'


def typedef_enum(w, d):
    m = re.match(r'typedef enum ({.*})? (\w+);', d.replace('\n', ''))
    if m is None:
        return
    values = m[1]
    enum_name = m[2]
    items = [v.strip().replace(' = 0', '') for v in values[1:-1].split(',') if v]

    w += f'class {enum_name}(Enum):'
    with w:
        # w += f'"""{d}"""'
        for i, item in enumerate(items):
            w += f'{item} = {i}'


def typedef_funcptr_def(w, d):
    m = re.match(r'typedef (\w+) \(\*(\w+)\)(.*);', d)
    if m is None:
        return
    type_name = m[2]
    args = m[3][1:-1].split(', ')
    arg_types = [a.replace('const ', '').split(' ')[0] for a in args]
    argtypes = [types.get(m[1], m[1])]
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))

    w += f'{type_name} = CFUNCTYPE({", ".join(argtypes)})'
    w += f'"""{d}"""'


def func_def(w, d):
    m = re.match(r'((?:const\s)?\w+\*?) (\w+)(.*);', d)
    if m is None:
        return
    func_name = m[2]
    ret = m[1]
    args = m[3][1:-1].split(', ')
    arg_types = [a.replace('const ', '').split(' ')[0] for a in args]
    argtypes = []
    for arg in arg_types:
        argtypes.append(types.get(arg, arg))

    w += f'{func_name} = lib.{func_name}'
    w += f'"""{d}"""'
    if ret != 'void':
        w += f'{func_name}.restype = {types.get(ret, ret)}'
    w += f'{func_name}.argtypes = [{", ".join(argtypes)}]'


def extern_bool(w, d):
    m = re.match(r'extern bool (.+);', d)
    if m is None:
        return
    w += f'# {m[1]} = lib.{m[1]}'
    w += f'"""{d}"""'


for d in definitions:
    if d.startswith('//'):
        continue
    if 'typedef' in d:
        if 'enum' in d:
            typedef_enum(w, d)
        elif '(*' in d:
            typedef_funcptr_def(w, d)
        elif 'int' in d.split(' ')[1]:
            typedef_int(w, d)
        elif 'struct' in d:
            typedef_struct(w, d)
    else:
        if '=' in d:
            continue
        elif 'extern bool' in d:
            extern_bool(w, d)
        else:
            func_def(w, d)
    w += ''

with open('cyber/lib.py', 'w') as f:
    f.write(w.join(''))
