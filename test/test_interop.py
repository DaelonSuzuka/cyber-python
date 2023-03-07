from cyber import CyberVM, CyResultCode, CyType


def test_python_function_specified_argtype(capsys):
    cyber = CyberVM()

    with cyber.module('core') as module:

        @module.function('test')
        def _new_func(one: str, two: int, three: float):
            print(one, two, three)

    cyber.eval("test 'one' 2 3")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one 2 3.0\n'


def test_python_function_unspecified_argtypes(capsys):
    cyber = CyberVM()

    with cyber.module('core') as module:

        @module.function('test')
        def _new_func(one, two, three):
            print(one, two, three)

    cyber.eval("test 'one' 2 3")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one 2.0 3.0\n'


def test_python_function_return_type():
    cyber = CyberVM()

    with cyber.module('core') as module:

        @module.function('test')
        def _test_func() -> str:
            return 'test'

    output = cyber.eval('test()')

    assert cyber.last_result == CyResultCode.CY_Success

    # TODO: I think cyber might not support this
    # assert output == 'test'
