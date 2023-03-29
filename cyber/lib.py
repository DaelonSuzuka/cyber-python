# GENERATED FILE DO NOT EDIT #

from ctypes import (
    Structure,
    CFUNCTYPE,
    POINTER,
    c_void_p,
    c_char_p,
    c_bool,
    c_size_t,
    c_int,
    c_double,
    c_uint64,
    c_uint32,
    c_uint8,
)
from pathlib import Path
import sys
from enum import Enum
import platform


base_path = Path(__file__).parent / 'lib'

if sys.platform == 'win32':
    from ctypes import WinDLL
    path = base_path / 'cyber.dll'
    lib = WinDLL(path.as_posix())
elif sys.platform == 'linux':
    from ctypes import CDLL
    path = base_path / 'libcyber.so'
    lib = CDLL(path.as_posix())
elif sys.platform == 'darwin':
    if platform.machine() == 'arm64':
        from ctypes import CDLL
        path = base_path / 'libcyber-arm64.dylib'
        lib = CDLL(path.as_posix())
    else:
        from ctypes import CDLL
        path = base_path / 'libcyber.dylib'
        lib = CDLL(path.as_posix())


# GENERATED FILE DO NOT EDIT #

class CyVM(Structure):
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
    CY_TypeEnum = 5
    CY_TypeSymbol = 6
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
    CY_TypePointer = 24
    CY_TypeFile = 25
    CY_TypeDir = 26
    CY_TypeDirIter = 27
    CY_TypeType = 28

class CStr(Structure):
    _fields_ = [('charz', c_char_p), ('len', c_size_t)]

class CyTypeId(c_uint32):
    ...

# typedef CyValue (*CyFunc)(CyVM* vm, CyValue* args, uint8_t nargs);
CyFunc = CFUNCTYPE(CyValue, POINTER(CyVM), POINTER(CyValue), c_uint8)

# typedef bool (*CyLoadModuleFunc)(CyVM* vm, CyModule* mod);
CyLoadModuleFunc = CFUNCTYPE(c_bool, POINTER(CyVM), POINTER(CyModule))

# CStr cyGetFullVersion();
cyGetFullVersion = lib.cyGetFullVersion
cyGetFullVersion.restype = CStr
cyGetFullVersion.argtypes = []

# CStr cyGetVersion();
cyGetVersion = lib.cyGetVersion
cyGetVersion.restype = CStr
cyGetVersion.argtypes = []

# CStr cyGetBuild();
cyGetBuild = lib.cyGetBuild
cyGetBuild.restype = CStr
cyGetBuild.argtypes = []

# CStr cyGetCommit();
cyGetCommit = lib.cyGetCommit
cyGetCommit.restype = CStr
cyGetCommit.argtypes = []

# CyVM* cyVmCreate();
cyVmCreate = lib.cyVmCreate
cyVmCreate.restype = POINTER(CyVM)
cyVmCreate.argtypes = []

# void cyVmDestroy(CyVM* vm);
cyVmDestroy = lib.cyVmDestroy
cyVmDestroy.argtypes = [POINTER(CyVM)]

# CyResultCode cyVmEval(CyVM* vm, CStr src, CyValue* outVal);
cyVmEval = lib.cyVmEval
cyVmEval.restype = c_int
cyVmEval.argtypes = [POINTER(CyVM), CStr, POINTER(CyValue)]

# CyResultCode cyVmValidate(CyVM* vm, CStr src);
cyVmValidate = lib.cyVmValidate
cyVmValidate.restype = c_int
cyVmValidate.argtypes = [POINTER(CyVM), CStr]

# CStr cyVmGetLastErrorReport(CyVM* vm);
cyVmGetLastErrorReport = lib.cyVmGetLastErrorReport
cyVmGetLastErrorReport.restype = CStr
cyVmGetLastErrorReport.argtypes = [POINTER(CyVM)]

# void cyVmRelease(CyVM* vm, CyValue val);
cyVmRelease = lib.cyVmRelease
cyVmRelease.argtypes = [POINTER(CyVM), CyValue]

# void cyVmRetain(CyVM* vm, CyValue val);
cyVmRetain = lib.cyVmRetain
cyVmRetain.argtypes = [POINTER(CyVM), CyValue]

# void* cyVmGetUserData(CyVM* vm);
cyVmGetUserData = lib.cyVmGetUserData
cyVmGetUserData.restype = c_void_p
cyVmGetUserData.argtypes = [POINTER(CyVM)]

# void cyVmSetUserData(CyVM* vm, void* userData);
cyVmSetUserData = lib.cyVmSetUserData
cyVmSetUserData.argtypes = [POINTER(CyVM), c_void_p]

# void cyVmAddModuleLoader(CyVM* vm, CStr name, CyLoadModuleFunc func);
cyVmAddModuleLoader = lib.cyVmAddModuleLoader
cyVmAddModuleLoader.argtypes = [POINTER(CyVM), CStr, CyLoadModuleFunc]

