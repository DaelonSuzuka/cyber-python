# GENERATED FILE DO NOT EDIT #
# ruff:  noqa: F401

from ctypes import (
    Structure,
    CFUNCTYPE,
    POINTER,
    c_void_p,
    c_char_p,
    c_bool,
    c_size_t,
    c_double,
    c_uint64,
    c_uint32,
    c_uint8,
    c_int64,
    c_int32,
    c_int,
)
from pathlib import Path
import sys
from enum import Enum
import platform


base_path = Path(__file__).parent / "lib"

if sys.platform == "win32":
    from ctypes import WinDLL

    path = base_path / "libcyber-windows-x64.dll"
    lib = WinDLL(path.as_posix())
elif sys.platform == "linux":
    from ctypes import CDLL

    path = base_path / "libcyber-linux-x64.so"
    lib = CDLL(path.as_posix())
elif sys.platform == "darwin":
    if platform.machine() == "arm64":
        from ctypes import CDLL

        path = base_path / "libcyber-macos-arm64.a"
        lib = CDLL(path.as_posix())
    else:
        from ctypes import CDLL

        path = base_path / "libcyber-macos-x64.dylib"
        lib = CDLL(path.as_posix())


# GENERATED FILE DO NOT EDIT #

class CsVM(Structure):
    ...

class CsValue(c_uint64):
    ...

class CsValueSlice(Structure):
    _fields_ = [('ptr', POINTER(CsValue)), ('len', c_size_t)]

class CsResolverResult(Structure):
    ...

class CsModuleLoaderResult(Structure):
    ...

class CsModule(Structure):
    ...

class CsResultCode(Enum):
    CS_SUCCESS = 0
    CS_ERROR_TOKEN = 1
    CS_ERROR_PARSE = 2
    CS_ERROR_COMPILE = 3
    CS_ERROR_PANIC = 4
    CS_ERROR_UNKNOWN = 5

class CsType(Enum):
    CS_TYPE_NONE = 0
    CS_TYPE_BOOLEAN = 1
    CS_TYPE_ERROR = 2
    CS_TYPE_PLACEHOLDER1 = 3
    CS_TYPE_PLACEHOLDER2 = 4
    CS_TYPE_PLACEHOLDER3 = 5
    CS_TYPE_SYMBOL = 6
    CS_TYPE_INTEGER = 7
    CS_TYPE_FLOAT = 8
    CS_TYPE_TUPLE = 9
    CS_TYPE_LIST = 10
    CS_TYPE_LISTITER = 11
    CS_TYPE_MAP = 12
    CS_TYPE_MAPITER = 13
    CS_TYPE_CLOSURE = 14
    CS_TYPE_LAMBDA = 15
    CS_TYPE_STRING = 16
    CS_TYPE_ARRAY = 17
    CS_TYPE_FIBER = 18
    CS_TYPE_BOX = 19
    CS_TYPE_HOSTFUNC = 20
    CS_TYPE_TCCSTATE = 21
    CS_TYPE_POINTER = 22
    CS_TYPE_METATYPE = 23

class CsTypeId(c_uint32):
    ...

class CsStr(Structure):
    _fields_ = [('buf', c_char_p), ('len', c_size_t)]

csGetFullVersion = lib.csGetFullVersion
"""CsStr csGetFullVersion();"""
csGetFullVersion.restype = CsStr
csGetFullVersion.argtypes = []

csGetVersion = lib.csGetVersion
"""CsStr csGetVersion();"""
csGetVersion.restype = CsStr
csGetVersion.argtypes = []

csGetBuild = lib.csGetBuild
"""CsStr csGetBuild();"""
csGetBuild.restype = CsStr
csGetBuild.argtypes = []

csGetCommit = lib.csGetCommit
"""CsStr csGetCommit();"""
csGetCommit.restype = CsStr
csGetCommit.argtypes = []

class CsModule(Structure):
    _fields_ = [('sym', c_void_p)]

