from cyber import CyberVM, CsResultCode


def test_list_conversion_numbers():
    cyber = CyberVM()
    result = cyber.eval('[1, 2, 3]')

    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert result == [1, 2, 3]


def test_list_conversion_strings():
    cyber = CyberVM()
    result = cyber.eval("['one', 'two', 'three']")

    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert result == ['one', 'two', 'three']
