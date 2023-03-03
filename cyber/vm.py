from ctypes import *
from pathlib import Path


default_lib_path = (Path(__file__).parent / 'lib/cyber.dll').as_posix()


class UserVM(Structure):
    pass


class CyModule(Structure):
    pass


class CStr(Structure):
    _fields_ = [
        ("charz", c_char_p),
        ("len", c_size_t)
    ]


class ResultCode:
    CY_Success = 0
    CY_ErrorToken = 1
    CY_ErrorParse = 2
    CY_ErrorCompile = 3
    CY_ErrorPanic = 4
    CY_ErrorUnknown = 5


class CyberVM:
    def __init__(self, lib_path=default_lib_path) -> None:
        self.lib = WinDLL(lib_path)

        self.vm_create = self.lib.cyVmCreate
        self.vm_create.restype = c_void_p

        self.vm_eval = self.lib.cyVmEval
        self.vm_eval.restype = c_int
        self.vm_eval.argtypes = [c_void_p, CStr, POINTER(c_uint64)]
        
        self.vm_get_last_error = self.lib.cyVmGetLastErrorReport
        self.vm_get_last_error.restype = CStr
        self.vm_get_last_error.argtypes = [c_void_p]
        
        self.vm = self.vm_create()

    def eval(self, src:str|bytes):
        if isinstance(src, str):
            src = src.encode()

        cstr = CStr(c_char_p(src), len(src))

        out = c_uint64(0)
        outptr = pointer(out)

        result = self.vm_eval(self.vm, cstr, outptr)

        # print(out)

        # if result != ResultCode.CY_Success:
        #     pass