CsFuncFn = CFUNCTYPE(CsValue, POINTER(CsVM), POINTER(CsValue), c_uint8)
"""typedef CsValue (*CsFuncFn)(CsVM* vm, const CsValue* args, uint8_t nargs);"""

CsInlineFuncFn = CFUNCTYPE(None, POINTER(CsVM), POINTER(c_uint8), POINTER(CsValue), c_uint8)
"""typedef void (*CsInlineFuncFn)(CsVM* vm, uint8_t* pc, const CsValue* args, uint8_t nargs);"""

CsResolverOnReceiptFn = CFUNCTYPE(None, POINTER(CsVM), POINTER(CsResolverResult))
"""typedef void (*CsResolverOnReceiptFn)(CsVM* vm, CsResolverResult* res);"""

class CsResolverResult(Structure):
    _fields_ = [('uri', c_char_p), ('uriLen', c_size_t), ('onReceipt', CsResolverOnReceiptFn)]

CsResolverFn = CFUNCTYPE(c_bool, POINTER(CsVM), c_uint32, CsStr, CsStr, POINTER(CsResolverResult))
"""typedef bool (*CsResolverFn)(CsVM* vm, uint32_t chunkId, CsStr curUri, CsStr spec, CsResolverResult* res);"""

CsModuleOnTypeLoadFn = CFUNCTYPE(None, POINTER(CsVM), CsModule)
"""typedef void (*CsModuleOnTypeLoadFn)(CsVM* vm, CsModule mod);"""

CsModuleOnLoadFn = CFUNCTYPE(None, POINTER(CsVM), CsModule)
"""typedef void (*CsModuleOnLoadFn)(CsVM* vm, CsModule mod);"""

CsModuleOnDestroyFn = CFUNCTYPE(None, POINTER(CsVM), CsModule)
"""typedef void (*CsModuleOnDestroyFn)(CsVM* vm, CsModule mod);"""

class CsFuncInfo(Structure):
    _fields_ = [('mod', CsModule), ('name', CsStr), ('funcSigId', c_uint32), ('idx', c_uint32)]

class CsFuncType(Enum):
    CS_FUNC_STANDARD = 0
    CS_FUNC_INLINE = 1

class CsFuncResult(Structure):
    _fields_ = [('ptr', c_void_p), ('type', c_uint8)]

CsFuncLoaderFn = CFUNCTYPE(c_bool, POINTER(CsVM), CsFuncInfo, POINTER(CsFuncResult))
"""typedef bool (*CsFuncLoaderFn)(CsVM* vm, CsFuncInfo funcInfo, CsFuncResult* out);"""

class CsVarInfo(Structure):
    _fields_ = [('mod', CsModule), ('name', CsStr), ('idx', c_uint32)]

CsVarLoaderFn = CFUNCTYPE(c_bool, POINTER(CsVM), CsVarInfo, POINTER(CsValue))
"""typedef bool (*CsVarLoaderFn)(CsVM* vm, CsVarInfo funcInfo, CsValue* out);"""

class CsTypeInfo(Structure):
    _fields_ = [('mod', CsModule), ('name', CsStr), ('idx', c_uint32)]

class CsTypeType(Enum):
    CS_TYPE_OBJECT = 0
    CS_TYPE_CORE_OBJECT = 1

CsObjectGetChildrenFn = CFUNCTYPE(CsValueSlice, POINTER(CsVM), c_void_p)
"""typedef CsValueSlice (*CsObjectGetChildrenFn)(CsVM* vm, void* obj);"""

CsObjectFinalizerFn = CFUNCTYPE(None, POINTER(CsVM), c_void_p)
"""typedef void (*CsObjectFinalizerFn)(CsVM* vm, void* obj);"""

class CsTypeResult(Structure):
    ...

