# GENERATED FILE DO NOT EDIT #

from ctypes import *
from pathlib import Path
import sys
from enum import Enum


base_path = Path(__file__).parent / 'lib'

if sys.platform == 'win32':
    path = base_path / 'cyber.dll'
    lib = WinDLL(path.as_posix())
elif sys.platform == 'linux':
    path = base_path / 'libcyber.so'
    lib = CDLL(path.as_posix())
elif sys.platform == 'darwin':
    if platform.machine() == 'arm64':
        path = base_path / 'libcyber-arm64.dylib'
        lib = CDLL(path.as_posix())
    else:
        path = base_path / 'libcyber.dylib'
        lib = CDLL(path.as_posix())


# GENERATED FILE DO NOT EDIT #

class CyUserVM(Structure):
    ...

class CyModule(Structure):
    ...

class CyValue(c_uint64):
    ...

class CyResultCode(Enum):
    CY_Success = 0
    CY_ErrorToken = 1
    CY_ErrorParse = 2
    CY_ErrorCompile = 3
    CY_ErrorPanic = 4
    CY_ErrorUnknown = 5

class CyType(Enum):
    CY_TypeNone = 0
    CY_TypeBoolean = 1
    CY_TypeError = 2
    CY_TypeStaticAstring = 3
    CY_TypeStaticUstring = 4
    CY_TypeUserTag = 5
    CY_TypeUserTagLiteral = 6
    CY_TypeInteger = 7
    CY_TypeNumber = 8
    CY_TypeList = 9
    CY_TypeListIter = 10
    CY_TypeMap = 11
    CY_TypeMapIter = 12
    CY_TypeClosure = 13
    CY_TypeLambda = 14
    CY_TypeAstring = 15
    CY_TypeUstring = 16
    CY_TypeStringSlice = 17
    CY_TypeRawString = 18
    CY_TypeRawStringSlice = 19
    CY_TypeFiber = 20
    CY_TypeBox = 21
    CY_TypeNativeFunc1 = 22
    CY_TypeTccState = 23
    CY_TypeOpaquePtr = 24
    CY_TypeFile = 25
    CY_TypeDir = 26
    CY_TypeDirIter = 27
    CY_TypeSymbol = 28

class CStr(Structure):
    _fields_ = [('charz', c_char_p), ('len', c_size_t)]

class CyTypeId(c_uint32):
    ...

# typedef CyValue (*CyFunc)(CyUserVM* vm, CyValue* args, uint8_t nargs);
CyFunc = CFUNCTYPE(CyValue, POINTER(CyUserVM), POINTER(CyValue), c_uint8)

# typedef bool (*CyLoadModuleFunc)(CyUserVM* vm, CyModule* mod);
CyLoadModuleFunc = CFUNCTYPE(c_bool, POINTER(CyUserVM), POINTER(CyModule))

# CyUserVM* cyVmCreate();
cyVmCreate = lib.cyVmCreate
cyVmCreate.restype = POINTER(CyUserVM)
cyVmCreate.argtypes = []

# void cyVmDestroy(CyUserVM* vm);
cyVmDestroy = lib.cyVmDestroy
cyVmDestroy.argtypes = [POINTER(CyUserVM)]

# CyResultCode cyVmEval(CyUserVM* vm, CStr src, CyValue* outVal);
cyVmEval = lib.cyVmEval
cyVmEval.restype = c_int
cyVmEval.argtypes = [POINTER(CyUserVM), CStr, POINTER(CyValue)]

# CStr cyVmGetLastErrorReport(CyUserVM* vm);
cyVmGetLastErrorReport = lib.cyVmGetLastErrorReport
cyVmGetLastErrorReport.restype = CStr
cyVmGetLastErrorReport.argtypes = [POINTER(CyUserVM)]

# void cyVmRelease(CyUserVM* vm, CyValue val);
cyVmRelease = lib.cyVmRelease
cyVmRelease.argtypes = [POINTER(CyUserVM), CyValue]

# void cyVmRetain(CyUserVM* vm, CyValue val);
cyVmRetain = lib.cyVmRetain
cyVmRetain.argtypes = [POINTER(CyUserVM), CyValue]

# void* cyVmGetUserData(CyUserVM* vm);
cyVmGetUserData = lib.cyVmGetUserData
cyVmGetUserData.restype = c_void_p
cyVmGetUserData.argtypes = [POINTER(CyUserVM)]

# void cyVmSetUserData(CyUserVM* vm, void* userData);
cyVmSetUserData = lib.cyVmSetUserData
cyVmSetUserData.argtypes = [POINTER(CyUserVM), c_void_p]

# void cyVmAddModuleLoader(CyUserVM* vm, CStr name, CyLoadModuleFunc func);
cyVmAddModuleLoader = lib.cyVmAddModuleLoader
cyVmAddModuleLoader.argtypes = [POINTER(CyUserVM), CStr, CyLoadModuleFunc]

# void cyVmSetModuleFunc(CyUserVM* vm, CyModule* mod, CStr name, uint32_t numParams, CyFunc func);
cyVmSetModuleFunc = lib.cyVmSetModuleFunc
cyVmSetModuleFunc.argtypes = [POINTER(CyUserVM), POINTER(CyModule), CStr, c_uint32, CyFunc]

# void cyVmSetModuleVar(CyUserVM* vm, CyModule* mod, CStr name, CyValue val);
cyVmSetModuleVar = lib.cyVmSetModuleVar
cyVmSetModuleVar.argtypes = [POINTER(CyUserVM), POINTER(CyModule), CStr, CyValue]

