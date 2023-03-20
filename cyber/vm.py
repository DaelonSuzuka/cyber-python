from ctypes import (
    c_char_p,
    pointer,
)
import inspect
from .lib import (
    CStr,
    CyFunc,
    CyValue,
    CyType,
    CyResultCode,
    CyLoadModuleFunc,
)
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


def py_to_cyvalue(vm, value) -> CyValue:
    match type(value):
        case builtins.bool:
            return lib.cyValueTrue() if value else lib.cyValueFalse()
        case builtins.int:
            return lib.cyValueInteger(value)
        case builtins.float:
            return lib.cyValueNumber(value)
        case builtins.str:
            return lib.cyValueGetOrAllocStringInfer(vm, cstr(value))
        case _:
            return lib.cyValueNone()


def cyvalue_to_py(vm, cyvalue):
    match CyType(lib.cyValueGetTypeId(cyvalue).value):
        case CyType.CY_TypeNone:
            return None
        case CyType.CY_TypeBoolean:
            return lib.cyValueAsBool(cyvalue)
        case CyType.CY_TypeInteger:
            return lib.cyValueAsInteger(cyvalue)
        case CyType.CY_TypeNumber:
            return lib.cyValueAsNumber(cyvalue)
        case CyType.CY_TypeStaticAstring:
            return lib.cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeStaticUstring:
            return lib.cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeAstring:
            return lib.cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeUstring:
            return lib.cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeStringSlice:
            return lib.cyValueToTempString(vm, cyvalue).charz.decode()
        case CyType.CY_TypeRawString:
            return lib.cyValueToTempRawString(vm, cyvalue).charz
        case CyType.CY_TypeRawStringSlice:
            return lib.cyValueToTempRawString(vm, cyvalue).charz
        case _:
            return cyvalue


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
                    _args.append(lib.cyValueToTempString(vm, args[i]).charz.decode())
                case builtins.int:
                    _args.append(int(lib.cyValueAsNumber(args[i])))
                case builtins.float:
                    _args.append(lib.cyValueAsNumber(args[i]))
                case builtins.bool:
                    _args.append(lib.cyValueToBool(args[i]))
                case lib.CyValue: # raw lib.cyValue
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
            #     ret = lib.cyValueNone()
            # case builtins.str:
            #     ret = lib.cyValueGetOrAllocStringInfer(vm, cstr(raw_ret))

        return ret

    return wrapper, nargs


class Module:
    def __init__(self, cyber, name, contents) -> None:
        self.cyber = cyber
        self.name = name
        self.functions = contents['funcs']
        self.variables = contents['vars']
        self.build()

    def build(self):
        @CyLoadModuleFunc
        def load_module(vm, mod):
            # print(f'[ContextModule]: loading module: {self.name}')
            for func_info in self.functions:
                # print(f'[ContextModule]: registering function: {name}')
                self.cyber.set_module_func(mod, *func_info)

            for var_info in self.variables:
                self.cyber.set_module_var(mod, *var_info)

            return True

        self.load_module = load_module
        self.cyber.add_module_loader(self.name, load_module)


class CyberVM:
    def __init__(self) -> None:
        self.last_result = None
        self.last_output_type = None
        self.last_output = None

        self.vm = lib.cyVmCreate()
        self.modules = []
        self.pending_modules = {}
        self.pending_module_classes = []

    def add_module_loader(self, name, loader):
        lib.cyVmAddModuleLoader(self.vm, cstr(name), loader)

    def set_module_func(self, mod, name, nargs, func):
        lib.cyVmSetModuleFunc(self.vm, mod, cstr(name), nargs, func)

    def set_module_var(self, mod, name, value):
        lib.cyVmSetModuleVar(self.vm, mod, cstr(name), py_to_cyvalue(self.vm, value))

    def _ensure_module(self, module_name):
        if module_name not in self.pending_modules:
            self.pending_modules[module_name] = {'funcs':[], 'vars':[]}
    
    def function(self, name):
        if isinstance(name, str):
            module_name = 'core'
            func_name = name
            if '.' in name:
                module_name, func_name = name.split('.')
            def _decorator(func):
                wrapper, nargs = generate_callback_wrapper(func)            
                self._ensure_module(module_name)
                self.pending_modules[module_name]['funcs'].append((func_name, nargs, wrapper))
                return func
            return _decorator
        else:
            # we ARE the decorator
            func = name
            module_name = 'core'
            func_name = func.__name__
            wrapper, nargs = generate_callback_wrapper(func)            

            self._ensure_module(module_name)
            self.pending_modules[module_name]['funcs'].append((func_name, nargs, wrapper))

            return func
        
    def variable(self, name, value):
        module_name = 'core'
        var_name = name
        if '.' in name:
            module_name, var_name = name.split('.')

        self._ensure_module(module_name)
        self.pending_modules[module_name]['vars'].append((var_name, value))

    def module(self, name):
        if isinstance(name, str):
            class ModuleClass:
                _name = name

                def __new__(cls, kls):
                    """should only be called as a class decorator"""
                    kls._name = cls._name
                    self.pending_module_classes.append(kls)
                    return cls, kls
                    
            self.pending_module_classes.append(ModuleClass)
            return ModuleClass
        else:
            # we ARE the decorator
            kls = name
            kls._name = kls.__name__
            
            self.pending_module_classes.append(kls)
            return kls

    def build_pending_modules(self):
        def get_funcs(klass):
            for func in [m for m in dir(klass) if callable(getattr(klass, m)) and not m.startswith('__')]:
                dec = self.function(f'{klass._name}.{func}')
                dec(getattr(klass, func))

        def get_vars(klass):
            for var in [m for m in dir(klass) if not callable(getattr(klass, m)) and not m.startswith('__')]:
                self.variable(f'{klass._name}.{var}', getattr(klass, var))

        for klass in self.pending_module_classes:
            get_funcs(klass)
            get_vars(klass)
            for sub in klass.__subclasses__():
                get_funcs(sub)
                get_vars(sub)

        for module_name, contents in self.pending_modules.items():
            mod = Module(self, module_name, contents)
            self.modules.append(mod)

        self.pending_modules.clear()
        self.pending_module_classes.clear()

    def validate(self, src: str | bytes):
        self.build_pending_modules()

        self.last_output_type = None
        self.last_output = None
        result = lib.cyVmValidate(self.vm, cstr(src))
        self.last_result = CyResultCode(result)
        return lib.cyVmGetLastErrorReport(self.vm).charz
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
        result = lib.cyVmEval(self.vm, cstr(src), pointer(out))
        self.last_result = CyResultCode(result)
        if self.last_result != CyResultCode.CY_Success:
            report = lib.cyVmGetLastErrorReport(self.vm).charz
            match self.last_result:
                case CyResultCode.CY_ErrorToken:
                    raise CyberTokenError(report)
                case CyResultCode.CY_ErrorParse:
                    raise CyberParseError(report)
                case CyResultCode.CY_ErrorCompile:
                    raise CyberCompileError(report)
                case CyResultCode.CY_ErrorPanic:
                    raise CyberPanicError(report)
                case CyResultCode.CY_ErrorUnknown:
                    raise CyberUnknownError(report)
            raise CyberUnknownError
        
        self.last_output_type = CyType(lib.cyValueGetTypeId(out).value)
        self.last_output = cyvalue_to_py(self.vm, out)
        return self.last_output

    def exec(self, src: str | bytes) -> None:
        self.eval(src)