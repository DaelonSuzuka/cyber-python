from cyber import CyberVM, CyResultCode


def test_list_conversion_numbers():
    cyber = CyberVM()
    result = cyber.eval('[1, 2, 3]')

    assert cyber.last_result == CyResultCode.CY_Success
    assert result == [1, 2, 3]


def test_list_conversion_strings():
    cyber = CyberVM()
    result = cyber.eval("['one', 'two', 'three']")

    assert cyber.last_result == CyResultCode.CY_Success
    assert result == ['one', 'two', 'three']
