from cyber import CyberVM, CyResultCode, CyType


# def test_validate_pass():
#     cyber = CyberVM()
#     cyber.validate('none')

#     assert cyber.last_result == CyResultCode.CY_Success

# def test_validate_token_error():
#     cyber = CyberVM()
#     cyber.validate('')

#     assert cyber.last_result == CyResultCode.CY_ErrorCompile

def test_validate_compile_error():
    cyber = CyberVM()
    cyber.validate('null')

    assert cyber.last_result == CyResultCode.CY_ErrorCompile
