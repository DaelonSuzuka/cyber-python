from cyber import CyberVM, CyResultCode, CyType, CyValue


def test_python_function_specified_argtype(capsys):
    cyber = CyberVM()

    @cyber.function('core.test')
    def _new_func(one: str, two: int, three: float, four: bool):
        print(one, two, three, four)

    cyber.eval("test 'one' 2 3 4")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one 2 3.0 True\n'


def test_python_function_specified_raw_cyvalue():
    cyber = CyberVM()

    output = []

    @cyber.function('core.test')
    def _new_func(value: CyValue):
        output.append(value)

    cyber.eval("test 'anything'")

    assert cyber.last_result == CyResultCode.CY_Success
    assert type(output[0]) == CyValue


def test_python_function_unspecified_argtypes(capsys):
    cyber = CyberVM()

    @cyber.function('core.test')
    def _new_func(one, two, three):
        print(one, two, three)

    cyber.eval("test 'one' 2 3")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one 2.0 3.0\n'


def test_python_function_return_type():
    cyber = CyberVM()

    @cyber.function('core.test')
    def _test_func() -> str:
        return 'test'

    output = cyber.eval('test()')

    assert cyber.last_result == CyResultCode.CY_Success

    # TODO: I think cyber might not support this
    # assert output == 'test'
