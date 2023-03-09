from ctypes import *
import inspect
from .lib import *
from . import lib
from textwrap import dedent
import builtins


# *************************************************************************** #


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


def generate_callback_wrapper(func):
    sig = inspect.signature(func)
    nargs = len(sig.parameters)
    return_type = sig.return_annotation

    # TODO: probably not a robust way to do this
    if 'self' in sig.parameters:
        nargs = nargs - 1

    @CyFunc
    def wrapper(vm, args, nargs):
        # convert args based on registered function signature
        _args = []
        i = 0
        for name, param in sig.parameters.items():
            # TODO: probably not a robust way to do this
            if name == 'self':
                _args.append(0)
                continue
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
            i += 1

        raw_ret = func(*_args)

        ret = 0

        # TODO: FFI return types
        # convert return type
        # match return_type:
            # case None:
            #     ret = cyValueNone()
            # case builtins.str:
            #     ret = cyValueGetOrAllocStringInfer(vm, cstr(raw_ret))

        return ret

    return wrapper, nargs


# TODO rename this something else, because the context manager syntax is gone
class ContextModule:
    def __init__(self, cyber, name) -> None:
        self.cyber = cyber
        self.name = name
        self.functions = []
        self.variables = []

    def function(self, name):
        def _decorator(func):
            # print(f'[ContextModule]: registering function: {name} {func}')
            wrapper, nargs = generate_callback_wrapper(func)
            self.functions.append((name, wrapper, nargs))
            return func

        return _decorator

    # def variable(self, name, nargs=0):
    #     def _decorator(func):
    #         self.variables.append((name, CyFunc(func), nargs))

    #     return _decorator

    def build(self):
        @CyLoadModuleFunc
        def load_module(vm, mod):
            # print(f'[ContextModule]: loading module: {self.name}')
            for name, nargs, wrapper in self.functions:
                # print(f'[ContextModule]: registering function: {name} {func}')
                self.cyber.set_module_func(mod, name, nargs, wrapper)
            return True

        self.load_module = load_module
        self.cyber.add_module_loader(self.name, load_module)


class CyberVM:
    def __init__(self) -> None:
        self.last_result = None
        self.last_output_type = None
        self.last_output = None

        self.vm = cyVmCreate()
        self.modules = []
        self.pending_modules = {}
        self.pending_module_classes = []

    def add_module_loader(self, name, loader):
        cyVmAddModuleLoader(self.vm, cstr(name), loader)

    def set_module_func(self, mod, name, nargs, func):
        cyVmSetModuleFunc(self.vm, mod, cstr(name), nargs, func)

    def set_module_var(self, mod, name, value):
        cyVmSetModuleVar(self.vm, mod, cstr(name), value)

    def function(self, name):
        module_name = 'core'
        func_name = name
        if '.' in name:
            module_name, func_name = name.split('.')
        def _decorator(func):
            wrapper, nargs = generate_callback_wrapper(func)            

            if module_name not in self.pending_modules:
                self.pending_modules[module_name] = {'funcs':[], 'vars':[]}
            self.pending_modules[module_name]['funcs'].append((func_name, nargs, wrapper))
            return func
        return _decorator

    def module(self, name):
        class ModuleClass:
            _name = name
        self.pending_module_classes.append(ModuleClass)
        return ModuleClass

    def _get_module(self, name):
        mod = ContextModule(self, name)
        self.modules.append(mod)
        return mod

    def build_pending_modules(self):
        for cls in self.pending_module_classes:
            for sub in cls.__subclasses__():
                for func in [ m for m in dir(sub) if callable(getattr(sub, m)) and not m.startswith('__')]:
                    dec = self.function(f'{sub._name}.{func}')
                    dec(getattr(sub, func))
                
        for module_name, contents in self.pending_modules.items():
            mod = self._get_module(module_name)
            mod.functions = contents['funcs']
            mod.build()

        self.pending_modules.clear()
        self.pending_module_classes.clear()

    def validate(self, src: str | bytes):
        self.build_pending_modules()

        self.last_output_type = None
        self.last_output = None
        result = cyVmValidate(self.vm, cstr(src))
        self.last_result = CyResultCode(result)
        return cyVmGetLastErrorReport(self.vm).charz
        # if self.last_result != CyResultCode.CY_Success:
        #     match self.last_result:
        #         case CyResultCode.CY_ErrorToken:
        #             raise CyberTokenError
        #         case CyResultCode.CY_ErrorParse:
        #             raise CyberParseError
        #         case CyResultCode.CY_ErrorCompile:
        #             raise CyberCompileError
        #         case CyResultCode.CY_ErrorPanic:
        #             raise CyberPanicError
        #         case CyResultCode.CY_ErrorUnknown:
        #             raise CyberUnknownError
        #     raise CyberUnknownError
        
    def eval(self, src: str | bytes):
        self.build_pending_modules()

        self.last_output_type = None
        self.last_output = None
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
        
        self.last_output_type = CyType(cyValueGetTypeId(out).value)
        self.last_output = cyvalue_to_py(self.vm, out)
        return self.last_output

    def exec(self, src: str | bytes) -> None:
        self.eval(src)