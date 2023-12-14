from cyber import CyberVM, CsResultCode, CsType, CsValue


def test_eval_none():
    cyber = CyberVM()

    output = cyber.eval('none')

    assert output is None
    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_NONE


def test_eval_bool():
    cyber = CyberVM()

    output = cyber.eval('true')

    assert output is True
    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_BOOLEAN

    output = cyber.eval('false')

    assert output is False
    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_BOOLEAN


def test_eval_int():
    cyber = CyberVM()


# TODO: parameterize me
def test_eval_number():
    cyber = CyberVM()

    output = cyber.eval('1')

    assert output == 1
    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_INTEGER

    output = cyber.eval('1.5')

    assert output == 1.5
    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_FLOAT


def test_eval_cyvalue():
    cyber = CyberVM()

    script = """
        func foo(a):
            pass
            
        foo
    """
    output = cyber.eval(script)

    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_LAMBDA
    assert type(output) == CsValue


def test_eval_string():
    cyber = CyberVM()

    output = cyber.eval("'string'")

    assert cyber.last_result == CsResultCode.CS_SUCCESS
    assert cyber.last_output_type == CsType.CS_TYPE_STRING
    assert output == 'string'
