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
