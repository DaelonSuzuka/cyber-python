from cyber import *


cyber = CyberVM()

# @CyFunc
# def beep(vm, args, nargs):
#     print('beep')
#     return 0

# @CyLoadModuleFunc
# def load_test(vm, mod):
#     print("load_test")
#     cyber.set_module_func(mod, 'beep', 0, beep)
#     return True

# cyber.add_module_loader('test', load_test)
# cyber.add_module_loader('test2', load_test)


# @CyFunc
# def fuck(vm, args, nargs):
#     print('fuck')
#     return 0

# @CyLoadModuleFunc
# def load_fuck(vm, mod):
#     print("load_fuck")
#     cyber.set_module_func(mod, 'fuck', 0, fuck)
#     return True

# cyber.add_module_loader('fuck', load_fuck)


# override existing symbol - WORKS
with cyber.module('core') as module:
    @module.function('print')
    def _print(string: str):
        print('<py>', string)

# add symbol to existing module - WORKS
with cyber.module('test') as module:
    @module.function('beep')
    def beep():
        print('<beep>')

# add new module - DOES NOT WORK
with cyber.module('wtf') as module:
    @module.function('boop')
    def boop():
        print('<boop>')

script = """
import test 'test'
import wtf 'wtf'

print 'pls work'

test.beep()
"""

cyber.eval(script)
