# cyberlang - batteries included python bindings for cyber

[![license](https://img.shields.io/pypi/l/cyberlang.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/cyberlang.svg)](https://pypi.org/project/cyberlang/)
[![PyPI status](https://img.shields.io/pypi/status/cyberlang.svg)](https://github.com/qtstrap/qtstrap)
[![discord](https://img.shields.io/discord/828041790711136274)](https://discord.gg/Ky8vNZJvAT)

## Installation

```
pip install cyberlang
```

## Usage

Simply create a CyberVM instance and evaluate a string:

```py
from cyber import CyberVM

vm = CyberVM()
vm.eval("print 'hello world!'")
```

Want to capture printed output? Override the `print` function from Cyber's `core` module with a binding.

The decorator generates all the required wrappers and interfaces, and registers everything with Cyber's VM.

```py
from cyber import CyberVM

vm = CyberVM()

@vm.function('core.print')
def _print(string: str):
    print(string)

vm.eval("print 'hello world!'")
```

Alternate techniques for creating callback functions:

```py
# if no module, assume core
# same result as previous example
# this creates function "print2" in the "core" module
@cyber.function('print2')
def _print2(string: str):
    print(string)

# if no module, assume core
# if no function name, use existing function name
# this creates function "test" in the "core" module
@cyber.function
def test():
    print('core.test')
```

Or define multiple functions at once using this class-based syntax

```py
# "core" already exists, so add a() and b() to it
class Core(cyber.module('core')):
    def a(self):
        print('core.test')
    def b(self):
        print('core.test2')

# create "new_module" and add c() and d() to it
@cyber.module('new_module')
class Module:
    def c(self):
        print('new_module.test')
    def d(self):
        print('new_module.test2')

# create module, implicitly named "NewModule" and add e() and f() to it
@cyber.module
class NewModule:
    def e(self):
        print('NewModule.test')
    def f(self):
        print('NewModule.test2')
```

# Supporters

[fubar](https://github.com/fubark) - creator of the Cyber language