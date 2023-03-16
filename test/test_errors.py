from cyber import (
    CyberVM,
    CyResultCode,
    CyType,
    CyberTokenError,
    CyberParseError,
    CyberCompileError,
    CyberPanicError,
    CyberUnknownError,
)
import pytest


def test_token_error():
    cyber = CyberVM()

    with pytest.raises(CyberTokenError):
        cyber.exec("print 'unterminated string")

    assert cyber.last_result == CyResultCode.CY_ErrorToken


def test_parse_error():
    cyber = CyberVM()

    script = """
        var
        var a: 123
        var b: 234    
    """

    with pytest.raises(CyberParseError):
        cyber.exec(script)

    assert cyber.last_result == CyResultCode.CY_ErrorParse


def test_compile_error():
    cyber = CyberVM()

    script = """
        func foo(a Vec2):
            pass
    """
    with pytest.raises(CyberCompileError):
        cyber.exec(script)

    assert cyber.last_result == CyResultCode.CY_ErrorCompile


def test_panic_error():
    cyber = CyberVM()

    with pytest.raises(CyberPanicError):
        cyber.exec('panic(#danger)')

    assert cyber.last_result == CyResultCode.CY_ErrorPanic


# TODO: how do I trigger this?
# def test_unknown_error():
#     cyber = CyberVM()
#     script = """

#     """
#     with pytest.raises(CyberUnknownError):
#         cyber.exec(script)

#     assert cyber.last_result == CyResultCode.CY_ErrorUnknown
