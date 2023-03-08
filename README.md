# cyber-python

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