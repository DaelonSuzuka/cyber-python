from cyber import CyberVM, CyResultCode, CyType


# def test_override_function():
#     assert False


# def test_add_function():
#     assert False


# def test_add_module():
#     assert False


def test_context_override_function(capsys):
    cyber = CyberVM()

    @cyber.function('print')
    def _print(string: str):
        print('<python>', string)

    cyber.eval("print 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == '<python> hello\n'


def test_context_add_function(capsys):
    cyber = CyberVM()

    @cyber.function('new_func')
    def _new_func(string: str):
        print(string)

    cyber.eval("new_func 'hello'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'


def test_context_add_function_two_args(capsys):
    cyber = CyberVM()

    @cyber.function('new_func')
    def _new_func(one: str, two: str):
        print(one, two)

    cyber.eval("new_func 'one' 'two'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one two\n'


def test_context_add_module(capsys):
    cyber = CyberVM()

    @cyber.function('new_module.new_func')
    def _new_func(one: float, two: float):
        print(one, two)

    script = """
    import mod 'new_module'
    mod.new_func 1 2
    """
    cyber.eval(script)

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == '1.0 2.0\n'