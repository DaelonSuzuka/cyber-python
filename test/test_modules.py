# from cyber import CyberVM, CsResultCode, CsType


# def test_override_function(capsys):
#     cyber = CyberVM()

#     @cyber.function('print')
#     def _print(string: str):
#         print('<python>', string)

#     cyber.eval("print 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == '<python> hello\n'


# def test_add_function(capsys):
#     cyber = CyberVM()

#     @cyber.function('new_func')
#     def _new_func(string: str):
#         print(string)

#     cyber.eval("new_func 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'


# def test_add_function_naked_decorator(capsys):
#     cyber = CyberVM()

#     @cyber.function
#     def new_func(string: str):
#         print(string)

#     cyber.eval("new_func 'hello'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'hello\n'


# def test_add_function_two_args(capsys):
#     cyber = CyberVM()

#     @cyber.function('new_func')
#     def _new_func(one: str, two: str):
#         print(one, two)

#     cyber.eval("new_func 'one' 'two'")

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'one two\n'


# def test_add_func_to_new_module(capsys):
#     cyber = CyberVM()

#     @cyber.function('new_module.new_func')
#     def _new_func(one: float, two: float):
#         print(one, two)

#     script = """
#         import mod 'new_module'
#         mod.new_func 1 2
#     """
#     cyber.eval(script)

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == '1.0 2.0\n'


# def test_module_inheritance(capsys):
#     cyber = CyberVM()

#     class Module(cyber.module('new_module')):
#         def test(self):
#             print('test')
#         def test2(self):
#             print('test2')

#     script = """
#         import mod 'new_module'
#         mod.test()
#         mod.test2()
#     """
#     cyber.eval(script)

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'test\ntest2\n'


# def test_module_decorator(capsys):
#     cyber = CyberVM()

#     @cyber.module('new_module')
#     class Module:
#         def test(self):
#             print('test')
#         def test2(self):
#             print('test2')

#     script = """
#         import mod 'new_module'
#         mod.test()
#         mod.test2()
#     """
#     cyber.eval(script)

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'test\ntest2\n'


# def test_variables(capsys):
#     cyber = CyberVM()

#     @cyber.function('print')
#     def _print(string: str):
#         print(string)

#     cyber.variable('one', 1)
#     cyber.variable('two', 'two')
#     cyber.variable('mod.three', 3)
#     cyber.variable('mod.foure', '4')

#     script = """
#         import mod 'mod'
#         print one
#         print two
#         print mod.three
#         print mod.foure
#     """
#     cyber.exec(script)

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == '1\ntwo\n3\n4\n'


# def test_module_with_variables(capsys):
#     cyber = CyberVM()

#     @cyber.module
#     class core:
#         var_none = None
#         var_true = True
#         var_false = False
#         var_string = 'abc'
#         var_integer = 7
#         var_number = 15.5

#         def print(self, string):
#             print(string)

#     script = """
#         print var_none
#         print var_true
#         print var_false
#         print var_string
#         print var_integer
#         print var_number
#     """
#     cyber.exec(script)

#     assert cyber.last_result == CsResultCode.CS_SUCCESS
#     captured = capsys.readouterr()
#     assert captured.out == 'None\nTrue\nFalse\nabc\n7\n15.5\n'
