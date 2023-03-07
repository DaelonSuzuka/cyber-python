from cyber import CyberVM, CyResultCode, CyType


def get_printing_vm():
    cyber = CyberVM()

    # have to override print so we can capture its output
    with cyber.module('core') as module:

        @module.function('print')
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
