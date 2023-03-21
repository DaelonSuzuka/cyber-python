from cyber import CyberVM, CyResultCode


def test_default_value(capsys):
    cyber = CyberVM()

    @cyber.function('core.test')
    def _new_func(one, two='default'):
        print(one, two)

    cyber.exec("test 'one' 'two'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one two\n'

    cyber.exec("test 'one'")

    assert cyber.last_result == CyResultCode.CY_Success
    captured = capsys.readouterr()
    assert captured.out == 'one default\n'


def test_fake_varargs(capsys):
    cyber = CyberVM()

    @cyber.function('core.print')
    def _new_func(arg1='', arg2='', arg3='', arg4='', arg5=''):
        args = [arg1, arg2, arg3, arg4, arg5]
        message = ''
        for arg in args:
            if arg:
                message += str(arg)
                message += ' '
        message = message.rstrip()
        print(message)

    cyber.exec("print 'one'")
    assert capsys.readouterr().out == 'one\n'

    cyber.exec("print 'one' 'two'")
    assert capsys.readouterr().out == 'one two\n'

    cyber.exec("print 'one' 'two' 3")
    assert capsys.readouterr().out == 'one two 3.0\n'

    cyber.exec("print 'one' 'two' 3 4")
    assert capsys.readouterr().out == 'one two 3.0 4.0\n'

    cyber.exec("print('one', 'two', [1, 2, 3])")
    assert capsys.readouterr().out == 'one two [1.0, 2.0, 3.0]\n'