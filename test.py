from src.cyber import *


cyber = CyberVM()

with cyber.module('core') as module:
    @module.function('print')
    def _print(string: str):
        print('<py>', string)


script = """
print 'hello'
"""

cyber.eval(script)
