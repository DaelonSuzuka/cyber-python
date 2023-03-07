from cyber import CyberVM, CyResultCode, CyType


def test_eval_none():
    cyber = CyberVM()

    output = cyber.eval('none')

    assert output == None
    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeNone


def test_eval_bool():
    cyber = CyberVM()

    output = cyber.eval('true')

    assert output == True
    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeBoolean

    output = cyber.eval('false')

    assert output == False
    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeBoolean


def test_eval_int():
    cyber = CyberVM()


# TODO: parameterize me
def test_eval_number():
    cyber = CyberVM()

    output = cyber.eval('1')

    assert output == 1
    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeNumber

    output = cyber.eval('1.5')

    assert output == 1.5
    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeNumber


def test_eval_static_a_string():
    cyber = CyberVM()

    output = cyber.eval("'string'")

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeStaticAstring
    assert output == 'string'


def test_eval_static_u_string():
    cyber = CyberVM()

    output = cyber.eval("'💕'")

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeStaticUstring
    assert output == '💕'


def test_eval_a_string():
    cyber = CyberVM()
    script = """
    t = 'string'
    s = '{t} interpolation'
    s
    """
    output = cyber.eval(script)

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeAstring
    assert output == 'string interpolation'


def test_eval_u_string():
    cyber = CyberVM()
    script = """
    t = '💕'
    s = '{t} interpolation'
    s
    """
    output = cyber.eval(script)

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeUstring
    assert output == '💕 interpolation'


def test_eval_string_slice():
    cyber = CyberVM()

    script = """
    t = 'string'
    s = '{t}'
    s[..3]
    """
    output = cyber.eval(script)

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeStringSlice
    assert output == 'str'


def test_eval_rawstring():
    cyber = CyberVM()

    output = cyber.eval("rawstring('rawstring')")

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeRawString
    assert output == b'rawstring'


def test_eval_rawstring_slice():
    cyber = CyberVM()

    script = """
    t = rawstring('rawstring')
    t[3..]
    """
    output = cyber.eval(script)

    assert cyber.last_result == CyResultCode.CY_Success
    assert cyber.last_output_type == CyType.CY_TypeRawStringSlice
    assert output == b'string'