CsTypeLoaderFn = CFUNCTYPE(c_bool, POINTER(CsVM), CsTypeInfo, POINTER(CsTypeResult))
"""typedef bool (*CsTypeLoaderFn)(CsVM* vm, CsTypeInfo typeInfo, CsTypeResult* out);"""

CsModuleOnReceiptFn = CFUNCTYPE(None, POINTER(CsVM), POINTER(CsModuleLoaderResult))
"""typedef void (*CsModuleOnReceiptFn)(CsVM* vm, CsModuleLoaderResult* res);"""

class CsModuleLoaderResult(Structure):
    _fields_ = [('src', c_char_p), ('srcLen', c_size_t)]

CsModuleLoaderFn = CFUNCTYPE(c_bool, POINTER(CsVM), CsStr, POINTER(CsModuleLoaderResult))
"""typedef bool (*CsModuleLoaderFn)(CsVM* vm, CsStr resolvedSpec, CsModuleLoaderResult* out);"""

CsPrintFn = CFUNCTYPE(None, POINTER(CsVM), CsStr)
"""typedef void (*CsPrintFn)(CsVM* vm, CsStr str);"""

csCreate = lib.csCreate
"""CsVM* csCreate();"""
csCreate.restype = POINTER(CsVM)
csCreate.argtypes = []

csDeinit = lib.csDeinit
"""void csDeinit(CsVM* vm);"""
csDeinit.argtypes = [POINTER(CsVM)]

csDestroy = lib.csDestroy
"""void csDestroy(CsVM* vm);"""
csDestroy.argtypes = [POINTER(CsVM)]

csGetResolver = lib.csGetResolver
"""CsResolverFn csGetResolver(CsVM* vm);"""
csGetResolver.restype = CsResolverFn
csGetResolver.argtypes = [POINTER(CsVM)]

csSetResolver = lib.csSetResolver
"""void csSetResolver(CsVM* vm, CsResolverFn resolver);"""
csSetResolver.argtypes = [POINTER(CsVM), CsResolverFn]

# csDefaultResolver = lib.csDefaultResolver
"""bool csDefaultResolver(CsVM* vm, uint32_t chunkId, CsStr curUri, CsStr spec, CsStr* outUri);"""
# csDefaultResolver.restype = c_bool
# csDefaultResolver.argtypes = [POINTER(CsVM), c_uint32, CsStr, CsStr, POINTER(CsStr)]

csGetModuleLoader = lib.csGetModuleLoader
"""CsModuleLoaderFn csGetModuleLoader(CsVM* vm);"""
csGetModuleLoader.restype = CsModuleLoaderFn
csGetModuleLoader.argtypes = [POINTER(CsVM)]

csSetModuleLoader = lib.csSetModuleLoader
"""void csSetModuleLoader(CsVM* vm, CsModuleLoaderFn loader);"""
csSetModuleLoader.argtypes = [POINTER(CsVM), CsModuleLoaderFn]

csDefaultModuleLoader = lib.csDefaultModuleLoader
"""bool csDefaultModuleLoader(CsVM* vm, CsStr resolvedSpec, CsModuleLoaderResult* out);"""
csDefaultModuleLoader.restype = c_bool
csDefaultModuleLoader.argtypes = [POINTER(CsVM), CsStr, POINTER(CsModuleLoaderResult)]

csGetPrint = lib.csGetPrint
"""CsPrintFn csGetPrint(CsVM* vm);"""
csGetPrint.restype = CsPrintFn
csGetPrint.argtypes = [POINTER(CsVM)]

csSetPrint = lib.csSetPrint
"""void csSetPrint(CsVM* vm, CsPrintFn print);"""
csSetPrint.argtypes = [POINTER(CsVM), CsPrintFn]

csEval = lib.csEval
"""CsResultCode csEval(CsVM* vm, CsStr src, CsValue* outVal);"""
csEval.restype = c_int
csEval.argtypes = [POINTER(CsVM), CsStr, POINTER(CsValue)]

