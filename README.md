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

```py
from cyber import CyberVM

vm = CyberVM()
vm.eval("print 'hello world!'")
```


```py
from cyber import CyberVM

vm = CyberVM()

# override cyber's print function with a python callback
@vm.function('core.print')
    def _print(string: str):
        print(string)

vm.eval("print 'hello world!'")
```

# Supporters

[fubar](https://github.com/fubark) - creator of the Cyber language