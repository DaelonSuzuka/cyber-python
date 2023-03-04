from cyber import *


cyber = CyberVM()

# @CyFunc
# def beep(vm, args, nargs):
#     print('beep')
#     return 0

# @CyLoadModuleFunc
# def load_core(vm, mod):
#     print("load_core")
#     cyber.set_module_func(mod, 'beep', 0, beep)
#     return True

# cyber.add_module_loader('core', load_core)

        

with cyber.module('core') as module:
    @module.function('beep')
    def beep(vm, args, nargs):
        print('beep')
        return 0
    
    @module.function('print', 1)
    def beep2(vm, args, nargs):
        s = cyValueToTempString(vm, args[0])
        print(s.charz)
        return 0

script = """
print 'hello cyberworld!'

"""
cyber.eval(script)