csValidate = lib.csValidate
"""CsResultCode csValidate(CsVM* vm, CsStr src);"""
csValidate.restype = c_int
csValidate.argtypes = [POINTER(CsVM), CsStr]

csNewLastErrorReport = lib.csNewLastErrorReport
"""const char* csNewLastErrorReport(CsVM* vm);"""
csNewLastErrorReport.restype = c_char_p
csNewLastErrorReport.argtypes = [POINTER(CsVM)]

csGetUserData = lib.csGetUserData
"""void* csGetUserData(CsVM* vm);"""
csGetUserData.restype = c_void_p
csGetUserData.argtypes = [POINTER(CsVM)]

csSetUserData = lib.csSetUserData
"""void csSetUserData(CsVM* vm, void* userData);"""
csSetUserData.argtypes = [POINTER(CsVM), c_void_p]

# csVerbose = lib.csVerbose
"""extern bool csVerbose;"""

csDeclareUntypedFunc = lib.csDeclareUntypedFunc
"""void csDeclareUntypedFunc(CsModule mod, const char* name, uint32_t numParams, CsFuncFn fn);"""
csDeclareUntypedFunc.argtypes = [CsModule, c_char_p, c_uint32, CsFuncFn]

csDeclareFunc = lib.csDeclareFunc
"""void csDeclareFunc(CsModule mod, const char* name, const CsTypeId* params, uint32_t numParams, CsTypeId retType, CsFuncFn fn);"""
csDeclareFunc.argtypes = [CsModule, c_char_p, POINTER(CsTypeId), c_uint32, CsTypeId, CsFuncFn]

csDeclareVar = lib.csDeclareVar
"""void csDeclareVar(CsModule mod, const char* name, CsValue val);"""
csDeclareVar.argtypes = [CsModule, c_char_p, CsValue]

csRelease = lib.csRelease
"""void csRelease(CsVM* vm, CsValue val);"""
csRelease.argtypes = [POINTER(CsVM), CsValue]

csRetain = lib.csRetain
"""void csRetain(CsVM* vm, CsValue val);"""
csRetain.argtypes = [POINTER(CsVM), CsValue]

class CsGCResult(Structure):
    _fields_ = [('numCycFreed', c_uint32), ('numObjFreed', c_uint32)]

csPerformGC = lib.csPerformGC
"""CsGCResult csPerformGC(CsVM* vm);"""
csPerformGC.restype = CsGCResult
csPerformGC.argtypes = [POINTER(CsVM)]

csGetGlobalRC = lib.csGetGlobalRC
"""size_t csGetGlobalRC(CsVM* vm);"""
csGetGlobalRC.restype = c_size_t
csGetGlobalRC.argtypes = [POINTER(CsVM)]

csCountObjects = lib.csCountObjects
"""size_t csCountObjects(CsVM* vm);"""
csCountObjects.restype = c_size_t
csCountObjects.argtypes = [POINTER(CsVM)]

csAlloc = lib.csAlloc
"""void* csAlloc(CsVM* vm, size_t size);"""
csAlloc.restype = c_void_p
csAlloc.argtypes = [POINTER(CsVM), c_size_t]

csFree = lib.csFree
"""void csFree(CsVM* vm, void* ptr, size_t len);"""
csFree.argtypes = [POINTER(CsVM), c_void_p, c_size_t]

csFreeStr = lib.csFreeStr
"""void csFreeStr(CsVM* vm, CsStr str);"""
csFreeStr.argtypes = [POINTER(CsVM), CsStr]

csFreeStrZ = lib.csFreeStrZ
"""void csFreeStrZ(CsVM* vm, const char* str);"""
csFreeStrZ.argtypes = [POINTER(CsVM), c_char_p]

csNone = lib.csNone
"""CsValue csNone();"""
csNone.restype = CsValue
csNone.argtypes = []

csTrue = lib.csTrue
"""CsValue csTrue();"""
csTrue.restype = CsValue
csTrue.argtypes = []

