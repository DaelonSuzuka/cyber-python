from ctypes import *
from pathlib import Path
import inspect
import sys


class UserVM(Structure):
    ...


class CyModule(Structure):
    ...


class CyValue(c_uint64):
    ...


class CStr(Structure):
    _fields_ = [('charz', c_char_p), ('len', c_size_t)]


def cstr(s) -> CStr:
    if isinstance(s, str):
        s = s.encode()
    return CStr(c_char_p(s), len(s))


class ResultCode:
    CY_Success = 0
    CY_ErrorToken = 1
    CY_ErrorParse = 2
    CY_ErrorCompile = 3
    CY_ErrorPanic = 4
    CY_ErrorUnknown = 5


# *************************************************************************** #

base_path = Path(__file__).parent / 'lib'
mode = 'release'

if sys.platform == 'win32':
    path = base_path / mode / 'cyber.dll'
    lib = WinDLL(path.as_posix())
elif sys.platform == 'linux':
    path = base_path / mode / 'libcyber.so'
    lib = CDLL(path.as_posix())
# elif sys.platform == 'darwin':
#     path = base_path / mode / 'libcyber.so'
#     lib = CDLL(path.as_posix())


# CyUserVM* cyVmCreate();
cyVmCreate = lib.cyVmCreate
cyVmCreate.restype = POINTER(UserVM)

# CyResultCode cyVmEval(CyUserVM* vm, CStr src, CyValue* outVal);
cyVmEval = lib.cyVmEval
cyVmEval.restype = c_int
cyVmEval.argtypes = [POINTER(UserVM), CStr, POINTER(CyValue)]

# CStr cyVmGetLastErrorReport(CyUserVM* vm);
cyVmGetLastErrorReport = lib.cyVmGetLastErrorReport
cyVmGetLastErrorReport.restype = CStr
cyVmGetLastErrorReport.argtypes = [POINTER(UserVM)]

# *************************************************************************** #

# void* cyVmGetUserData(CyUserVM* vm);
# void cyVmSetUserData(CyUserVM* vm, void* userData);

# typedef CyValue (*CyFunc)(CyUserVM* vm, CyValue* args, uint8_t nargs);
CyFunc = CFUNCTYPE(CyValue, POINTER(UserVM), POINTER(CyValue), c_uint8)

# typedef bool (*CyLoadModuleFunc)(CyUserVM* vm, CyModule* mod);
CyLoadModuleFunc = CFUNCTYPE(c_bool, POINTER(UserVM), POINTER(CyModule))

# void cyVmAddModuleLoader(CyUserVM* vm, CStr name, CyLoadModuleFunc func);
cyVmAddModuleLoader = lib.cyVmAddModuleLoader
cyVmAddModuleLoader.argtypes = [POINTER(UserVM), CStr, CyLoadModuleFunc]

# void cyVmSetModuleFunc(CyUserVM* vm, CyModule* mod, CStr name, uint32_t numParams, CyFunc func);
cyVmSetModuleFunc = lib.cyVmSetModuleFunc
cyVmSetModuleFunc.argtypes = [POINTER(UserVM), POINTER(CyModule), CStr, c_uint32, CyFunc]

# void cyVmSetModuleVar(CyUserVM* vm, CyModule* mod, CStr name, CyValue val);
cyVmSetModuleVar = lib.cyVmSetModuleVar
cyVmSetModuleVar.argtypes = [POINTER(UserVM), POINTER(CyModule), CStr, CyValue]

# *************************************************************************** #

cyValueNone = lib.cyValueNone
cyValueNone.restype = CyValue

cyValueTrue = lib.cyValueTrue
cyValueTrue.restype = CyValue

cyValueFalse = lib.cyValueFalse
cyValueFalse.restype = CyValue

cyValueNumber = lib.cyValueNumber
cyValueNumber.restype = CyValue
cyValueNumber.argtypes = [c_double]

cyValueGetOrAllocStringInfer = lib.cyValueGetOrAllocStringInfer
cyValueGetOrAllocStringInfer.restype = CyValue
cyValueGetOrAllocStringInfer.argtypes = [POINTER(UserVM), CStr]

# --------------------------------------------------------------------------- #

cyValueAsDouble = lib.cyValueAsDouble
cyValueAsDouble.restype = c_double
cyValueAsDouble.argtypes = [CyValue]

cyValueToTempString = lib.cyValueToTempString
cyValueToTempString.restype = CStr
cyValueToTempString.argtypes = [POINTER(UserVM), CyValue]

cyValueToTempRawString = lib.cyValueToTempRawString
cyValueToTempRawString.restype = CStr
cyValueToTempRawString.argtypes = [POINTER(UserVM), CyValue]

# *************************************************************************** #


class ContextModule:
    def __init__(self, cyber, name) -> None:
        self.cyber = cyber
        self.name = name
        self.functions = []
        self.variables = []

    def function(self, name):
        def _decorator(func):
            print(f'[ContextModule]: registering function: {name} {func}')

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
                        val = int(cyValueAsDouble(args[i]))
                        _args.append(val)
                    elif param.annotation == float:
                        val = cyValueAsDouble(args[i])
                        _args.append(val)
                    # elif param.annotation == bool:
                    #     val = args[i] == cyValueTrue()
                    #     _args.append(val)
                    else: # raw cyValue, hopefully this doesn't happen
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
            print(f'[ContextModule]: loading module: {self.name}')
            for name, func, nargs, *_ in self.functions:
                print(f'[ContextModule]: registering function: {name} {func}')
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
