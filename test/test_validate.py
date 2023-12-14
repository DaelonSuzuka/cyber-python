from cyber import CyberVM, CsResultCode


# def test_validate_pass():
#     cyber = CyberVM()
#     cyber.validate('none')

#     assert cyber.last_result == CsResultCode.CS_SUCCESS

# def test_validate_token_error():
#     cyber = CyberVM()
#     cyber.validate('')

#     assert cyber.last_result == CsResultCode.CY_ErrorCompile

def test_validate_compile_error():
    cyber = CyberVM()
    cyber.validate('null')

    assert cyber.last_result == CsResultCode.CS_ERROR_COMPILE