# void cyVmSetModuleFunc(CyVM* vm, CyModule* mod, CStr name, uint32_t numParams, CyFunc func);
cyVmSetModuleFunc = lib.cyVmSetModuleFunc
cyVmSetModuleFunc.argtypes = [POINTER(CyVM), POINTER(CyModule), CStr, c_uint32, CyFunc]

# void cyVmSetModuleVar(CyVM* vm, CyModule* mod, CStr name, CyValue val);
cyVmSetModuleVar = lib.cyVmSetModuleVar
cyVmSetModuleVar.argtypes = [POINTER(CyVM), POINTER(CyModule), CStr, CyValue]

# void* cyVmAlloc(CyVM* vm, size_t size);
cyVmAlloc = lib.cyVmAlloc
cyVmAlloc.restype = c_void_p
cyVmAlloc.argtypes = [POINTER(CyVM), c_size_t]

# void cyVmFree(CyVM* vm, void* ptr, size_t len);
cyVmFree = lib.cyVmFree
cyVmFree.argtypes = [POINTER(CyVM), c_void_p, c_size_t]

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

# CyValue cyValueGetOrAllocStringInfer(CyVM* vm, CStr str);
cyValueGetOrAllocStringInfer = lib.cyValueGetOrAllocStringInfer
cyValueGetOrAllocStringInfer.restype = CyValue
cyValueGetOrAllocStringInfer.argtypes = [POINTER(CyVM), CStr]

# CyValue cyValueGetOrAllocAstring(CyVM* vm, CStr str);
cyValueGetOrAllocAstring = lib.cyValueGetOrAllocAstring
cyValueGetOrAllocAstring.restype = CyValue
cyValueGetOrAllocAstring.argtypes = [POINTER(CyVM), CStr]

# CyValue cyValueGetOrAllocUstring(CyVM* vm, CStr str, uint32_t charLen);
cyValueGetOrAllocUstring = lib.cyValueGetOrAllocUstring
cyValueGetOrAllocUstring.restype = CyValue
cyValueGetOrAllocUstring.argtypes = [POINTER(CyVM), CStr, c_uint32]

# CyValue cyValueAllocList(CyVM* vm);
cyValueAllocList = lib.cyValueAllocList
cyValueAllocList.restype = CyValue
cyValueAllocList.argtypes = [POINTER(CyVM)]

# CyValue cyValueAllocMap(CyVM* vm);
cyValueAllocMap = lib.cyValueAllocMap
cyValueAllocMap.restype = CyValue
cyValueAllocMap.argtypes = [POINTER(CyVM)]

# CyValue cyValueAllocNativeFunc(CyVM* vm, CyFunc func, uint32_t numParams);
cyValueAllocNativeFunc = lib.cyValueAllocNativeFunc
cyValueAllocNativeFunc.restype = CyValue
cyValueAllocNativeFunc.argtypes = [POINTER(CyVM), CyFunc, c_uint32]

# CyValue cyValueAllocPointer(CyVM* vm, void* ptr);
cyValueAllocPointer = lib.cyValueAllocPointer
cyValueAllocPointer.restype = CyValue
cyValueAllocPointer.argtypes = [POINTER(CyVM), c_void_p]

# CyValue cyValueTagLiteral(CyVM* vm, CStr str);
cyValueTagLiteral = lib.cyValueTagLiteral
cyValueTagLiteral.restype = CyValue
cyValueTagLiteral.argtypes = [POINTER(CyVM), CStr]

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

# CStr cyValueToTempString(CyVM* vm, CyValue val);
cyValueToTempString = lib.cyValueToTempString
cyValueToTempString.restype = CStr
cyValueToTempString.argtypes = [POINTER(CyVM), CyValue]

# CStr cyValueToTempRawString(CyVM* vm, CyValue val);
cyValueToTempRawString = lib.cyValueToTempRawString
cyValueToTempRawString.restype = CStr
cyValueToTempRawString.argtypes = [POINTER(CyVM), CyValue]

# size_t cyListLen(CyValue list);
cyListLen = lib.cyListLen
cyListLen.restype = c_size_t
cyListLen.argtypes = [CyValue]

# size_t cyListCap(CyValue list);
cyListCap = lib.cyListCap
cyListCap.restype = c_size_t
cyListCap.argtypes = [CyValue]

# CyValue cyListGet(CyVM* vm, CyValue list, size_t idx);
cyListGet = lib.cyListGet
cyListGet.restype = CyValue
cyListGet.argtypes = [POINTER(CyVM), CyValue, c_size_t]

# void cyListSet(CyVM* vm, CyValue list, size_t idx, CyValue val);
cyListSet = lib.cyListSet
cyListSet.argtypes = [POINTER(CyVM), CyValue, c_size_t, CyValue]

# void cyListAppend(CyVM* vm, CyValue list, CyValue val);
cyListAppend = lib.cyListAppend
cyListAppend.argtypes = [POINTER(CyVM), CyValue, CyValue]

# void cyListInsert(CyVM* vm, CyValue list, size_t idx, CyValue val);
cyListInsert = lib.cyListInsert
cyListInsert.argtypes = [POINTER(CyVM), CyValue, c_size_t, CyValue]

