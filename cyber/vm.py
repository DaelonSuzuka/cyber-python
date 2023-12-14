from ctypes import (
    c_char_p,
    pointer,
)
import inspect
from .lib import (
    CsPrintFn,
    CsFuncFn,
    CsStr,
    CsValue,
    CsType,
    CsResultCode,
    csSetModuleLoader,
    csGetPrint,
    csSetPrint,
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


def cstr(s) -> CsStr:
    if isinstance(s, str):
        s = dedent(s).encode()
    return CsStr(c_char_p(s), len(s))


def py_to_cyvalue(vm, value) -> CsValue:
    match type(value):
        case builtins.bool:
            return lib.csTrue() if value else lib.csFalse()
        case builtins.int:
            return lib.csInteger(value)
        case builtins.float:
            return lib.csFloat(value)
        case builtins.str:
            return lib.csNewString(vm, cstr(value))
        case _:
            return lib.csNone()


def cyvalue_to_py(vm, cyvalue):
    match CsType(lib.csGetTypeId(cyvalue).value):
        case CsType.CS_TYPE_NONE:
            return None
        case CsType.CS_TYPE_BOOLEAN:
            return lib.csAsBool(cyvalue)
        case CsType.CS_TYPE_INTEGER:
            return lib.csAsInteger(cyvalue)
        case CsType.CS_TYPE_FLOAT:
            return lib.csAsFloat(cyvalue)
        case CsType.CS_TYPE_STRING:
            return lib.csToTempString(vm, cyvalue).buf.decode()
        # case CsType.CS_TYPE_ARRAY:
        #     return lib.csToTempByteArray(vm, cyvalue).buf
        case CsType.CS_TYPE_LIST:
            length = lib.csListLen(cyvalue)
            cylist = [lib.csListGet(vm, cyvalue, i) for i in range(length)]
            return [cyvalue_to_py(vm, cyval) for cyval in cylist]
        case _:
            return cyvalue


def generate_callback_wrapper(func):
    sig = inspect.signature(func)
    # return_type = sig.return_annotation

    @CsFuncFn
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
                    _args.append(lib.csToTempString(vm, args[i]).buf.decode())
                case builtins.int:
                    _args.append(int(lib.csAsFloat(args[i])))
                case builtins.float:
                    _args.append(lib.csAsFloat(args[i]))
                case builtins.bool:
                    _args.append(lib.csToBool(args[i]))
                case lib.CsValue: # raw lib.cs
                    _args.append(args[i])
                case _: # no type specified, try to auto-convert
                    _args.append(cyvalue_to_py(vm, args[i]))
            i += 1
            # quit when all args have been consumed
            # allows default parameters in wrapped functions
            if i == nargs:
                break

        raw_ret = func(*_args)

        ret = 0

        # TODO: FFI return types
        # convert return type
        # match return_type:
            # case None:
            #     ret = lib.csNone()
            # case builtins.str:
            #     ret = lib.csGetOrAllocStringInfer(vm, cstr(raw_ret))

        return ret

    return wrapper


# class Module:
#     def __init__(self, cyber, name, contents) -> None:
#         self.cyber = cyber
#         self.name = name
#         self.functions = contents['funcs']
#         self.variables = contents['vars']
#         self.build()

#     def build(self):
#         @CsLoadModuleFunc
#         def load_module(vm, mod):
#             # print(f'[ContextModule]: loading module: {self.name}')
#             for func_info in self.functions:
#                 # print(f'[ContextModule]: registering function: {name}')
#                 self.cyber.set_module_func(mod, *func_info)

#             for var_info in self.variables:
#                 self.cyber.set_module_var(mod, *var_info)

#             return True

#         self.load_module = load_module
#         self.cyber.add_module_loader(self.name, load_module)


class CyberVM:
    def __init__(self) -> None:
        self.last_result = None
        self.last_output_type = None
        self.last_output = None

        self.vm = lib.csCreate()
        self.modules = []
        self.pending_modules = {}
        self.pending_module_classes = []

    def get_print(self):
        return csGetPrint(self.vm)

    def set_print(self, func):
        print('set_print')

        @CsPrintFn
        def wrapper(vm, a):
            print('wrapper')
            # print(lib.csToTempString(vm, a).buf.decode())

        print(wrapper)
        csSetPrint(self.vm, wrapper)

    # def add_module_loader(self, name, loader):
    #     lib.csVmAddModuleLoader(self.vm, cstr(name), loader)

    # def set_module_func(self, mod, name, nargs, func):
    #     lib.cyVmSetModuleFunc(self.vm, mod, cstr(name), nargs, func)

    # def set_module_var(self, mod, name, value):
    #     lib.cyVmSetModuleVar(self.vm, mod, cstr(name), py_to_cyvalue(self.vm, value))

    # def _ensure_module(self, module_name):
    #     if module_name not in self.pending_modules:
    #         self.pending_modules[module_name] = {'funcs':[], 'vars':[]}
    
    # def generate_wrappers(self, module_name, func_name, func):
    #     sig = inspect.signature(func)
    #     nargs = len(sig.parameters)
    #     # TODO: probably not a robust way to do this
    #     if 'self' in sig.parameters:
    #         nargs = nargs - 1
    #     sigs = [nargs]

    #     optionals = 0
    #     for name, param in sig.parameters.items():
    #         if param.default != inspect._empty:
    #             optionals += 1
    #             sigs.append(nargs - optionals)

    #     wrapper = generate_callback_wrapper(func)

    #     for n in sigs:
    #         self.pending_modules[module_name]['funcs'].append((func_name, n, wrapper))

    def function(self, name):
        if isinstance(name, str):
            module_name = 'core'
            func_name = name
            if '.' in name:
                module_name, func_name = name.split('.')
            # self._ensure_module(module_name)
            def _decorator(func):
                # self.generate_wrappers(module_name, func_name, func)
                return func
            return _decorator
        else:
            # we ARE the decorator
            func = name
            # module_name = 'core'
            # self._ensure_module(module_name)
            # func_name = func.__name__
            # self.generate_wrappers(module_name, func_name, func)
            return func
        
    def variable(self, name, value):
        module_name = 'core'
        var_name = name
        if '.' in name:
            module_name, var_name = name.split('.')

        # self._ensure_module(module_name)
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

    # def build_pending_modules(self):
    #     def get_funcs(klass):
    #         for func in [m for m in dir(klass) if callable(getattr(klass, m)) and not m.startswith('__')]:
    #             dec = self.function(f'{klass._name}.{func}')
    #             dec(getattr(klass, func))

    #     def get_vars(klass):
    #         for var in [m for m in dir(klass) if not callable(getattr(klass, m)) and not m.startswith('__')]:
    #             self.variable(f'{klass._name}.{var}', getattr(klass, var))

    #     for klass in self.pending_module_classes:
    #         get_funcs(klass)
    #         get_vars(klass)
    #         for sub in klass.__subclasses__():
    #             get_funcs(sub)
    #             get_vars(sub)

    #     for module_name, contents in self.pending_modules.items():
    #         mod = Module(self, module_name, contents)
    #         self.modules.append(mod)

    #     self.pending_modules.clear()
    #     self.pending_module_classes.clear()

    def validate(self, src: str | bytes):
        # self.build_pending_modules()

        self.last_output_type = None
        self.last_output = None
        result = lib.csValidate(self.vm, cstr(src))
        self.last_result = CsResultCode(result)
        return lib.csNewLastErrorReport(self.vm)
        # if self.last_result != CsResultCode.CS_SUCCESS:
        #     match self.last_result:
        #         case CsResultCode.CS_ERROR_TOKEN:
        #             raise CyberTokenError
        #         case CsResultCode.CS_ERROR_PARSE:
        #             raise CyberParseError
        #         case CsResultCode.CS_ERROR_COMPILE:
        #             raise CyberCompileError
        #         case CsResultCode.CS_ERROR_PANIC:
        #             raise CyberPanicError
        #         case CsResultCode.CS_ERROR_UNKNOWN:
        #             raise CyberUnknownError
        #     raise CyberUnknownError
        
    def eval(self, src: str | bytes):
        # self.build_pending_modules()

        self.last_output_type = None
        self.last_output = None
        out = CsValue()
        result = lib.csEval(self.vm, cstr(src), pointer(out))
        self.last_result = CsResultCode(result)
        if self.last_result != CsResultCode.CS_SUCCESS:
            report = lib.csNewLastErrorReport(self.vm)
            match self.last_result:
                case CsResultCode.CS_ERROR_TOKEN:
                    raise CyberTokenError(report)
                case CsResultCode.CS_ERROR_PARSE:
                    raise CyberParseError(report)
                case CsResultCode.CS_ERROR_COMPILE:
                    raise CyberCompileError(report)
                case CsResultCode.CS_ERROR_PANIC:
                    raise CyberPanicError(report)
                case CsResultCode.CS_ERROR_UNKNOWN:
                    raise CyberUnknownError(report)
            raise CyberUnknownError
        
        self.last_output_type = CsType(lib.csGetTypeId(out).value)
        self.last_output = cyvalue_to_py(self.vm, out)
        return self.last_output

    def exec(self, src: str | bytes) -> None:
        self.eval(src)