csFalse = lib.csFalse
"""CsValue csFalse();"""
csFalse.restype = CsValue
csFalse.argtypes = []

csBool = lib.csBool
"""CsValue csBool(bool b);"""
csBool.restype = CsValue
csBool.argtypes = [c_bool]

csInteger = lib.csInteger
"""CsValue csInteger(int64_t n);"""
csInteger.restype = CsValue
csInteger.argtypes = [c_int64]

csInteger32 = lib.csInteger32
"""CsValue csInteger32(int32_t n);"""
csInteger32.restype = CsValue
csInteger32.argtypes = [c_int32]

csFloat = lib.csFloat
"""CsValue csFloat(double f);"""
csFloat.restype = CsValue
csFloat.argtypes = [c_double]

csHostObject = lib.csHostObject
"""CsValue csHostObject(void* ptr);"""
csHostObject.restype = CsValue
csHostObject.argtypes = [c_void_p]

csVmObject = lib.csVmObject
"""CsValue csVmObject(void* ptr);"""
csVmObject.restype = CsValue
csVmObject.argtypes = [c_void_p]

csSymbol = lib.csSymbol
"""CsValue csSymbol(CsVM* vm, CsStr str);"""
csSymbol.restype = CsValue
csSymbol.argtypes = [POINTER(CsVM), CsStr]

csNewString = lib.csNewString
"""CsValue csNewString(CsVM* vm, CsStr str);"""
csNewString.restype = CsValue
csNewString.argtypes = [POINTER(CsVM), CsStr]

csNewAstring = lib.csNewAstring
"""CsValue csNewAstring(CsVM* vm, CsStr str);"""
csNewAstring.restype = CsValue
csNewAstring.argtypes = [POINTER(CsVM), CsStr]

csNewUstring = lib.csNewUstring
"""CsValue csNewUstring(CsVM* vm, CsStr str, uint32_t charLen);"""
csNewUstring.restype = CsValue
csNewUstring.argtypes = [POINTER(CsVM), CsStr, c_uint32]

csNewTuple = lib.csNewTuple
"""CsValue csNewTuple(CsVM* vm, const CsValue* vals, size_t len);"""
csNewTuple.restype = CsValue
csNewTuple.argtypes = [POINTER(CsVM), POINTER(CsValue), c_size_t]

csNewEmptyList = lib.csNewEmptyList
"""CsValue csNewEmptyList(CsVM* vm);"""
csNewEmptyList.restype = CsValue
csNewEmptyList.argtypes = [POINTER(CsVM)]

csNewList = lib.csNewList
"""CsValue csNewList(CsVM* vm, const CsValue* vals, size_t len);"""
csNewList.restype = CsValue
csNewList.argtypes = [POINTER(CsVM), POINTER(CsValue), c_size_t]

csNewEmptyMap = lib.csNewEmptyMap
"""CsValue csNewEmptyMap(CsVM* vm);"""
csNewEmptyMap.restype = CsValue
csNewEmptyMap.argtypes = [POINTER(CsVM)]

csNewUntypedFunc = lib.csNewUntypedFunc
"""CsValue csNewUntypedFunc(CsVM* vm, uint32_t numParams, CsFuncFn func);"""
csNewUntypedFunc.restype = CsValue
csNewUntypedFunc.argtypes = [POINTER(CsVM), c_uint32, CsFuncFn]

csNewFunc = lib.csNewFunc
"""CsValue csNewFunc(CsVM* vm, const CsTypeId* params, uint32_t numParams, CsTypeId retType, CsFuncFn func);"""
csNewFunc.restype = CsValue
csNewFunc.argtypes = [POINTER(CsVM), POINTER(CsTypeId), c_uint32, CsTypeId, CsFuncFn]

csNewPointer = lib.csNewPointer
"""CsValue csNewPointer(CsVM* vm, void* ptr);"""
csNewPointer.restype = CsValue
csNewPointer.argtypes = [POINTER(CsVM), c_void_p]

