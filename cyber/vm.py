from ctypes import *
import inspect
from .lib import *
from . import lib
from textwrap import dedent
import builtins


# *************************************************************************** #


def cstr(s) -> CStr:
    if isinstance(s, str):
        s = dedent(s).encode()
    return CStr(c_char_p(s), len(s))


def cyvalue_to_py(vm, cyvalue):
    match CyType(cyValueGetTypeId(cyvalue).value):
        case CyType.CY_TypeNone:
            return None
        case CyType.CY_TypeBoolean:
            return cyValueAsBool(cyvalue)
        case CyType.CY_TypeInteger:
            return cyValueAsInteger(cyvalue)
        case CyType.CY_TypeNumber:
            return cyValueAsNumber(cyvalue)
        case CyType.CY_TypeStaticAstring:
            return cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeStaticUstring:
            return cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeAstring:
            return cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeUstring:
            return cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeStringSlice:
            return cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeRawString:
            return cyValueToTempRawString(vm, cyvalue).charz
        case CyType.CY_TypeRawStringSlice:
            return cyValueToTempRawString(vm, cyvalue).charz


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
                # convert args based on registered function signature
                for i, param in enumerate(sig.parameters.values()):
                    match param.annotation:
                        case builtins.str:
                            _args.append(cyValueToTempString(vm, args[i]).charz.decode())
                        case builtins.int:
                            _args.append(int(cyValueAsNumber(args[i])))
                        case builtins.float:
                            _args.append(cyValueAsNumber(args[i]))
                        case builtins.bool:
                            _args.append(cyValueToBool(args[i]))
                        case lib.CyValue: # raw cyValue
                            _args.append(args[i])
                        case _: # no type specified, try to auto-convert
                            _args.append(cyvalue_to_py(vm, args[i]))

                raw_ret = func(*_args)

                ret = 0

                # convert return type
                # match return_type:
                    # case None:
                    #     ret = cyValueNone()
                    # case builtins.str:
                    #     ret = cyValueGetOrAllocStringInfer(vm, cstr(raw_ret))

                return ret

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


class CyberTokenError(Exception):
    ...
class CyberParseError(Exception):
    ...
class CyberCompileError(Exception):
    ...
class CyberPanicError(Exception):
    ...
class CyberUnknownError(Exception):
    ...


class CyberVM:
    def __init__(self) -> None:
        self.last_result = None
        self.last_output_type = None
        self.last_output = None

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
        self.last_result = CyResultCode(result)
        if self.last_result != CyResultCode.CY_Success:
            match self.last_result:
                case CyResultCode.CY_ErrorToken:
                    raise CyberTokenError
                case CyResultCode.CY_ErrorParse:
                    raise CyberParseError
                case CyResultCode.CY_ErrorCompile:
                    raise CyberCompileError
                case CyResultCode.CY_ErrorPanic:
                    raise CyberPanicError
                case CyResultCode.CY_ErrorUnknown:
                    raise CyberUnknownError
            raise CyberUnknownError
            return
        
        self.last_output_type = CyType(cyValueGetTypeId(out).value)
        self.last_output = cyvalue_to_py(self.vm, out)
        return self.last_output