# void* cyVmAlloc(CyUserVM* vm, size_t size);
cyVmAlloc = lib.cyVmAlloc
cyVmAlloc.restype = c_void_p
cyVmAlloc.argtypes = [POINTER(CyUserVM), c_size_t]

# void cyVmFree(CyUserVM* vm, void* ptr, size_t len);
cyVmFree = lib.cyVmFree
cyVmFree.argtypes = [POINTER(CyUserVM), c_void_p, c_size_t]

# CyValue cyValueNone();
cyValueNone = lib.cyValueNone
cyValueNone.restype = CyValue
cyValueNone.argtypes = []

# CyValue cyValueTrue();
cyValueTrue = lib.cyValueTrue
cyValueTrue.restype = CyValue
cyValueTrue.argtypes = []

# CyValue cyValueFalse();
cyValueFalse = lib.cyValueFalse
cyValueFalse.restype = CyValue
cyValueFalse.argtypes = []

# CyValue cyValueNumber(double n);
cyValueNumber = lib.cyValueNumber
cyValueNumber.restype = CyValue
cyValueNumber.argtypes = [c_double]

# CyValue cyValueInteger(int n);
cyValueInteger = lib.cyValueInteger
cyValueInteger.restype = CyValue
cyValueInteger.argtypes = [c_int]

# CyValue cyValueGetOrAllocStringInfer(CyUserVM* vm, CStr str);
cyValueGetOrAllocStringInfer = lib.cyValueGetOrAllocStringInfer
cyValueGetOrAllocStringInfer.restype = CyValue
cyValueGetOrAllocStringInfer.argtypes = [POINTER(CyUserVM), CStr]

# CyValue cyValueGetOrAllocAstring(CyUserVM* vm, CStr str);
cyValueGetOrAllocAstring = lib.cyValueGetOrAllocAstring
cyValueGetOrAllocAstring.restype = CyValue
cyValueGetOrAllocAstring.argtypes = [POINTER(CyUserVM), CStr]

# CyValue cyValueGetOrAllocUstring(CyUserVM* vm, CStr str, uint32_t charLen);
cyValueGetOrAllocUstring = lib.cyValueGetOrAllocUstring
cyValueGetOrAllocUstring.restype = CyValue
cyValueGetOrAllocUstring.argtypes = [POINTER(CyUserVM), CStr, c_uint32]

# CyValue cyValueAllocList(CyUserVM* vm);
cyValueAllocList = lib.cyValueAllocList
cyValueAllocList.restype = CyValue
cyValueAllocList.argtypes = [POINTER(CyUserVM)]

# CyValue cyValueAllocMap(CyUserVM* vm);
cyValueAllocMap = lib.cyValueAllocMap
cyValueAllocMap.restype = CyValue
cyValueAllocMap.argtypes = [POINTER(CyUserVM)]

# CyValue cyValueAllocNativeFunc(CyUserVM* vm, CyFunc func, uint32_t numParams);
cyValueAllocNativeFunc = lib.cyValueAllocNativeFunc
cyValueAllocNativeFunc.restype = CyValue
cyValueAllocNativeFunc.argtypes = [POINTER(CyUserVM), CyFunc, c_uint32]

# CyValue cyValueAllocOpaquePtr(CyUserVM* vm, void* ptr);
cyValueAllocOpaquePtr = lib.cyValueAllocOpaquePtr
cyValueAllocOpaquePtr.restype = CyValue
cyValueAllocOpaquePtr.argtypes = [POINTER(CyUserVM), c_void_p]

# CyValue cyValueTagLiteral(CyUserVM* vm, CStr str);
cyValueTagLiteral = lib.cyValueTagLiteral
cyValueTagLiteral.restype = CyValue
cyValueTagLiteral.argtypes = [POINTER(CyUserVM), CStr]

# CyTypeId cyValueGetTypeId(CyValue val);
cyValueGetTypeId = lib.cyValueGetTypeId
cyValueGetTypeId.restype = CyTypeId
cyValueGetTypeId.argtypes = [CyValue]

# double cyValueAsNumber(CyValue val);
cyValueAsNumber = lib.cyValueAsNumber
cyValueAsNumber.restype = c_double
cyValueAsNumber.argtypes = [CyValue]

# bool cyValueToBool(CyValue val);
cyValueToBool = lib.cyValueToBool
cyValueToBool.restype = c_bool
cyValueToBool.argtypes = [CyValue]

# bool cyValueAsBool(CyValue val);
cyValueAsBool = lib.cyValueAsBool
cyValueAsBool.restype = c_bool
cyValueAsBool.argtypes = [CyValue]

# int cyValueAsInteger(CyValue val);
cyValueAsInteger = lib.cyValueAsInteger
cyValueAsInteger.restype = c_int
cyValueAsInteger.argtypes = [CyValue]

# uint32_t cyValueAsTagLiteralId(CyValue val);
cyValueAsTagLiteralId = lib.cyValueAsTagLiteralId
cyValueAsTagLiteralId.restype = c_uint32
cyValueAsTagLiteralId.argtypes = [CyValue]

# CStr cyValueToTempString(CyUserVM* vm, CyValue val);
cyValueToTempString = lib.cyValueToTempString
cyValueToTempString.restype = CStr
cyValueToTempString.argtypes = [POINTER(CyUserVM), CyValue]

# CStr cyValueToTempRawString(CyUserVM* vm, CyValue val);
cyValueToTempRawString = lib.cyValueToTempRawString
cyValueToTempRawString.restype = CStr
cyValueToTempRawString.argtypes = [POINTER(CyUserVM), CyValue]
