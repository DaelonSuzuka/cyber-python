from ctypes import *
import inspect
from .lib import *


# *************************************************************************** #


def cstr(s) -> CStr:
    if isinstance(s, str):
        s = s.encode()
    return CStr(c_char_p(s), len(s))


class ContextModule:
    def __init__(self, cyber, name) -> None:
        self.cyber = cyber
        self.name = name
        self.functions = []
        self.variables = []

    def function(self, name):
        def _decorator(func):
            # print(f'[ContextModule]: registering function: {name} {func}')

            sig = inspect.signature(func)
            nargs = len(sig.parameters)
            return_type = sig.return_annotation

            @CyFunc
            def wrapper(vm, args, nargs):
                _args = []
                # automatically convert args based on registered function signature
                for i, param in enumerate(sig.parameters.values()):
                    if param.annotation == str:
                        s = cyValueToTempString(vm, args[i])
                        _args.append(s.charz.decode())
                    elif param.annotation == int:
                        val = int(cyValueAsNumber(args[i]))
                        _args.append(val)
                    elif param.annotation == float:
                        val = cyValueAsNumber(args[i])
                        _args.append(val)
                    # elif param.annotation == bool:
                    #     val = args[i] == cyValueTrue()
                    #     _args.append(val)
                    else:   # raw cyValue, hopefully this doesn't happen
                        _args.append(args[i])

                ret = func(*_args)

                # convert return type
                # if return_type == None:
                #     ret = cyValueNone()

                return 0

            self.functions.append((name, wrapper, nargs, wrapper, func))
            return func

        return _decorator

    # def variable(self, name, nargs=0):
    #     def _decorator(func):
    #         self.variables.append((name, CyFunc(func), nargs))

    #     return _decorator

    def __enter__(self):
        return self

    def __exit__(self, *_):
        @CyLoadModuleFunc
        def load_module(vm, mod):
            # print(f'[ContextModule]: loading module: {self.name}')
            for name, func, nargs, *_ in self.functions:
                # print(f'[ContextModule]: registering function: {name} {func}')
                self.cyber.set_module_func(mod, name, nargs, func)
            return True

        self.load_module = load_module
        self.cyber.add_module_loader(self.name, load_module)
        return


class CyberVM:
    def __init__(self) -> None:
        self.vm = cyVmCreate()
        self.modules = []

    def add_module_loader(self, name, loader):
        cyVmAddModuleLoader(self.vm, cstr(name), loader)

    def set_module_func(self, mod, name, nargs, func):
        cyVmSetModuleFunc(self.vm, mod, cstr(name), nargs, func)

    def set_module_var(self, mod, name, value):
        cyVmSetModuleVar(self.vm, mod, cstr(name), value)

    def module(self, name):
        mod = ContextModule(self, name)
        self.modules.append(mod)
        return mod

    def eval(self, src: str | bytes):

        out = CyValue()
        result = cyVmEval(self.vm, cstr(src), pointer(out))

        # print(out)

        # if result != ResultCode.CY_Success:
        #     pass
