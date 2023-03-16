from cyber import CyberVM, CyResultCode, CyType, CyberTokenError
import pytest


def get_printing_vm():
    cyber = CyberVM()

    # have to override print so we can capture its output
    @cyber.function('core.print')
    def _print(string: str):
        print(string)

    return cyber


def test_string_eval(capsys):
    cyber = get_printing_vm()

    cyber.eval("print 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'


def test_bytes_eval(capsys):
    cyber = get_printing_vm()

    cyber.eval(b"print 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'


def test_multiple_eval(capsys):
    cyber = get_printing_vm()

    cyber.eval(b"print 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'

    cyber.eval(b"print 'hello again'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello again\n'


def test_multiple_eval_after_failure(capsys):
    cyber = get_printing_vm()

    with pytest.raises(CyberTokenError):
        cyber.eval(b"print 'unterminated string")

    assert cyber.last_result == CyResultCode.CY_ErrorToken
    captured = capsys.readouterr() # clear stdout

    cyber.eval(b"print 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'