csNewHostObject = lib.csNewHostObject
"""CsValue csNewHostObject(CsVM* vm, CsTypeId typeId, size_t n);"""
csNewHostObject.restype = CsValue
csNewHostObject.argtypes = [POINTER(CsVM), CsTypeId, c_size_t]

csNewHostObjectPtr = lib.csNewHostObjectPtr
"""void* csNewHostObjectPtr(CsVM* vm, CsTypeId typeId, size_t n);"""
csNewHostObjectPtr.restype = c_void_p
csNewHostObjectPtr.argtypes = [POINTER(CsVM), CsTypeId, c_size_t]

csNewVmObject = lib.csNewVmObject
"""CsValue csNewVmObject(CsVM* vm, CsTypeId typeId);"""
csNewVmObject.restype = CsValue
csNewVmObject.argtypes = [POINTER(CsVM), CsTypeId]

csGetTypeId = lib.csGetTypeId
"""CsTypeId csGetTypeId(CsValue val);"""
csGetTypeId.restype = CsTypeId
csGetTypeId.argtypes = [CsValue]

csAsFloat = lib.csAsFloat
"""double csAsFloat(CsValue val);"""
csAsFloat.restype = c_double
csAsFloat.argtypes = [CsValue]

csToBool = lib.csToBool
"""bool csToBool(CsValue val);"""
csToBool.restype = c_bool
csToBool.argtypes = [CsValue]

csAsBool = lib.csAsBool
"""bool csAsBool(CsValue val);"""
csAsBool.restype = c_bool
csAsBool.argtypes = [CsValue]

csAsInteger = lib.csAsInteger
"""int64_t csAsInteger(CsValue val);"""
csAsInteger.restype = c_int64
csAsInteger.argtypes = [CsValue]

csAsSymbolId = lib.csAsSymbolId
"""uint32_t csAsSymbolId(CsValue val);"""
csAsSymbolId.restype = c_uint32
csAsSymbolId.argtypes = [CsValue]

csToTempString = lib.csToTempString
"""CsStr csToTempString(CsVM* vm, CsValue val);"""
csToTempString.restype = CsStr
csToTempString.argtypes = [POINTER(CsVM), CsValue]

# csToTempRawString = lib.csToTempRawString
"""CsStr csToTempRawString(CsVM* vm, CsValue val);"""
# csToTempRawString.restype = CsStr
# csToTempRawString.argtypes = [POINTER(CsVM), CsValue]

csAsHostObject = lib.csAsHostObject
"""void* csAsHostObject(CsValue val);"""
csAsHostObject.restype = c_void_p
csAsHostObject.argtypes = [CsValue]

csListLen = lib.csListLen
"""size_t csListLen(CsValue list);"""
csListLen.restype = c_size_t
csListLen.argtypes = [CsValue]

csListCap = lib.csListCap
"""size_t csListCap(CsValue list);"""
csListCap.restype = c_size_t
csListCap.argtypes = [CsValue]

csListGet = lib.csListGet
"""CsValue csListGet(CsVM* vm, CsValue list, size_t idx);"""
csListGet.restype = CsValue
csListGet.argtypes = [POINTER(CsVM), CsValue, c_size_t]

csListSet = lib.csListSet
"""void csListSet(CsVM* vm, CsValue list, size_t idx, CsValue val);"""
csListSet.argtypes = [POINTER(CsVM), CsValue, c_size_t, CsValue]

csListAppend = lib.csListAppend
"""void csListAppend(CsVM* vm, CsValue list, CsValue val);"""
csListAppend.argtypes = [POINTER(CsVM), CsValue, CsValue]

csListInsert = lib.csListInsert
"""void csListInsert(CsVM* vm, CsValue list, size_t idx, CsValue val);"""
csListInsert.argtypes = [POINTER(CsVM), CsValue, c_size_t, CsValue]
