# from cyber import CyberVM, CsResultCode, CyberTokenError
# import pytest


# def get_printing_vm():
#     cyber = CyberVM()
    
#     cyber.set_print(print)

#     return cyber


# def test_string_eval(capsys):
#     cyber = get_printing_vm()

#     cyber.eval("print 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'


# def test_bytes_eval(capsys):
#     cyber = get_printing_vm()

#     cyber.eval(b"print 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'


# def test_multiple_eval(capsys):
#     cyber = get_printing_vm()

#     cyber.eval(b"print 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'

#     cyber.eval(b"print 'hello again'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello again\n'


# def test_multiple_eval_after_failure(capsys):
#     cyber = get_printing_vm()

#     with pytest.raises(CyberTokenError):
#         cyber.eval(b"print 'unterminated string")

#     assert cyber.last_result == CsResultCode.CS_ERROR_TOKEN
#     captured = capsys.readouterr() # clear stdout

#     cyber.eval(b"print 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'